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

    def expand_by_sequence(self, query_words: List[str]) -> Dict[str, float]:
        unknown_words = {*query_words} - {*self.__terms}
        known_query_words = [w for w in query_words if w not in unknown_words]
        query_expansion: DefaultDict[str, float] = defaultdict(float)
        for q_word in unknown_words:
            self.__matcher.set_seq2(q_word)
            for term in self.__terms:
                self.__matcher.set_seq1(term)
                if self.__matcher.real_quick_ratio() >= self.__sequencediff_cutoff and \
                   self.__matcher.quick_ratio() >= self.__sequencediff_cutoff and \
                   self.__matcher.ratio() >= self.__sequencediff_cutoff:
                    query_expansion[term] += self.__matcher.ratio()
        query_expansion.update(dict(Counter(known_query_words)))
        return query_expansion

    def expand_by_semantics(self, query_words: List[str]) -> Dict[str, float]:
        unknown_words = {*query_words} - {*self.__terms}
        known_query_words = [w for w in query_words if w not in unknown_words]
        query_expansion: DefaultDict[str, float] = defaultdict(float)
        for q_word in known_query_words:
            for confidence, neighbor in self.__semantic_model.get_nearest_neighbors(
                    q_word,
                    k=self.__n_semantic_neighbors,
            ):
                if confidence >= self.__semantic_cutoff and neighbor != '</s>':
                    query_expansion[neighbor] += confidence
        query_expansion.update(dict(Counter(known_query_words)))
        return query_expansion
