from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from collections import defaultdict
from django.conf import settings
import re
import math


# Helper functions
def sigmoid(x):
    """Sigmoid activation function."""
    return 1 / (1 + math.exp(-x))

def dot_product(vec1, vec2):
    """Compute dot product of two vectors."""
    return sum(a * b for a, b in zip(vec1, vec2))

def compute_relevance_score(X, W_input, B_input, W_output, B_output):
    """Compute relevance score."""
    weighted_sum_hidden = dot_product(W_input, X) + B_input
    H = sigmoid(weighted_sum_hidden)
    relevance_score = W_output * H + B_output
    return relevance_score

# Django view
def relevance_score_view(request):
    # Default values
    default_values = {
        "X1": 0.7,
        "X2": 0.5,
        "W_input1": 0.8,
        "W_input2": 0.6,
        "B_input": 0.2,
        "W_output": 1.5,
        "B_output": -0.4,
    }

    relevance_score = None

    if request.method == "POST":
        # Get values from the form
        X1 = float(request.POST.get("X1", 0))
        X2 = float(request.POST.get("X2", 0))
        W_input1 = float(request.POST.get("W_input1", 0))
        W_input2 = float(request.POST.get("W_input2", 0))
        B_input = float(request.POST.get("B_input", 0))
        W_output = float(request.POST.get("W_output", 0))
        B_output = float(request.POST.get("B_output", 0))

        # Compute the relevance score
        X = [X1, X2]
        W_input = [W_input1, W_input2]
        relevance_score = compute_relevance_score(X, W_input, B_input, W_output, B_output)

    return render(request, "relevance_score.html", {
        "default_values": default_values,
        "relevance_score": relevance_score,
    })

