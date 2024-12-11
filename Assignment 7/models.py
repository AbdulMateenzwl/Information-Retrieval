import math
from collections import Counter

# Tokenization and Helper Functions
def tokenize(text):
    """Tokenize text: lowercase and split by spaces."""
    return text.lower().split()

def calculate_tf(doc):
    """Calculate term frequency for a document."""
    tokens = tokenize(doc)
    tf = Counter(tokens)
    return {word: freq / len(tokens) for word, freq in tf.items()}

# Interference Model
def calculate_probabilities(query, documents):
    """
    Compute probabilities for query-document pairs.
    P(Relevance | Query) ∝ Σ P(Term | Document)
    """
    probabilities = {}
    query_tokens = tokenize(query)
    
    for doc_id, doc in documents.items():
        doc_tf = calculate_tf(doc)
        # Calculate the average term frequency for query terms in the document
        prob = sum(doc_tf.get(token, 0) for token in query_tokens) / len(query_tokens)
        probabilities[doc_id] = prob
    
    return probabilities

def rank_documents(query, probabilities):
    """Rank documents for a query based on their relevance probabilities, excluding zero scores."""
    ranked_docs = sorted(
        [(doc_id, score) for doc_id, score in probabilities.items() if score > 0],
        key=lambda x: x[1],
        reverse=True
    )
    return ranked_docs

# Belief Network
def joint_probability(query_prob, relevance_prob, doc_feature_prob):
    """Calculate joint probability P(Query, Relevance, DocumentFeatures)."""
    return query_prob * relevance_prob * doc_feature_prob

def marginal_probability(joint_probs):
    """Calculate marginal probabilities by summing over joint probabilities."""
    if not joint_probs:
        return 0  # Avoid division by zero in the belief model
    return sum(joint_probs)

def bayes_theorem(p_relevance, p_query_given_relevance, p_query):
    """Compute P(Relevance | Query) using Bayes' theorem."""
    if p_query == 0:  # To avoid division by zero
        raise ValueError("P(Query) cannot be zero.")
    return (p_query_given_relevance * p_relevance) / p_query

def calculate_belief_probabilities(query, documents, relevance_scores=None):
    """
    Compute P(Relevance | Query) dynamically using Bayes' theorem.
    If no relevance scores are passed, calculate it based on query-document terms.
    """
    belief_results = {}
    
    # If relevance scores are provided, use them, otherwise calculate them based on query-document match.
    for doc_id, doc in documents.items():
        query_prob = len(set(tokenize(query)) & set(tokenize(doc))) / len(set(tokenize(query)))  # Query-document match ratio
        
        # If relevance_scores are not provided, calculate relevance dynamically
        relevance_prob = relevance_scores.get(doc_id, 0.5) if relevance_scores else query_prob  # Default relevance is based on query match
        
        marginal_prob = query_prob * relevance_prob
        try:
            posterior = bayes_theorem(relevance_prob, query_prob, marginal_prob)
        except ValueError:
            posterior = 0  # Handle cases where there's a zero probability
        
        if posterior > 0:  # Only include documents with positive probabilities
            belief_results[doc_id] = posterior
    
    return belief_results
