import time

import streamlit as st

from typing_assistant.indexing import load_collection, load_images_handler, load_lexicon
from typing_assistant.ranking import OkapiBM25Ranker


def handle_query():
    print('here is the query:', st.session_state['query'])


if __name__ == '__main__':
    tic = time.time()
    collection = load_collection('binaries/collection.pkl')
    st.text(f'collection loaded in {(time.time() - tic):.2f} seconds')
    tic = time.time()
    lexicon = load_lexicon('binaries/lexicon.pkl')
    st.text(f'lexicon loaded in {(time.time() - tic):.2f} seconds')
    st.text(f'lexicon contains {len(lexicon.get_words_lexicon())} terms')
    tic = time.time()
    images_handler = load_images_handler('binaries/images_handler.pkl')
    st.text(f'images handler loaded in {(time.time() - tic):.2f} seconds')
    ranker = OkapiBM25Ranker(collection, lexicon)

    if 'query' not in st.session_state:
        st.session_state['query'] = ''
    query = st.text_input('query text:', key='query', on_change=handle_query)
    tic = time.time()
    results = ranker.lookup_query(query)
    st.text(f'query executed in {(time.time() - tic):.2f} seconds')
    for _, text, score in results:
        st.text(f'{score:.4f}, {text}')
    tic = time.time()
    # images = images_handler.download_images([doc_id for doc_id, _, _ in results])
    # st.text(f'images downloaded in {(time.time() - tic):.2f}')
    # for i, image in enumerate(images):
    #     st.image(image, caption=results[i][1], output_format='png')
