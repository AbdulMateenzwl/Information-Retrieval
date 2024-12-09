from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from collections import defaultdict
from django.conf import settings
import re

def get_presentation(request):
    slides = [
        {
            "title": "Fuzzy Set Theory",
            "content": [
                "Imagine regular search is like a light switch—it's either on (relevant) or off (not relevant).",
                "With the fuzzy model, it's like a dimmer switch. It can be a little relevant, somewhat relevant, or very relevant.",
                "Fuzzy set theory allows for degrees of membership rather than strict binary membership.",
                "An element can have a partial or fuzzy membership in a set.",
            ],
        },
        {
            "title": "Fuzzy Set Theory in IR",
            "content": [
                "Documents or queries can be associated with multiple degrees of relevance.",
                "Instead of just being relevant or irrelevant, a document can be partially relevant to a query.",
                "Fuzzy set-based IR models help address ambiguity and vagueness in retrieval tasks.",
                "These models allow for a nuanced representation of relevance.",
            ],
        },
        {
            "title": "Extended Boolean Model",
            "content": [
                "Regular search uses simple words like 'AND,' 'OR,' and 'NOT' to find things.",
                "The extended Boolean model allows more specific queries like 'Fruits OR Vegetables BUT NOT Processed Food'.",
                "It enhances the precision and flexibility of traditional Boolean search.",
            ],
        },
        {
            "title": "Generalized Vector Model",
            "content": [
                "Documents and queries are represented as vectors in a multi-dimensional space.",
                "Each dimension corresponds to a unique term or feature.",
                "Documents and queries are like arrows in this space, with direction and length indicating relevance.",
            ],
        },
        {
            "title": "Algebraic IR Models: Latent Semantic Indexing (LSI)",
            "content": [
                "Algebraic IR models, like LSI, go beyond simple word matching to understand semantic relationships.",
                "LSI uses Singular Value Decomposition (SVD) to analyze relationships between terms in large corpora.",
                "LSI discovers hidden semantic structures, retrieving conceptually related documents even without exact word matches.",
            ],
        },
    ]
    return JsonResponse({"slides": slides})


# Mock data for hypertext nodes
HYPERTEXT_NODES = {
    "home": {
        "title": "Information Retrieval Models",
        "content": "Welcome! Explore the concepts of IR models by clicking on the links below.",
        "links": {
            "fuzzy_set": "Fuzzy Set Theory",
            "boolean_model": "Extended Boolean Model",
            "vector_model": "Generalized Vector Model",
            "lsi_model": "Algebraic IR Models (LSI)"
        }
    },
    "fuzzy_set": {
        "title": "Fuzzy Set Theory",
        "content": """
            Imagine regular search is like a light switch—it's either on or off. 
            The fuzzy model is like a dimmer switch, allowing for partial relevance.
        """,
        "links": {"home": "Back to Home"}
    },
    "boolean_model": {
        "title": "Extended Boolean Model",
        "content": """
            Extended Boolean Model uses enhanced Boolean operators for more 
            specific searches, like 'Fruits OR Vegetables BUT NOT Processed Food.'
        """,
        "links": {"home": "Back to Home"}
    },
    "vector_model": {
        "title": "Generalized Vector Model",
        "content": """
            In this model, documents and queries are represented as vectors in a multi-dimensional space, 
            with direction and length indicating relevance and importance.
        """,
        "links": {"home": "Back to Home"}
    },
    "lsi_model": {
        "title": "Algebraic IR Models (LSI)",
        "content": """
            Latent Semantic Indexing (LSI) uses mathematical techniques to discover 
            hidden semantic structures in text, retrieving conceptually related documents.
        """,
        "links": {"home": "Back to Home"}
    }
}

def hypertext_node_view(request, node="home"):
    """
    View to fetch content of a specific hypertext node.
    """
    node_data = HYPERTEXT_NODES.get(node, {"title": "Not Found", "content": "Node does not exist.", "links": {"home": "Back to Home"}})
    return render(request, "hypertext_node.html", {"node": node_data})