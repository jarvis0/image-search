from collections import defaultdict
from difflib import SequenceMatcher
from typing import DefaultDict, Dict, List

import fasttext as ft

from ..context import Context

ft.FastText.eprint = lambda x: None


class SequenceSimilarity():

    @staticmethod
    def merge_dicts(*dicts: Dict[str, float]) -> Dict[str, float]:
        res: DefaultDict[str, float] = defaultdict(float)
        for d in dicts:
            for k, v in d.items():
                res[k] += v
        return {**res}

    def __init__(self, context: Context):
        super().__init__()
        self.__sequence_similarity_cutoff: float = context.sequence_similarity_cutoff
        self.__max_sequence_similarities: int = context.max_sequence_similarities
        self.__sequence_matcher: SequenceMatcher = SequenceMatcher(isjunk=None, autojunk=False)

    def get_nearest_neighbors(
        self,
        reference_term: str,
        terms: List[str],
        term_cutoff: int,
    ) -> Dict[str, float]:
        self.__sequence_matcher.set_seq2(reference_term)
        similar_terms = {}
        for term in terms:
            self.__sequence_matcher.set_seq1(term[: term_cutoff])
            if self.__sequence_matcher.real_quick_ratio() >= self.__sequence_similarity_cutoff and \
                self.__sequence_matcher.quick_ratio() >= self.__sequence_similarity_cutoff and \
                    self.__sequence_matcher.ratio() >= self.__sequence_similarity_cutoff:
                similar_terms[term] = self.__sequence_matcher.ratio()
        most_similar_terms = sorted(
            similar_terms.items(),
            key=lambda x: x[1],
            reverse=True,
        )[: self.__max_sequence_similarities]
        return {term: ratio for term, ratio in most_similar_terms}

    def retrieve_similar_terms(
        self,
        reference_terms: List[str],
        terms: List[str],
        term_cutoff: int = 1000,
    ) -> Dict[str, float]:
        sequence_similar_terms: Dict[str, float] = {}
        for ref_term in reference_terms:
            new_sequence_similar_terms = self.get_nearest_neighbors(ref_term, terms, term_cutoff)
            sequence_similar_terms = SequenceSimilarity.merge_dicts(
                sequence_similar_terms,
                new_sequence_similar_terms,
            )
        return sequence_similar_terms


class SemanticSimilarity():

    SEMANTIC_MODEL_PATH: str = 'binaries/semantic_model.bin'

    def __init__(self, context: Context):
        self.__semantic_similarity_cutoff: float = context.semantic_similarity_cutoff
        self.__max_semantic_similarities: int = context.max_semantic_similarities
        self.__semantic_model: ft.FastText = ft.load_model(SemanticSimilarity.SEMANTIC_MODEL_PATH)

    def retrieve_similar_terms(self, terms: List[str]) -> Dict[str, float]:
        semantic_similar_terms: DefaultDict[str, float] = defaultdict(float)
        for q_term in terms:
            for confidence, neighbor in self.__semantic_model.get_nearest_neighbors(
                    q_term,
                    k=self.__max_semantic_similarities,
            ):
                if confidence >= self.__semantic_similarity_cutoff and neighbor != '</s>':
                    semantic_similar_terms[neighbor] += confidence
        return {**semantic_similar_terms}
