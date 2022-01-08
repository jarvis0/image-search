import pickle
import time

from .ranking import OkapiBM25Ranker


if __name__ == '__main__':
    tic = time.time()
    with open('data/dumps/collection.pkl', 'rb') as fp:
        collection = pickle.load(fp)
    print('load collection', time.time() - tic)
    tic = time.time()
    with open('data/dumps/lexicon.pkl', 'rb') as fp:
        lexicon = pickle.load(fp)
    print('load lexicon', time.time() - tic)
    print('lexicon entries', len(lexicon.get_words_lexicon()))

    lexicon.init_query_mode()
    ranker = OkapiBM25Ranker(collection, lexicon)
    n = 10
    tic = time.time()
    for _ in range(n):
        query = 'runnig ftball player in a field'
        results = ranker.lookup_query(query)
    print('query', (time.time() - tic) / n)
    for text, score in results:
        print(score, text)
