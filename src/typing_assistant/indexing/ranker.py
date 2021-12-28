from collections import defaultdict
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
        self.doc_freqs: List[int] = []  # TODO
        self.idf: Dict = {}  # TODO
        self.doc_len: List = []  # TODO
        self.k1: float = k1
        self.b: float = b
        self.delta: float = delta

    def lookup_query(self, query):
        query_words = tuple(re.findall(r'\w+', query))
        tf, idf = defaultdict(lambda: defaultdict(int)), {}
        for w in query_words:
            lexicon_entry = self.inv_index.lexicon[w]
            idf[w] = lexicon_entry['idf']
            for p in lexicon_entry['postings']:
                tf[w][p.docId] += p.frequency
        scores = defaultdict(int)
        for w in query_words:
            for docId in tf[w]:
                scores[docId] += ((self.k1 + 1) * tf[w][docId]) / (tf[w][docId] + self.k1 * (1 - self.b + self.b * self.collection.get_document(docId).length / self.avgdl)) * idf[w]
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
        return [(self.collection.get_document(docId), sorted_scores[docId]) for docId in sorted_scores][: 5]


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
