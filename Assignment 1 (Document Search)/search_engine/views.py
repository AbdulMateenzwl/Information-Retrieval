from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from collections import defaultdict
from django.conf import settings
import re

# Path to the directory where text documents are stored
DOCUMENTS_DIR = os.path.join(settings.BASE_DIR, 'documents')

def build_index():
    """
    Build indexes for quick searching.
    - `index`: Maps words to the documents they appear in.
    - `title_index`: Maps document titles to their full content.
    - `documents`: Stores the complete content of all documents.
    """
    index = defaultdict(list)
    title_index = {}
    documents = {}

    # Loop through files in the DOCUMENTS_DIR
    for filename in os.listdir(DOCUMENTS_DIR):
        file_path = os.path.join(DOCUMENTS_DIR, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                title_index[filename] = content
                documents[filename] = content
                # Tokenize and index each word
                words = content.split()
                for word in words:
                    index[word.lower()].append(filename)
    return index, title_index, documents

# Initialize indexes when the server starts
INDEX, TITLE_INDEX, DOCUMENTS = build_index()

def search_by_content(query):
    """
    Search documents by content.
    :param query: The word to search for in document content.
    :return: A list of document filenames containing the query.
    """
    query = query.lower()
    return list(set(INDEX.get(query, [])))

def search_by_title(title):
    """
    Search documents by title.
    :param title: The title of the document to search for.
    :return: A list containing the title if it exists, otherwise an empty list.
    """
    if title in TITLE_INDEX:
        return [title]
    return []

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

@csrf_exempt
def search_view(request):
    """
    Handle search requests.
    Supports POST requests for content-based or title-based searches.
    """
    if request.method == 'POST':
        # Get query type and query text from the request
        query_type = request.POST.get('type', 'content')
        query = request.POST.get('query', '')

        # Return empty results if the query is missing
        if not query:
            return JsonResponse({'results': []})

        # Perform the search based on the query type
        if query_type == 'title':
            results = search_by_title(query)
        else:
            results = find_matching_lines(query, DOCUMENTS)

        return JsonResponse({'results': results})

    # Render the search interface for GET requests
    return render(request, 'search.html')

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
