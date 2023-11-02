from sentence_transformers import SentenceTransformer, util

# Download model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Corpus of documents and their embeddings
corpus = ['Python is an interpreted high-level general-purpose programming language.',
    'Python is dynamically-typed and garbage-collected.',
    'The quick brown fox jumps over the lazy dog.']
corpus_embeddings = model.encode(corpus)

# Queries and their embeddings
queries = [input('search:\n')]
print(f"your search: {queries}")
queries_embeddings = model.encode(queries)

# Find the top-10 corpus documents matching each query
hits = util.semantic_search(queries_embeddings, corpus_embeddings, top_k=10)

# Print results of first query
print(f"Query: {queries[0]}")
for hit in hits[0]:
    print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
# Query: What is Python?
# Python is an interpreted high-level general-purpose programming language. (Score: 0.6759)
# Python is dynamically-typed and garbage-collected. (Score: 0.6219)

