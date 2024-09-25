from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader

def cleanString(inString):
    """
    Takes in a string and replaces extra lines ('\n') and '..' with nothing,
    essentially removing them
    :param inString: string of text
    :return: outString: cleaned text
    """
    outString = inString.replace('\n','').replace('..','')
    outString = outString.lower()
    return outString

def readCorpus(document):
    """
    Function reads in PDF document and extracts text, iterates over all pages
    of document, cleans extracted text, and splits all text into individual
    sentences Prints page of document as it processes each page
    :param document: the PDF document to be analyzed
    :return: pageText is a  list of tuples of the page number and all sentences extracted and cleaned from that page
    """
    reader = PdfReader(document)
    pageText = []
    line2sentence = {}
    print(f"processing document {document} ")
    for pageNum in range(len(reader.pages)):
        if (1 + pageNum) % 4 == 0:
            print(f".", end="")
        page = reader.pages[pageNum]
        pageExtract = page.extract_text()
        pageExtract = cleanString(pageExtract)
        splitPeriod = pageExtract.split('. ')
        sentenceList = [(pageNum, sentenceNum, x) for sentenceNum, x in enumerate(splitPeriod) if len(x.split()) > 0]
        if sentenceList != []:
            pageText.extend(sentenceList)
    line2sentence.update({ix: sentTup for ix, sentTup in enumerate(pageText)})
    print(f"\n{pageNum} pages read containing {len(pageText)} sentences.")
    return pageText

if __name__ == "__main__":
    modelName = 'paraphrase-MiniLM-L6-v2'
    corpusName = 'DOT_PerformancePlan.pdf'
    print(f"This is the main function.\n A sentence analysis is done on a target document {corpusName} by creating an embedding vector for each sentence in the document.")
    print(f"The embedding vectors are created using {modelName} with sentence transformers based on bert (https://sbert.net/).\n\n")
    print(f"With the embedding vectors in place, the user is able to query the ")
    print(f"document by submitting a query which produces a list of 10 response ")
    print(f"sentences that are best matches as determined by using a semantic search.")

    requireWords = True
    # Download model
    model = SentenceTransformer(modelName)

    # Corpus of documents and their embeddings
    corpus = readCorpus(corpusName)

    print(f"Creating the embeddings for {len(corpus)} sentences")
    corpus_embeddings = model.encode([x[2] for x in corpus])

    # Queries and their embeddings
    queries = [input('search:\n')]

    # Continues to ask for new queries until 'quit' is inputted
    while len(queries) > 0 and queries[0] != 'quit':
        queries_embeddings = model.encode(queries)
        # Find the top-10 corpus documents matching each query
        hits = util.semantic_search(queries_embeddings, corpus_embeddings, top_k=10)
        hit = hits[0]
        qWords = queries[0].split()
        for _h in hit:
            lineTxt = corpus[_h['corpus_id']][2]
            if all(x in lineTxt for x in qWords) or not requireWords:
                print(f"score changed from {_h['score']} to ", end="")
                _h['score'] += .1 if _h['score'] < 0.9 else 1.0
                print(f" {_h['score']}")
        hit.sort(key=lambda x: -x['score'])
        # Print results of first query
        print(f"Query: {queries[0]}")
        print("score: Page number, line number, text")
        for _h in hit:
            print(f"{_h['score']}: {corpus[_h['corpus_id']]}")
        queries = [input('search:\n')]

    print("Done")

