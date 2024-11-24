import os
from collections import Counter
from math import log

DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), 'documents')

def read_documents():
    """Read all documents from the documents directory."""
    documents = {}
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(DOCUMENTS_DIR, filename), 'r') as file:
                documents[filename] = file.read()
    return documents

def keyword_matching(query, documents):
    """Rank documents based on keyword matching."""
    query_words = query.lower().split()
    rankings = []
    for doc_name, content in documents.items():
        doc_words = content.lower().split()
        match_count = sum(word in doc_words for word in query_words)
        rankings.append((doc_name, match_count))
    return sorted(rankings, key=lambda x: x[1], reverse=True)

def calculate_tf_idf(query, documents):
    """Rank documents based on TF-IDF scoring."""
    query_words = query.lower().split()
    doc_count = len(documents)
    term_doc_count = Counter()
    
    for content in documents.values():
        words = set(content.lower().split())
        term_doc_count.update(words)
    
    rankings = []
    for doc_name, content in documents.items():
        tf_idf_score = 0
        words = content.lower().split()
        word_count = Counter(words)
        total_words = len(words)
        
        for word in query_words:
            tf = word_count[word] / total_words
            idf = log(doc_count / (1 + term_doc_count[word]))
            tf_idf_score += tf * idf
        
        rankings.append((doc_name, tf_idf_score))
    return sorted(rankings, key=lambda x: x[1], reverse=True)
