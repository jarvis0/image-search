from os.path import join

from flask import Flask, escape, render_template, request

from .config import config
from .context import Context
from .indexing.indexes_loader import load_indexes
from .suggestions import OkapiBM25Ranker, TypingAssistant


def create_web_app():
    context = Context(config.ROOT)
    collection, lexicon, images_handler = load_indexes(config.ROOT)
    ranker = OkapiBM25Ranker(context, collection, lexicon)
    assistant = TypingAssistant(context, lexicon)

    web_app = Flask(
        __name__,
        template_folder=join(config.ROOT, 'src/typing_assistant/client/templates'),
        static_folder=join(config.ROOT, 'src/typing_assistant/client/static'),
    )

    @web_app.route('/')
    def index():
        return render_template('index.html')

    @web_app.route('/complete', methods=['POST'])
    def complete():
        partial_query = str(escape(request.form.get('partial_query')))
        query_terms = partial_query.lower().split()
        completions = ranker.lookup_query(query_terms)
        response = {'completions': [completion['document'] for completion in completions]}
        return response

    @web_app.route('/predict_term', methods=['POST'])
    def predict_term():
        partial_query = str(escape(request.form.get('partial_query')))
        query_terms = partial_query.lower().split()
        prediction = assistant.predict(query_terms)[0]
        return prediction

    @web_app.route('/correct_term', methods=['POST'])
    def correct_term():
        partial_query = str(escape(request.form.get('partial_query')))
        query_terms = partial_query.lower().split()
        correction = assistant.correct(query_terms)[0]
        return correction

    @web_app.route('/complete_term', methods=['POST'])
    def complete_term():
        partial_query = str(escape(request.form.get('partial_query')))
        query_terms = partial_query.lower().split()
        correction = assistant.complete(query_terms)[0]
        return correction

    @web_app.route('/query', methods=['POST'])
    def query():
        query = str(escape(request.form.get('query', '')))
        query_terms = query.lower().split()
        query_completions = ranker.lookup_query(query_terms)
        query_results = [(
            images_handler.get_url(query_completion['doc_id']),
            query_completion['document'],
            round(query_completion['score'], 4),
        ) for query_completion in query_completions]
        return render_template('query_results.html', query=query, query_results=query_results)

    return web_app


if __name__ == '__main__':
    web_app = create_web_app()
    web_app.run(
        host=config.HOST,
        port=config.PORT,
    )
