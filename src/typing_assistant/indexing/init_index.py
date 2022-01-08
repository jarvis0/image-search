import pickle
import time

import pandas as pd

from .collector import Collection
from .indexer import InvertedIndex
from .lex import Lexicon


if __name__ == '__main__':
    corpus = pd.read_csv('data/raw/all_captions.tsv', sep='\t', index_col='id')['caption'].to_dict()
    print('number of sentences:', len(corpus))
    tic = time.time()
    collection = Collection()
    collection.build_collection(corpus)
    print('build collection', time.time() - tic)
    tic = time.time()
    inv_index = InvertedIndex(collection)
    inv_index.index_collection()
    print('build index', time.time() - tic)
    tic = time.time()
    lexicon = Lexicon()
    lexicon.build_lexicon(collection, inv_index)
    print('build lexicon', time.time() - tic)

    print('lexicon entries', len(lexicon.get_words_lexicon()))
    tic = time.time()
    with open('data/dumps/collection.pkl', 'wb') as fp:
        pickle.dump(collection, fp)
    print('dump collection', time.time() - tic)
    tic = time.time()
    with open('data/dumps/lexicon.pkl', 'wb') as fp:
        pickle.dump(lexicon, fp)
    print('dump lexicon', time.time() - tic)
