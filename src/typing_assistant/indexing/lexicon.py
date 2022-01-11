import math
import pickle
from typing import Dict, List

from . import Collection, InvertedIndex
from .indexer import Posting


class WordLexicon:

    def __init__(
        self,
        total_frequency: int,
        inverse_term_frequency: float,
        postings: List[Posting],
    ):
        self.tot_freq: int = total_frequency
        self.idf: float = inverse_term_frequency
        self.postings: List[Posting] = postings

    def __repr__(self) -> str:
        return f'$tot_freq: {self.tot_freq} - idf: {self.idf} - postings: {self.postings}$'


class Lexicon:

    DUMP_PATH: str = 'binaries/lexicon.pkl'

    def __init__(self):
        self.lexicon: Dict[str, WordLexicon] = {}

    def dump(self):
        with open(Lexicon.DUMP_PATH, 'wb') as fp:
            pickle.dump(self, fp)

    def __add_word_lexicon(self, collection_size: int, term: str, postings: List[Posting]):
        self.lexicon[term] = WordLexicon(
            sum(p.frequency for p in postings),
            math.log((collection_size - len(postings) + 0.5) / (len(postings) + 0.5) + 1),
            postings,
        )

    def build_lexicon(self, collection: Collection, inv_index: InvertedIndex):
        collection_size = collection.get_size()
        for term, postings in inv_index.get_items():
            self.__add_word_lexicon(collection_size, term, postings)

    def get_words_lexicon(self) -> List[WordLexicon]:
        return self.lexicon.values()

    def get_word_lexicon(self, word: str) -> WordLexicon:
        return self.lexicon[word]

    def get_terms(self) -> List[str]:
        return self.lexicon.keys()


def load_lexicon(lexicon_dump_path) -> Lexicon:
    with open(lexicon_dump_path, 'rb') as fp:
        lexicon = pickle.load(fp)
    return lexicon
