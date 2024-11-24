from django.shortcuts import render
from .utils import read_documents, keyword_matching, calculate_tf_idf

def search_view(request):
    results = []
    if request.method == "POST":
        query = request.POST.get('query', '')
        search_type = request.POST.get('type', 'content')
        documents = read_documents()
        
        if query:
            if search_type == 'content':
                results = keyword_matching(query, documents)
            else:
                results = calculate_tf_idf(query, documents)
    return render(request, 'ranking/search.html', {'results': results})
