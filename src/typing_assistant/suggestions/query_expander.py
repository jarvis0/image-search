from collections import Counter
from typing import Dict, List, Set

from .text_similarities import SemanticSimilarity, SequenceSimilarity
from ..context import Context
from ..indexing import Lexicon


class QueryExpander:

    def __init__(self, context: Context, lexicon: Lexicon):
        self.__terms: List[str] = lexicon.terms
        self.__stop_terms: Set[str] = lexicon.stop_terms
        self.__sequence_similarity: SequenceSimilarity = SequenceSimilarity(context)
        self.__semantic_similarity: SemanticSimilarity = SemanticSimilarity(context)

    def expand_by_sequence(self, query_terms: List[str]) -> Dict[str, float]:
        filtered_query_terms = {*query_terms} - self.__stop_terms
        unknown_terms = filtered_query_terms - {*self.__terms}
        known_query_terms = [w for w in filtered_query_terms if w not in unknown_terms]
        query_expansion = self.__sequence_similarity.retrieve_similar_terms([*unknown_terms], self.__terms)
        query_expansion.update(dict(Counter(known_query_terms)))
        return query_expansion

    def expand_by_semantics(self, query_terms: List[str]) -> Dict[str, float]:
        filtered_query_terms = {*query_terms} - self.__stop_terms
        unknown_terms = filtered_query_terms - {*self.__terms}
        known_query_terms = [w for w in filtered_query_terms if w not in unknown_terms]
        query_expansion = self.__semantic_similarity.retrieve_similar_terms(known_query_terms)
        query_expansion.update(dict(Counter(known_query_terms)))
        return query_expansion
