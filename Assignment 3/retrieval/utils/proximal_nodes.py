def retrieve_proximal_nodes_from_graph(query, graph, documents):
    """
    Retrieve documents based on proximal nodes from a predefined graph.

    Parameters:
        - query_word: The word input by the user.
        - graph: A dictionary mapping words to their related words.
        - documents: A dictionary of document IDs and their content.

    Returns:
        - A dictionary of relevant document IDs and their content.
    """
    # Preprocess query to extract related words
    query = query.lower()
    related_words = set(graph.get(query, []))  # Get related words from the graph
    related_words.add(query)  # Include the query itself in related words

    # Dictionary to store document scores
    doc_scores = {doc_id: 0 for doc_id in documents}

    # Search documents containing any of the related words and calculate scores
    for word in related_words:
        for doc_id, content in documents.items():
            if word in content.lower():  # Case-insensitive matching
                doc_scores[doc_id] += 1  # Increment score for each match

    # Sort documents by score in descending order
    ranked_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)

    # Filter out documents with a score of 0 and return only their IDs
    return [doc_id for doc_id, score in ranked_docs if score > 0]
