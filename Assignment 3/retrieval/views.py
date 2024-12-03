from django.shortcuts import render
from .utils.sample_data import DOCUMENTS
from .utils.bim import calculate_bim
from .utils.non_overlap import non_overlapped_lists
from .utils.sample_data import DOCUMENTS, RELATED_WORDS_GRAPH
from .utils.proximal_nodes import retrieve_proximal_nodes_from_graph

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
    
    return render(request, "retrieval/search.html", {"results": results})
