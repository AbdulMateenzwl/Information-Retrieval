from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from collections import defaultdict
from django.conf import settings

DOCUMENTS_DIR = os.path.join(settings.BASE_DIR, 'documents')

def build_index():
    index = defaultdict(list)
    title_index = {}
    
    for filename in os.listdir(DOCUMENTS_DIR):
        file_path = os.path.join(DOCUMENTS_DIR, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                title_index[filename] = content
                words = content.split()
                for word in words:
                    index[word.lower()].append(filename)
    return index, title_index

INDEX, TITLE_INDEX = build_index()

def search_by_content(query):
    query = query.lower()
    return list(set(INDEX.get(query, [])))

def search_by_title(title):
    if title in TITLE_INDEX:
        return [title]
    return []


@csrf_exempt
def search_view(request):
    if request.method == 'POST':
        query_type = request.POST.get('type', 'content')
        query = request.POST.get('query', '')

        if query_type == 'title':
            results = search_by_title(query)
        else:
            results = search_by_content(query)

        return JsonResponse({'results': results})

    return render(request, 'search.html')
