import time

from .config import config
from .indexing import indexes_loader
from .ranking import OkapiBM25Ranker


if __name__ == '__main__':
    collection, lexicon, images_handler = indexes_loader(config.ROOT)
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
