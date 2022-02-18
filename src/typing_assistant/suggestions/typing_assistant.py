from difflib import SequenceMatcher
from typing import Dict, List

from ..context import Context
from ..indexing import Lexicon


class TypingAssistant():

    def __init__(self, context: Context, lexicon: Lexicon):
        self.__max_predictions: int = context.max_predictions
        self.__max_corrections: int = context.max_corrections
        self.__lexicon: Lexicon = lexicon
        self.__sequencediff_cutoff = context.sequencediff_cutoff
        self.__matcher: SequenceMatcher = SequenceMatcher(isjunk=None, autojunk=False)

    def predict(self, query_terms: List[str]) -> List[Dict]:
        predictions = {}
        if len(query_terms) >= 2:
            predictions = self.__lexicon.predict_from_trigrams(query_terms[-2], query_terms[-1])
        if len(query_terms) == 1 or len(predictions) == 0:
            predictions = self.__lexicon.predict_from_bigrams(query_terms[-1])
        suggestions: List[Dict] = [{}]
        if len(predictions) >= 1:
            sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
            term_predictions = [term for term, _ in sorted_predictions[: self.__max_predictions]]
            suggestions = [{'next_term': term} for term in term_predictions][: self.__max_predictions]
        return suggestions

    def correct(self, query_terms: List[str]) -> List[Dict]:
        known_terms = []
        if query_terms[-1] in self.__lexicon.terms:
            known_terms = [query_terms[-1]]
        self.__matcher.set_seq2(query_terms[-1])
        seqdiff_similar_terms = []
        for term in self.__lexicon.terms:
            self.__matcher.set_seq1(term)
            if self.__matcher.real_quick_ratio() >= self.__sequencediff_cutoff and \
               self.__matcher.quick_ratio() >= self.__sequencediff_cutoff and \
               self.__matcher.ratio() >= self.__sequencediff_cutoff:
                seqdiff_similar_terms.append(term)
        candidates = set(known_terms or seqdiff_similar_terms)  # TODO: check usefulness of known_terms

        corrections = []
        if len(query_terms) >= 3:
            trigrams = self.__lexicon.predict_from_trigrams(query_terms[-3], query_terms[-2])
            selected_candidates = candidates & set(trigrams)
            if bool(selected_candidates):
                corrections = list(selected_candidates)
                corrections.sort(key=lambda x: trigrams[x], reverse=True)
        elif len(query_terms) == 2:
            bigrams = self.__lexicon.predict_from_bigrams(query_terms[-2])
            selected_candidates = candidates & set(bigrams)
            if bool(selected_candidates):
                corrections = list(selected_candidates)
                corrections.sort(key=lambda x: bigrams[x], reverse=True)
        if len(corrections) == 0 and len(candidates) >= 1:
            corrections = list(candidates)
            corrections.sort(
                key=lambda x: list(self.__lexicon.predict_from_unigrams(x).values())[0],
                reverse=True,
            )

        suggestions: List[Dict] = [{}]
        if len(corrections) >= 1 and corrections[0] != query_terms[-1]:
            suggestions = [
                {'correct_term': correction, 'wrong_term': query_terms[-1]}
                for correction in corrections
            ][: self.__max_corrections]
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
