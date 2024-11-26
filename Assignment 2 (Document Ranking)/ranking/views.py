from django.shortcuts import render
from .utils import read_documents, keyword_matching, calculate_tf_idf

def search_view(request):
    # Initialize an empty list to store the search results
    results = []
    
    # Check if the request method is POST (i.e., form submission)
    if request.method == "POST":
        # Get the search query and search type from the POST data
        query = request.POST.get('query', '')  # Default to empty string if query is not provided
        search_type = request.POST.get('type', 'content')  # Default to 'content' if type is not provided
        
        # Read all documents (this could be fetching from a database or file system)
        documents = read_documents()
        
        # Perform search if query is provided
        if query:
            # If the search type is 'content', perform keyword matching
            if search_type == 'content':
                results = keyword_matching(query, documents)
            # If the search type is not 'content', use TF-IDF ranking
            else:
                results = calculate_tf_idf(query, documents)
    
    # Render the search results in the template

    print(results)
    return render(request, 'ranking/search.html', {'results': results})
