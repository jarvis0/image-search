from typing import Dict, List

from .text_similarities import SequenceSimilarity
from ..context import Context
from ..indexing import Lexicon


class TypingAssistant():

    def __init__(self, context: Context, lexicon: Lexicon):
        self.__max_predictions: int = context.max_predictions
        self.__max_corrections: int = context.max_corrections
        self.__lexicon: Lexicon = lexicon
        self.__terms: List[str] = lexicon.terms
        self.__sequence_similarity: SequenceSimilarity = SequenceSimilarity(context)

    def predict(self, query_terms: List[str]) -> List[Dict[str, str]]:
        predictions = {}
        if len(query_terms) >= 2:
            predictions = self.__lexicon.predict_from_trigrams(query_terms[-2], query_terms[-1])
        if len(query_terms) >= 1 and len(predictions) == 0:
            predictions = self.__lexicon.predict_from_bigrams(query_terms[-1])
        suggestions = []
        if len(predictions) >= 1:
            sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
            term_predictions = [term for term, _ in sorted_predictions[: self.__max_predictions]]
            suggestions = [{'next_term': term} for term in term_predictions][: self.__max_predictions]
        suggestions.append({})
        return suggestions

    def correct(self, query_terms: List[str]) -> List[Dict[str, str]]:
        known_term = {query_terms[-1]} & {*self.__terms}
        sequence_similar_terms = self.__sequence_similarity.retrieve_similar_terms([query_terms[-1]], self.__terms)
        candidates = known_term or {*sequence_similar_terms}

        corrections = []
        if len(query_terms) >= 3:
            trigrams = self.__lexicon.predict_from_trigrams(query_terms[-3], query_terms[-2])
            selected_candidates = candidates & {*trigrams}
            if bool(selected_candidates):
                corrections = sorted(selected_candidates, key=lambda x: trigrams[x], reverse=True)
        if len(query_terms) >= 2 and len(corrections) == 0:
            bigrams = self.__lexicon.predict_from_bigrams(query_terms[-2])
            selected_candidates = candidates & {*bigrams}
            if bool(selected_candidates):
                corrections = sorted(selected_candidates, key=lambda x: bigrams[x], reverse=True)
        if len(corrections) == 0 and len(candidates) >= 1:
            corrections = sorted(
                candidates,
                key=lambda x: [*self.__lexicon.predict_from_unigrams(x).values()][0],
                reverse=True,
            )

        suggestions = []
        if len(corrections) >= 1:
            suggestions = [
                {'correct_term': correction, 'wrong_term': query_terms[-1]}
                for correction in corrections
                if correction != query_terms[-1]
            ][: self.__max_corrections]
        suggestions.append({})
        return suggestions

    # def complete(self, input_terms: tuple) -> dict:
    #    bi_grams, tri_grams = [], []
    #    if len(input_terms) >= 3:
    #        tri_grams = self.__tgs_freq[input_terms[-3], input_terms[-2]]
    #    elif len(input_terms) == 2:
    #        bi_grams = self.__bgs_freq[input_terms[-2]]
    #    candidates = tri_grams or bi_grams or self.__ugs_freq
    #    candidates = dict(candidates)

    #    term_cutoff = len(input_terms[-1]) + 1
    #    selected_candidates = {}
    #    for candidate, candidate_freq in candidates.items():
    #        similarity_score = levenshtein_similarity(input_terms[-1], candidate[: term_cutoff])
    #        if similarity_score >= self.__configs['term_completion_threshold']:
    #            selected_candidates[candidate] = similarity_score

    #    predictions = []
    #    if len(selected_candidates) > 0:
    #        selected_candidates = dict(sorted(selected_candidates.items(), key=lambda x: x[1], reverse=True))
    #        predictions = tuple(selected_candidates.keys())

    #    suggestion = {}
    #    if len(predictions) >= 1 and predictions[0] != input_terms[-1]:
    #        suggestion = {'complete_term': predictions[0], 'incomplete_term': input_terms[-1]}
    #    return suggestion
