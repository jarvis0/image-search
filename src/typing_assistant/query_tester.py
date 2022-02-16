import time

from .config import config
from .context import Context
from .indexing.indexes_loader import load_indexes
from .ranking import OkapiBM25Ranker


if __name__ == '__main__':
    context = Context(config.ROOT)
    collection, lexicon, images_handler = load_indexes(config.ROOT)
    ranker = OkapiBM25Ranker(context, collection, lexicon)

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
    captions = [caption for _, caption, _ in results]
    images_captions = [*zip(images, captions)]
    images_handler.draw_images(images_captions)
    print('draw images', time.time() - tic)
