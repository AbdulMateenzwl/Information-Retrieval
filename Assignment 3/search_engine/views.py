from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from collections import defaultdict
from django.conf import settings
import re
from .utils.bim import calculate_bim
from .utils.non_overlap import non_overlapped_lists
from .utils.sample_data import RELATED_WORDS_GRAPH
from .utils.proximal_nodes import retrieve_proximal_nodes_from_graph

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
# print(DOCUMENTS)

def find_matching_lines(query, documents):
    """
    Find lines in documents that contain the query.
    :param query: The word or phrase to search for.
    :param documents: A dictionary of document names and their content.
    :return: A list of dictionaries with document names and matching lines.
    """
    query_lower = query.lower()
    matching_lines = []

    # Search each document's content for the query
    for doc_name, content in documents.items():
        lines = content.splitlines()
        for line in lines:
            if query_lower in line.lower():
                # Highlight the query in the matching line
                highlighted_line = re.sub(
                    re.escape(query),
                    f"<mark>{query}</mark>",
                    line,
                    flags=re.IGNORECASE
                )
                matching_lines.append({"document": doc_name, "line": highlighted_line.strip()})
    
    return matching_lines

def search_view(request):
    results = []
    if request.method == "POST":
        query = request.POST.get('query', '')
        model = request.POST.get('model', 'bim')  # Default to BIM

        if model == 'bim':
            results = calculate_bim(DOCUMENTS, query)
        elif model == 'non_overlap':
            terms = query.split()
            results = non_overlapped_lists(DOCUMENTS,terms)
        elif model == 'proximal_nodes':
            results = retrieve_proximal_nodes_from_graph(query, RELATED_WORDS_GRAPH, DOCUMENTS)
    
    return render(request, "search.html", {"results": results})

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
