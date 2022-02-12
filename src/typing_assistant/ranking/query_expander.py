from collections import Counter, defaultdict
from difflib import SequenceMatcher
from typing import DefaultDict, Dict, List

import fasttext as ft

from ..context import Context
from ..indexing import Lexicon


ft.FastText.eprint = lambda x: None


class QueryExpander:

    SEMANTIC_MODEL_PATH: str = 'binaries/semantic_model.bin'

    def __init__(self, context: Context, lexicon: Lexicon):
        self.__sequencediff_cutoff: float = context.sequencediff_cutoff
        self.__semantic_cutoff: float = context.semantic_cutoff
        self.__n_semantic_neighbors: int = context.n_semantic_neighbors
        self.__terms: List[str] = lexicon.terms
        self.__matcher: SequenceMatcher = SequenceMatcher(isjunk=None, autojunk=False)
        self.__semantic_model: ft.FastText = ft.load_model(QueryExpander.SEMANTIC_MODEL_PATH)

    def expand_by_sequence(self, query_terms: List[str]) -> Dict[str, float]:
        unknown_terms = {*query_terms} - {*self.__terms}
        known_query_terms = [w for w in query_terms if w not in unknown_terms]
        query_expansion: DefaultDict[str, float] = defaultdict(float)
        for q_term in unknown_terms:
            self.__matcher.set_seq2(q_term)
            for term in self.__terms:
                self.__matcher.set_seq1(term)
                if self.__matcher.real_quick_ratio() >= self.__sequencediff_cutoff and \
                   self.__matcher.quick_ratio() >= self.__sequencediff_cutoff and \
                   self.__matcher.ratio() >= self.__sequencediff_cutoff:
                    query_expansion[term] += self.__matcher.ratio()
        query_expansion.update(dict(Counter(known_query_terms)))
        return query_expansion

    def expand_by_semantics(self, query_terms: List[str]) -> Dict[str, float]:
        unknown_terms = {*query_terms} - {*self.__terms}
        known_query_terms = [w for w in query_terms if w not in unknown_terms]
        query_expansion: DefaultDict[str, float] = defaultdict(float)
        for q_term in known_query_terms:
            for confidence, neighbor in self.__semantic_model.get_nearest_neighbors(
                    q_term,
                    k=self.__n_semantic_neighbors,
            ):
                if confidence >= self.__semantic_cutoff and neighbor != '</s>':
                    query_expansion[neighbor] += confidence
        query_expansion.update(dict(Counter(known_query_terms)))
        return query_expansion
