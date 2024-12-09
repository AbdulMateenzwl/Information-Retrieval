from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from collections import defaultdict
from django.conf import settings
import re
from .utils.sample_data import RELATED_WORDS_GRAPH

# Path to the directory where text documents are stored
DOCUMENTS_DIR = os.path.join(settings.BASE_DIR, 'documents')

def build_index():
    """
    Build an index of documents where the key is the document name
    and the value is the document content.
    """
    DOCUMENTS = {}

    # Loop through files in the DOCUMENTS_DIR
    for filename in os.listdir(DOCUMENTS_DIR):
        file_path = os.path.join(DOCUMENTS_DIR, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                DOCUMENTS[filename] = content  # Add document name and content to the index

    return DOCUMENTS

# Initialize indexes when the server starts
DOCUMENTS = build_index()

def search_view(request):
    results = []
    if request.method == "POST":
        query = request.POST.get('query', '')
        model = request.POST.get('model', 'vector')  # Default to vector model

        if model == 'boolean':
            results = boolean_search(query, DOCUMENTS)
        elif model == 'fuzzy':
            # threshold = float(request.POST.get())  # Optional threshold parameter
            results = fuzzy_search(query, DOCUMENTS)
        elif model == 'vector':
            results = vector_search(query, DOCUMENTS)
        # elif model == 'lsi':
            # results = lsi_search(query, TERM_DOCUMENT_MATRIX)

    return render(request, "search.html", {"results": results})

def vector_search(query, documents):
    """
    Perform vector space model search using cosine similarity.
    Args:
        query (str): Search query.
        documents (dict): Document collection where keys are document IDs and values are document content.

    Returns:
        list: List of tuples (document ID, cosine similarity score).
    """
    from math import sqrt

    def calculate_term_frequency(content):
        terms = content.split()
        tf = {}
        for term in terms:
            tf[term] = tf.get(term, 0) + 1
        return tf

    def cosine_similarity(vec1, vec2):
        dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) for term in set(vec1) | set(vec2))
        magnitude1 = sqrt(sum(value ** 2 for value in vec1.values()))
        magnitude2 = sqrt(sum(value ** 2 for value in vec2.values()))
        return dot_product / (magnitude1 * magnitude2) if magnitude1 and magnitude2 else 0

    query_tf = calculate_term_frequency(query)
    results = []
    for doc_id, content in documents.items():
        doc_tf = calculate_term_frequency(content)
        score = cosine_similarity(query_tf, doc_tf)
        results.append((doc_id, score))
    return sorted(results, key=lambda x: x[1], reverse=True)


def fuzzy_search(query, documents,threshold=0.5 ):
    """
    Perform Fuzzy search on a collection of documents based on membership scores.
    Args:
        query (str): Search query.
        documents (dict): Document collection where keys are document IDs and values are document content.
        threshold (float): Minimum relevance score for a document to be considered relevant.

    Returns:
        list: List of tuples (document ID, relevance score).
    """
    
    def calculate_membership(query_terms, doc_terms):
        matches = sum(1 for term in query_terms if term in doc_terms)
        return matches / len(query_terms)

    query_terms = set(query.split())
    results = []
    for doc_id, content in documents.items():
        doc_terms = set(content.split())
        score = calculate_membership(query_terms, doc_terms)
        if score >= threshold:
            results.append((doc_id, score))

    print(DOCUMENTS)
    print(results)
    return sorted(results, key=lambda x: x[1], reverse=True)

def boolean_search(query, documents):
    """
    Perform Boolean search on a collection of documents.
    Args:
        query (str): Boolean query (e.g., "term1 AND term2 OR NOT term3").
        documents (dict): Document collection where keys are document IDs and values are document content.

    Returns:
        list: List of matching document IDs.
    """
    def evaluate_boolean_expression(expression, terms):
        import re
        # Replace logical operators with Python equivalents
        expression = re.sub(r"\bAND\b", "and", expression)
        expression = re.sub(r"\bOR\b", "or", expression)
        expression = re.sub(r"\bNOT (\w+)", r"'\\1' not in terms", expression)
        expression = re.sub(r"(\w+)", r"'\\1' in terms", expression)

        print(f"Transformed Expression: {expression}")  # Debug print

        try:
            return eval(expression)
        except Exception as e:
            raise ValueError(f"Invalid Boolean query: {expression}. Error: {e}")

    results = []
    for doc_id, content in documents.items():
        terms = set(content.split())  # Split document content into a set of terms
        if evaluate_boolean_expression(query, terms):
            results.append(doc_id)
    return results


def update_index(file_path, filename):
    """
    Update the indexes with a new or modified file.
    :param file_path: Path to the file to index.
    :param filename: Name of the file being indexed.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        DOCUMENTS[filename] = content
        TITLE_INDEX[filename] = content
        words = content.split()
        # Update the word-to-document index
        for word in words:
            INDEX[word.lower()].append(filename)

@csrf_exempt
def upload_file_view(request):
    """
    Handle file uploads.
    Accepts .txt files and updates the index upon successful upload.
    """
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # Validate the uploaded file type
        if not uploaded_file.name.endswith('.txt'):
            return JsonResponse({'success': False, 'message': 'Only .txt files are allowed.'})

        # Save the file to the DOCUMENTS_DIR
        file_path = os.path.join(DOCUMENTS_DIR, uploaded_file.name)
        with open(file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Update the index with the new file
        update_index(file_path, uploaded_file.name)

        return JsonResponse({'success': True, 'message': 'File uploaded and index updated successfully.'})

    # Respond with an error for invalid requests
    return JsonResponse({'success': False, 'message': 'Invalid request.'})


documents = {
    "doc1": "machine learning artificial intelligence",
    "doc2": "deep learning neural networks",
    "doc3": "artificial intelligence neural networks",
}


print(boolean_search(" artificial AND intelligence OR NOT deep ", documents))
 