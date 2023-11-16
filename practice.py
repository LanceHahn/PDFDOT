from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader

def cleanString(inString):

    outString = inString.replace('\n','').replace('..','')
    outString = outString.lower()

    return outString

def readCorpus(document):
    """
    function reads in PDF document and extracts text from a specified
    page
    :param document: the PDF document to be analyzed
    :return: pageText is the extracted lowercase text

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

# MAIN

# Download model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Corpus of documents and their embeddings

corpus = readCorpus('DOT_PerformancePlan.pdf')

# Combined sentences on each page, first element is page number
newCorpus = combineSentences(corpus)

# did not change this, so it still encodes based on tuple of (pageNum, individual sentence), not newCorpus
# tried changing it to work for newCorpus, but couldn't get it right

#corpus = ['Python is an interpreted high-level general-purpose programming language.',
#    'Python is dynamically-typed and garbage-collected.',
#    'The quick brown fox jumps over the lazy dog.']
#
#corpus = readCorpus('DOT_PerformancePlan.pdf')
#
# corpus_embeddings = model.encode([x[1] for x in corpus])
corpus_embeddings = model.encode([sent for page in newCorpus for sent in page[1:]])

# Queries and their embeddings
queries = [input('search:\n')]
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



# Run key-word analysis to generate key word list for each page.
# re-assemble each page of text from corpus
# determine key words for each page
# look for amount overlap between the identified key words for each page and
# the words in the search
# list the pages with most overlap and what query words were included
print("Done")