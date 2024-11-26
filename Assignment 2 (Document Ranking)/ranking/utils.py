import os
from collections import Counter
import math

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
    """
    Calculate TF-IDF scores for documents based on a query.

    Parameters:
        documents (dict): A dictionary where keys are document names and values are their content.
        query (str): The search query to rank documents by relevance.

    Returns:
        list: A sorted list of tuples containing document names and their TF-IDF scores.
    """
    # Normalize query and split into words
    query_words = query.lower().split()

    # Total number of documents
    num_documents = len(documents)

    # Dictionary to store document frequency for each term
    term_doc_count = Counter()

    # Preprocess documents and calculate term frequencies
    doc_word_counts = {}
    for doc_name, content in documents.items():
        words = content.lower().split()
        word_count = Counter(words)
        doc_word_counts[doc_name] = word_count
        for word in set(words):
            term_doc_count[word] += 1

    # Calculate TF-IDF scores
    doc_scores = []
    for doc_name, word_count in doc_word_counts.items():
        tf_idf_score = 0
        total_words = sum(word_count.values())
        for word in query_words:
            # Correct minor errors in query words by matching the closest term
            word_matches = [term for term in term_doc_count.keys() if term.startswith(word[:3])]
            word = word_matches[0] if word_matches else word

            # Calculate Term Frequency (TF)
            tf = word_count.get(word, 0) / total_words

            # Calculate Inverse Document Frequency (IDF)
            doc_freq = term_doc_count.get(word, 0)
            idf = math.log((1 + num_documents) / (1 + doc_freq)) + 1 if doc_freq > 0 else 0

            # TF-IDF score contribution for the word
            tf_idf_score += tf * idf

        # Append the document and its score
        doc_scores.append((doc_name, tf_idf_score))

    # Sort documents by their TF-IDF score in descending order
    return sorted(doc_scores, key=lambda x: x[1], reverse=True)
