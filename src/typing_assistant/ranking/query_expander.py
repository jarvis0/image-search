from collections import Counter, defaultdict
from difflib import SequenceMatcher
from typing import DefaultDict, Dict, List

import fasttext as ft

from ..indexing import Lexicon


ft.FastText.eprint = lambda x: None


class QueryExpander:

    MATCHER_CUTOFF: float = 0.8
    SEMANTIC_MODEL_PATH: str = 'binaries/semantic_model.bin'
    N_SEMANTIC_NEIGHBORS: int = 1
    SEMANTIC_CUTOFF: float = 0.7

    def __init__(self, lexicon: Lexicon):
        self.terms: List[str] = lexicon.get_terms()
        self.matcher: SequenceMatcher = SequenceMatcher(isjunk=None, autojunk=False)
        self.semantic_model: ft.FastText = ft.load_model(QueryExpander.SEMANTIC_MODEL_PATH)

    def expand_by_sequence(self, query_words: List[str]) -> Dict[str, float]:
        unknown_words = set(query_words) - set(self.terms)
        known_query_words = [w for w in query_words if w not in unknown_words]
        query_expansion: DefaultDict[str, float] = defaultdict(float)
        for q_word in unknown_words:
            self.matcher.set_seq2(q_word)
            for term in self.terms:
                self.matcher.set_seq1(term)
                if self.matcher.real_quick_ratio() >= QueryExpander.MATCHER_CUTOFF and \
                   self.matcher.quick_ratio() >= QueryExpander.MATCHER_CUTOFF and \
                   self.matcher.ratio() >= QueryExpander.MATCHER_CUTOFF:
                    query_expansion[term] += self.matcher.ratio()
        query_expansion.update(dict(Counter(known_query_words)))
        return query_expansion

    def expand_by_semantics(self, query_words: List[str]) -> Dict[str, float]:
        unknown_words = set(query_words) - set(self.terms)
        known_query_words = [w for w in query_words if w not in unknown_words]
        query_expansion: DefaultDict[str, float] = defaultdict(float)
        for q_word in known_query_words:
            for confidence, neighbor in self.semantic_model.get_nearest_neighbors(
                    q_word,
                    k=QueryExpander.N_SEMANTIC_NEIGHBORS,
            ):
                if confidence >= QueryExpander.SEMANTIC_CUTOFF and neighbor != '</s>':
                    query_expansion[neighbor] += confidence
        query_expansion.update(dict(Counter(known_query_words)))
        return query_expansion
