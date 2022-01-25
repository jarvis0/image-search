import argparse
from os.path import join

from flask import Flask, escape, render_template, request

from .config import config
from .indexing.indexes_loader import load_indexes
from .ranking import OkapiBM25Ranker


def create_web_app():
    collection, lexicon, images_handler = load_indexes(config.ROOT)
    ranker = OkapiBM25Ranker(collection, lexicon)

    web_app = Flask(
        __name__,
        template_folder=join(config.ROOT, 'src/typing_assistant/client/templates'),
        static_folder=join(config.ROOT, 'src/typing_assistant/client/static'),
    )

    @web_app.route('/')
    def index():
        return render_template('index.html')

    @web_app.route('/predict_next_word', methods=['POST'])
    def predict_next_word():
        partial_query = str(escape(request.form.get('partial_query')))
        response = {'next_word_prediction': partial_query}
        return response

    @web_app.route('/query_partially', methods=['POST'])
    def query_partially():
        partial_query = str(escape(request.form.get('partial_query')))
        query_results = ranker.lookup_query(partial_query)
        query_results = [text.text for _, text, _ in query_results]
        response = {'partial_query_results': query_results}
        return response

    @web_app.route('/query', methods=['POST'])
    def query():
        query = str(escape(request.form.get('query', '')))
        query_results = ranker.lookup_query(query)
        query_results = [(images_handler.get_url(doc_id), text, round(score, 4)) for doc_id, text, score in query_results]
        return render_template('query.html', query=query, query_results=query_results)

    return web_app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-hs', '--host', action='store', default='localhost')
    parser.add_argument('-p', '--port', action='store', default='8080')
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    args = parser.parse_args()

    web_app = create_web_app()
    web_app.run(
        host=args.host,
        port=int(args.port),
        debug=args.debug,
    )
