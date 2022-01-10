import pickle
import time

from .ranking import OkapiBM25Ranker


if __name__ == '__main__':
    tic = time.time()
    with open('binaries/collection.pkl', 'rb') as fp:
        collection = pickle.load(fp)
    print('load collection', time.time() - tic)
    tic = time.time()
    with open('binaries/lexicon.pkl', 'rb') as fp:
        lexicon = pickle.load(fp)
    print('load lexicon', time.time() - tic)
    print('lexicon entries', len(lexicon.get_words_lexicon()))

    ranker = OkapiBM25Ranker(collection, lexicon)
    n = 10
    tic = time.time()
    for _ in range(n):
        query = 'running football player player in field across football'
        results = ranker.lookup_query(query)
    print('query', (time.time() - tic) / n)
    for text, score in results:
        print(score, text)
