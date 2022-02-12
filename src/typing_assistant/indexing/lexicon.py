import math
import pickle
from os.path import join
from typing import Dict, List

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
        self.__lexicon: Dict[str, TermLexicon] = {}

    @property
    def terms(self) -> List[str]:
        return [*self.__lexicon.keys()]

    @property
    def terms_lexicon(self) -> List[TermLexicon]:
        return [*self.__lexicon.values()]

    def __add_term_lexicon(self, collection_size: int, term: str, postings: List[Posting]):
        self.__lexicon[term] = TermLexicon(
            sum(p.frequency for p in postings),
            math.log((collection_size - len(postings) + 0.5) / (len(postings) + 0.5) + 1),
            postings,
        )

    def build_lexicon(self, collection: Collection, inv_index: InvertedIndex):
        for term, postings in inv_index.items:
            self.__add_term_lexicon(collection.size, term, postings)

    def get_term_lexicon(self, term: str) -> TermLexicon:
        return self.__lexicon[term]

    def dump(self, root: str):
        with open(join(root, Lexicon.DUMP_PATH), 'wb') as fp:
            pickle.dump(self, fp)


def load_lexicon(root: str) -> Lexicon:
    with open(join(root, Lexicon.DUMP_PATH), 'rb') as fp:
        lexicon = pickle.load(fp)
    return lexicon
