import re
from collections import defaultdict
from typing import List, Tuple

from ..indexing import Collection, Lexicon


class BM25Ranker:

    def __init__(self, collection: Collection, lexicon: Lexicon, kappa: float = 1.5, beta: float = 0.75):
        self.collection: Collection = collection
        self.lexicon: Lexicon = lexicon
        self.kappa: float = kappa
        self.beta: float = beta
        self.avgdl: float = sum(x.tot_freq for x in self.lexicon.get_words_lexicon()) / self.collection.get_size()

    def lookup_query(self, query: str) -> List[Tuple[str, float]]:
        query_words = tuple(re.findall(r'\w+', query))
        tf, idf = defaultdict(lambda: defaultdict(int)), {}
        for w in query_words:
            word_lexicon = self.lexicon.get_word_lexicon(w)
            idf[w] = word_lexicon.idf
            for p in word_lexicon.postings:
                tf[w][p.doc_id] += p.frequency
        scores = defaultdict(int)
        for doc_id in tf[w]:
            for w in query_words:
                scores[doc_id] += idf[w] * ((self.kappa + 1) * tf[w][doc_id] / (
                    tf[w][doc_id] + self.kappa * (1 - self.beta + self.beta * self.collection.get_doc_length(doc_id) / self.avgdl)))
        sorted_results = list(sorted(scores.items(), key=lambda x: x[1], reverse=True))[: 5]
        return [(self.collection.get_document(doc_id), score) for doc_id, score in sorted_results]
