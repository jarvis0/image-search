import re
import time
from typing import Dict, List

import pandas as pd

from .collector import Collection
from .indexer import InvertedIndex


class BM25Plus:

    def __init__(self, collection: Collection, inv_index: InvertedIndex, k1: float = 1.5, b: float = 0.75, delta: float = 1.):
        self.collection: Collection = collection
        self.inv_index: InvertedIndex = inv_index
        self.avgdl: float = sum(x['tot_freq'] for x in self.inv_index.lexicon.values()) / len(self.collection.documents)
        print(self.avgdl)
        self.doc_freqs: List[int] = []
        self.idf: Dict = {}  # TODO
        self.doc_len: List = []  # TODO
        self.k1: float = k1
        self.b: float = b
        self.delta: float = delta

    def lookup_query(self, query):
        query_words = tuple(re.findall(r'\w+', query))
        accumulators = {}
        for w in query_words:
            postings = self.inv_index.lexicon[w]['postings']
            for p in postings:
                accumulators[p.docId] = accumulators.get(p.docId, 0) + p.frequency
        sorted_accumulators = dict(sorted(accumulators.items(), key=lambda x: x[1], reverse=True))
        return [(self.collection.get_document(docId), sorted_accumulators[docId]) for docId in sorted_accumulators][: 5]


if __name__ == '__main__':
    corpus = pd.read_csv('data/captions.tsv', sep='\t', index_col='id')['caption'].to_dict()
    print('number of sentences:', len(corpus))
    tic = time.time()
    collection = Collection(corpus)
    collection.build_collection()
    print('build collection', time.time() - tic)
    tic = time.time()
    inv_index = InvertedIndex(collection)
    inv_index.index_collection()
    print('index collection', time.time() - tic)
    tic = time.time()
    inv_index.build_lexicon()
    print('build lexicon', time.time() - tic)
    print('inv_index entries', len(inv_index.lexicon))
    tic = time.time()
    ranker = BM25Plus(collection, inv_index)
    query = 'football player'
    results = ranker.lookup_query(query)
    print('query', time.time() - tic)
    for text, score in results:
        print(score, text)
