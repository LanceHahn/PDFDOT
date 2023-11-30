from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader

def cleanString(inString):
    """
    Takes in a string and replaces extra lines ('\n') and '..' with nothing, essentially removing them
    :param inString: string of text
    :return: outString: cleaned text
    """
    outString = inString.replace('\n','').replace('..','')
    outString = outString.lower()
    return outString

def readCorpus(document):
    """
    Function reads in PDF document and extracts text, iterates over all pages of document,
    cleans extracted text, and splits all text into individual sentences
    Prints page of document as it processes each page
    :param document: the PDF document to be analyzed
    :return: pageText is a  list of tuples of the page number and all sentences extracted and cleaned from that page
    """
    reader = PdfReader(document)
    pageText = []
    print("processing page ")
    for pageNum in range(len(reader.pages)):
        print(f"{pageNum} ",end="")
        page = reader.pages[pageNum]
        pageExtract = page.extract_text()
        pageExtract = cleanString(pageExtract)
        splitPeriod = pageExtract.split('. ')
        sentenceList = [(pageNum, x) for x in splitPeriod if len(x.split()) > 0]
        if sentenceList != []:
            pageText.extend(sentenceList)
    print()
    return pageText

def combineSentences(sentenceTuples):
    """
    takes in the tuple of (page num, sentence) and combines sentences
    if they have the same page num (second elements of each tuple are combined
    if they match on first element)
    :param corpus: list of tuples (pagenum, sentence)
    :return: res: new list of tuples (pagenum, sentence, sentence, ...etc.)
    """
    res = []
    for sub in sentenceTuples:
        if res and res[-1][0] == sub[0]:
            res[-1].extend(sub[1:])
        else:
            res.append([ele for ele in sub])
    res = list(map(tuple,res))
    return res

if __name__ == "__main__":

    # Download model
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    # Corpus of documents and their embeddings
    corpus = readCorpus('DOT_PerformancePlan.pdf')

    # Combined sentences on each page, first element is page number
    newCorpus = combineSentences(corpus)


    corpus_embeddings = model.encode([x[1] for x in corpus])

    corpus_embeddings = model.encode([sent for page in newCorpus for sent in page[1:]])

    # Queries and their embeddings
    queries = [input('search:\n')]

    # Continues to ask for new queries until 'quit' is inputted
    while len(queries) > 0 and queries[0] != 'quit':
        print(f"your search: {queries}")
        queries_embeddings = model.encode(queries)
        # Find the top-10 corpus documents matching each query
        hits = util.semantic_search(queries_embeddings, corpus_embeddings, top_k=10)
        qWords = queries[0].split()
        lineNum = 0
        lineNumInPage = 0
        lastPage = -1
        for pgNum, lineTxt in corpus:
            if pgNum != lastPage:
                lastPage = pgNum
                lineNumInPage = 0
            lineNum += 1
            lineNumInPage += 1
            if all(x in lineTxt for x in qWords):
                print(f"{lineNum} {pgNum}:{lineNumInPage} {lineTxt}")
                ids = [ix for ix, x in enumerate(hits[0]) if corpus[x['corpus_id']][1] == lineTxt]
                if len(ids) > 0:
                    print(f"score changed from {hits[0][ids[0]]['score']} to")
                    hits[0][ids[0]]['score'] += .1
                    if hits[0][ids[0]]['score'] > 1.0:
                        hits[0][ids[0]]['score'] = 1.0
                    print(f" {hits[0][ids[0]]['score']}")
        hits[0].sort(key=lambda x: -x['score'])
        # Print results of first query
        print(f"Query: {queries[0]}")
        for hit in hits[0]:
            print(f"{hit['score']}: {corpus[hit['corpus_id']]}")
        queries = [input('search:\n')]


    print("Done")