import argparse
import os
from os.path import join

from flask import Flask, escape, jsonify, render_template, request

from .init_loader import load_init
from .ranking import OkapiBM25Ranker


ROOT = os.getenv('ROOT')


def create_app():
    collection, lexicon, images_handler = load_init(ROOT)
    ranker = OkapiBM25Ranker(collection, lexicon)

    app = Flask(
        __name__,
        template_folder=join(ROOT, 'src/typing_assistant/client/templates'),
        static_folder=join(ROOT, 'src/typing_assistant/client/static'),
    )

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/partial_query', methods=['POST'])
    def partial_query():
        partial_query = str(escape(request.form.get('partial_query')))
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

    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-ht', '--host', action='store', default='localhost')
    parser.add_argument('-p', '--port', action='store', default='8080')
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    args = parser.parse_args()

    app = create_app()
    app.run(
        host=args.host,
        port=int(args.port),
        debug=args.debug,
    )
