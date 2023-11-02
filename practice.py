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
    :return: pageOutputLower is the extracted lowercase text
    """
    reader = PdfReader(document)
    pageText = []
    for pageNum in range(len(reader.pages)):
        print(f"processing page {pageNum}")
        page = reader.pages[pageNum]
        pageExtract = page.extract_text()
        pageExtract = cleanString(pageExtract)
        splitPeriod = pageExtract.split('. ')
        sentenceList = [(pageNum, x) for x in splitPeriod if len(x.split()) > 0]
        if sentenceList != []:
            pageText.extend(sentenceList)
    return pageText

# Download model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Corpus of documents and their embeddings
corpus = ['Python is an interpreted high-level general-purpose programming language.',
    'Python is dynamically-typed and garbage-collected.',
    'The quick brown fox jumps over the lazy dog.']

corpus = readCorpus('DOT_PerformancePlan.pdf')
corpus_embeddings = model.encode([x[1] for x in corpus])

# Queries and their embeddings
queries = [input('search:\n')]
print(f"your search: {queries}")
queries_embeddings = model.encode(queries)

# Find the top-10 corpus documents matching each query
hits = util.semantic_search(queries_embeddings, corpus_embeddings, top_k=10)

# Print results of first query
print(f"Query: {queries[0]}")
for hit in hits[0]:
    print(f"{hit['score']}: {corpus[hit['corpus_id']]}")

# Run key-word analysis to generate key word list for each page.
# re-assemble each page of text from corpus
# determine key words for each page
# look for amount overlap between the identified key words for each page and
# the words in the search
# list the pages with most overlap and what query words were included

