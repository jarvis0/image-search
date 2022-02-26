import math
import pickle
from itertools import chain
from os.path import join
from typing import Dict, List, Set

from nltk import ConditionalFreqDist, bigrams, trigrams

from sklearn.feature_extraction.text import TfidfVectorizer

from . import Collection, InvertedIndex
from .indexer import Posting
from ..context import Context


class TermLexicon:

    def __init__(
        self,
        total_frequency: int,
        inverse_term_frequency: float,
        postings: List[Posting],
    ):
        self.__tot_freq: int = total_frequency
        self.__idf: float = inverse_term_frequency
        self.__postings: List[Posting] = postings

    def __repr__(self) -> str:
        return f'$tot_freq: {self.__tot_freq} - idf: {self.__idf} - postings: {self.__postings}$'

    @property
    def tot_freq(self) -> int:
        return self.__tot_freq

    @property
    def idf(self) -> float:
        return self.__idf

    @property
    def postings(self) -> List[Posting]:
        return self.__postings


class Lexicon:

    DUMP_PATH: str = 'binaries/lexicon.pkl'

    def __init__(self, context: Context):
        self.__regex: str = context.regex
        self.__en_stop_terms: Set[str] = context.en_stop_terms
        self.__stop_terms_fraction: float = context.stop_terms_fraction
        self.__lexicon: Dict[str, TermLexicon] = {}
        self.__stop_terms: Set[str]
        self.__unigrams: ConditionalFreqDist
        self.__bigrams: ConditionalFreqDist
        self.__trigrams: ConditionalFreqDist

    @property
    def terms(self) -> List[str]:
        return [*self.__lexicon]

    @property
    def terms_lexicon(self) -> List[TermLexicon]:
        return [*self.__lexicon.values()]

    @property
    def stop_terms(self) -> Set[str]:
        return self.__stop_terms

    def __add_term_lexicon(self, collection_size: int, term: str, postings: List[Posting]):
        self.__lexicon[term] = TermLexicon(
            sum(p.frequency for p in postings),
            math.log((collection_size - len(postings) + 0.5) / (len(postings) + 0.5) + 1),
            postings,
        )

    def __remove_stop_terms(self):
        n_stop_terms = int(self.__stop_terms_fraction * len(self.__lexicon))
        self.__stop_terms = {
            x[0] for x in sorted(
                self.__lexicon.items(),
                key=lambda x: x[1].tot_freq,
                reverse=True,
            )[: n_stop_terms]
        } & self.__en_stop_terms
        for stop_term in self.__stop_terms:
            del self.__lexicon[stop_term]

    def build_lexicon(self, collection: Collection, inv_index: InvertedIndex):
        for term, postings in inv_index.items:
            self.__add_term_lexicon(collection.size, term, postings)
        self.__remove_stop_terms()

    def build_unigrams(self, collection: Collection):
        vectorizer = TfidfVectorizer(
            token_pattern=self.__regex,
            lowercase=False,
            stop_words=self.__stop_terms,
        )
        tfidf_matrix = vectorizer.fit_transform(document.text for document in collection.documents)
        features = vectorizer.get_feature_names_out()
        sums = tfidf_matrix.sum(axis=0)
        self.__unigrams = {term: sums[0, col] for col, term in enumerate(features)}

    def build_bigrams(self, collection: Collection):
        bgs = chain(
            *([
                *bigrams(filter(lambda x: x not in self.__stop_terms, document.tokens)),
            ] for document in collection.documents),
        )
        self.__bigrams = ConditionalFreqDist(bgs)

    def build_trigrams(self, collection: Collection):
        full_tgs = chain(
            *([
                *trigrams(filter(lambda x: x not in self.__stop_terms, document.tokens)),
            ] for document in collection.documents),
        )
        a, b, c = zip(*full_tgs)
        tgs = [*zip(zip(a, b), c)]
        self.__trigrams = ConditionalFreqDist(tgs)

    def predict_from_unigrams(self, term: str) -> Dict[str, float]:
        return {term: self.__unigrams[term]}

    def predict_from_bigrams(self, term: str) -> Dict[str, int]:
        return dict(self.__bigrams[term])

    def predict_from_trigrams(self, term_a: str, term_b: str) -> Dict[str, int]:
        return dict(self.__trigrams[term_a, term_b])

    def get_term_lexicon(self, term: str) -> TermLexicon:
        return self.__lexicon[term]

    def dump(self, root: str):
        with open(join(root, Lexicon.DUMP_PATH), 'wb') as fp:
            pickle.dump(self, fp)


def load_lexicon(root: str) -> Lexicon:
    with open(join(root, Lexicon.DUMP_PATH), 'rb') as fp:
        lexicon = pickle.load(fp)
    return lexicon
