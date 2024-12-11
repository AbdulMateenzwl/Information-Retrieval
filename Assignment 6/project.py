import math

def sigmoid(x):
    """Sigmoid activation function."""
    return 1 / (1 + math.exp(-x))

def dot_product(vec1, vec2):
    """Compute dot product of two vectors."""
    return sum(a * b for a, b in zip(vec1, vec2))

def compute_relevance_score(X, W_input, B_input, W_output, B_output):
    """
    Compute the relevance score using a feed-forward neural network with a single hidden layer.

    Parameters:
        X (list): Feature vector (input).
        W_input (list): Weights for the hidden layer.
        B_input (float): Bias for the hidden layer.
        W_output (float): Weight for the output layer.
        B_output (float): Bias for the output layer.

    Returns:
        float: Relevance score.
    """
    # Compute the hidden layer output (H)
    weighted_sum_hidden = dot_product(W_input, X) + B_input
    H = sigmoid(weighted_sum_hidden)

    # Compute the relevance score (output layer)
    relevance_score = W_output * H + B_output
    return relevance_score

# Input features (X)
X = [0.7, 0.5]  # Feature vector: [X1, X2]

# Weights and bias for the hidden layer
W_input = [0.8, 0.6]  # Weights: [W_input1, W_input2]
B_input = 0.2  # Bias for the hidden layer

# Weight and bias for the output layer
W_output = 1.5  # Weight for the output layer
B_output = -0.4  # Bias for the output layer

# Compute the relevance score
relevance_score = compute_relevance_score(X, W_input, B_input, W_output, B_output)
print(f"Relevance Score: {relevance_score:.3f}")
