from flask import Flask, escape, jsonify, render_template, request

from typing_assistant.binaries_loader import load_binaries
from typing_assistant.ranking import OkapiBM25Ranker


collection, lexicon, images_handler = load_binaries(binaries_path='binaries')
ranker = OkapiBM25Ranker(collection, lexicon)
app = Flask(__name__, template_folder='../server/templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/partial_query', methods=['POST'])
def partial_query():
    partial_query = str(escape(request.get_json()['partial_query']))
    query_results = ranker.lookup_query(partial_query)
    query_results = [text.text for _, text, _ in query_results]
    response = {'query_results': query_results}
    return jsonify(response)


@app.route('/query', methods=['POST'])
def query():
    query = str(escape(request.form.get('input_search', '')))
    query_results = ranker.lookup_query(query)
    query_results = [(images_handler.get_url(doc_id), text, round(score, 4)) for doc_id, text, score in query_results]
    return render_template('query.html', query=query, query_results=query_results)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
