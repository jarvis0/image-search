import re
import time
from collections import defaultdict
from typing import List, Tuple

import pandas as pd

from .collector import Collection
from .indexer import InvertedIndex


class BM25PlusRanker:

    def __init__(self, collection: Collection, inv_index: InvertedIndex, kappa: float = 1.5, beta: float = 0.75, delta: float = 1.):
        self.collection: Collection = collection
        self.inv_index: InvertedIndex = inv_index
        self.kappa: float = kappa
        self.beta: float = beta
        self.delta: float = delta
        self.avgdl: float = sum(x['tot_freq'] for x in self.inv_index.lexicon.values()) / self.collection.n_documents

    def lookup_query(self, query: str) -> List[Tuple[str, float]]:
        query_words = tuple(re.findall(r'\w+', query))
        tf, idf = defaultdict(lambda: defaultdict(int)), {}
        for w in query_words:
            lexicon_entry = self.inv_index.lexicon[w]
            idf[w] = lexicon_entry['idf']
            for p in lexicon_entry['postings']:
                tf[w][p.docId] += p.frequency
        scores = defaultdict(int)
        for docId in tf[w]:
            for w in query_words:
                scores[docId] += idf[w] * (self.delta + ((self.kappa + 1) * tf[w][docId]) / (
                    tf[w][docId] + self.kappa * (1 - self.beta + self.beta * self.collection.get_doc_length(docId) / self.avgdl)))
        sorted_results = list(sorted(scores.items(), key=lambda x: x[1], reverse=True))[: 5]
        return [(self.collection.get_document(docId), score) for docId, score in sorted_results]


if __name__ == '__main__':
    corpus = pd.read_csv('data/captions.tsv', sep='\t', index_col='id')['caption'].iloc[: 8].to_dict()
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
    ranker = BM25PlusRanker(collection, inv_index)
    query = 'basketball player'
    results = ranker.lookup_query(query)
    print('query', time.time() - tic)
    for text, score in results:
        print(score, text)
