def non_overlapped_lists(documents, query_terms):
    """
    Non-Overlapped List Model for Information Retrieval.
    
    Args:
        documents (dict): A dictionary where keys are document IDs and values are document content.
        query_terms (list): A list of terms to search for in the documents.

    Returns:
        dict: A dictionary where keys are terms and values are lists of document IDs containing that term.
    """
    # Preprocess query terms (case-insensitive matching)
    query_terms = [term.lower() for term in query_terms]
    
    # Dictionary to store results for each query term
    results = {term: [] for term in query_terms}

    # Search documents for each query term
    for term in query_terms:
        for doc_id, content in documents.items():
            if term in content.lower():  # Case-insensitive matching
                results[term].append(doc_id)

    # Combine all document lists into a non-overlapping set
    combined_docs = set()
    for doc_list in results.values():
        combined_docs.update(doc_list)

    # Rank combined documents by frequency of matching terms
    doc_scores = {doc_id: 0 for doc_id in combined_docs}
    for term, doc_list in results.items():
        for doc_id in doc_list:
            doc_scores[doc_id] += 1  # Increment score for each term match

    # Sort documents by score in descending order
    ranked_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)

    val =  {"term_results": results, "ranked_documents": [doc_id for doc_id, _ in ranked_docs]}
    print(val)
    return val
