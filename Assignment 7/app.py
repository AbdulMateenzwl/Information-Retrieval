from flask import Flask, render_template, request
from models import calculate_probabilities, rank_documents, calculate_belief_probabilities
from dataset import documents

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        query_text = request.form.get('query')
        model_type = request.form.get('model')
        
        if model_type == "Interference":
            # Calculate probabilities based on the user query for the interference model
            probabilities = calculate_probabilities(query_text, documents)
            ranked_docs = rank_documents(query_text, probabilities)
        
        elif model_type == "Belief":
            # For Belief model, dynamically calculate relevance scores based on the user query
            belief_results = calculate_belief_probabilities(query_text, documents)
            ranked_docs = sorted(belief_results.items(), key=lambda x: x[1], reverse=True)
        
        else:
            ranked_docs = []

        return render_template("results.html", query=query_text, model=model_type, results=ranked_docs)

    return render_template("query.html")


if __name__ == "__main__":
    app.run(debug=True)
