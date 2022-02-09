import re
from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple

from .query_expander import QueryExpander
from ..context import Context
from ..indexing import Collection, Lexicon


class OkapiBM25Ranker:

    KAPPA: float = 1.5
    BETA: float = 0.75
    REGEX: str = r'\w+'

    def __init__(self, context: Context, collection: Collection, lexicon: Lexicon):
        self.__max_results: int = context.max_results
        self.__collection: Collection = collection
        self.__lexicon: Lexicon = lexicon
        self.__query_expander: QueryExpander = QueryExpander(lexicon)
        self.__avgdl: float = sum(x.tot_freq for x in self.__lexicon.get_words_lexicon()) / self.__collection.size

    def lookup_query(self, query: str) -> List[Tuple[int, str, float]]:
        query_words = list(re.findall(OkapiBM25Ranker.REGEX, query))
        seq_expanded_query_words: Dict[str, float] = self.__query_expander.expand_by_sequence(query_words)
        sem_expanded_query_words: Dict[str, float] = self.__query_expander.expand_by_semantics(query_words)
        expanded_query_words: Dict[str, float] = {**seq_expanded_query_words, **sem_expanded_query_words}
        tf: DefaultDict[str, DefaultDict[int, int]] = defaultdict(lambda: defaultdict(int))
        idf: Dict[str, float] = {}
        for w in expanded_query_words:
            word_lexicon = self.__lexicon.get_word_lexicon(w)
            idf[w] = word_lexicon.idf
            for p in word_lexicon.postings:
                tf[w][p.doc_id] += p.frequency
        scores: DefaultDict[int, float] = defaultdict(int)
        for w, weight in expanded_query_words.items():
            for doc_id in tf[w]:
                scores[doc_id] += weight * idf[w] * ((OkapiBM25Ranker.KAPPA + 1) * tf[w][doc_id] / (
                    tf[w][doc_id] + OkapiBM25Ranker.KAPPA * (
                        1 - OkapiBM25Ranker.BETA + OkapiBM25Ranker.BETA * self.__collection.get_doc_length(doc_id) / self.__avgdl)))
        sorted_results = list(sorted(scores.items(), key=lambda x: x[1], reverse=True))[: self.__max_results]
        return [(doc_id, self.__collection.get_document(doc_id).text, score) for doc_id, score in sorted_results]
