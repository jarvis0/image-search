import pickle
import time

from .ranking import BM25Ranker


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

    tic = time.time()
    ranker = BM25Ranker(collection, lexicon)
    query = 'basketball player'
    results = ranker.lookup_query(query)
    print('query', time.time() - tic)
    for text, score in results:
        print(score, text)
