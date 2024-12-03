# Binary Independence Model implementation
def calculate_bim(documents, query):
    """
    Binary Independence Model for information retrieval.

    Args:
        documents (dict): A dictionary where keys are document IDs and values are the text of the documents.
        query (str): The search query.

    Returns:
        list: Ranked list of document IDs based on relevance scores.
    """
    # Preprocess the documents and query
    def preprocess(text):
        # Simple preprocessing: convert to lowercase, split into words, remove duplicates
        return set(text.lower().split())

    processed_documents = {doc_id: preprocess(content) for doc_id, content in documents.items()}
    processed_query = preprocess(query)

    # Calculate scores for each document
    scores = {}
    for doc_id, words in processed_documents.items():
        # Count matching words
        matching_words = processed_query.intersection(words)
        scores[doc_id] = len(matching_words)  # Score based on count of matching words

    # Filter documents with a score of zero
    zero_score_docs = [doc_id for doc_id, score in scores.items() if score == 1]

    return zero_score_docs
