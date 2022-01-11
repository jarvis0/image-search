import time

from .indexing import load_collection, load_lexicon
from .ranking import OkapiBM25Ranker


if __name__ == '__main__':
    tic = time.time()
    collection = load_collection('binaries/collection.pkl')
    print('load collection', time.time() - tic)
    tic = time.time()
    lexicon = load_lexicon('binaries/lexicon.pkl')
    print('load lexicon', time.time() - tic)
    print('lexicon entries', len(lexicon.get_words_lexicon()))

    ranker = OkapiBM25Ranker(collection, lexicon)
    n = 10
    tic = time.time()
    for _ in range(n):
        query = 'vanilla and pink sky at sunset near the beach'
        results = ranker.lookup_query(query)
    print('query', (time.time() - tic) / n)
    for text, score in results:
        print(score, text)
