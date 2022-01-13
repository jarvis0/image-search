import time

from .indexing import load_collection, load_images_handler, load_lexicon
from .ranking import OkapiBM25Ranker


if __name__ == '__main__':
    tic = time.time()
    collection = load_collection('binaries/collection.pkl')
    print('load collection', time.time() - tic)
    tic = time.time()
    lexicon = load_lexicon('binaries/lexicon.pkl')
    print('load lexicon', time.time() - tic)
    print('lexicon entries', len(lexicon.get_words_lexicon()))
    tic = time.time()
    images_handler = load_images_handler('binaries/images_handler.pkl')
    print('load images handler', time.time() - tic)

    ranker = OkapiBM25Ranker(collection, lexicon)
    n = 1
    tic = time.time()
    for _ in range(n):
        query = 'vanilla and pink sky at sunset near the beach'
        results = ranker.lookup_query(query)
    print('query', (time.time() - tic) / n)
    for _, text, score in results:
        print(score, text)
    tic = time.time()
    images = images_handler.download_images([doc_id for doc_id, _, _ in results])
    print('download images', time.time() - tic)
    tic = time.time()
    images_handler.draw_images(images)
    print('draw images', time.time() - tic)
