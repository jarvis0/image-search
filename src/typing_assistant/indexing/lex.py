import math
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from typing import Dict, List, Optional

from .collector import Collection
from .indexer import InvertedIndex, Posting


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

    def __init__(self):
        self.lexicon: Dict[str, WordLexicon] = {}
        self.matcher: Optional[SequenceMatcher] = None
        self.terms: Optional[List[str]] = None

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

    def init_query_mode(self):
        self.matcher = SequenceMatcher(isjunk=None, autojunk=False)

    def expand_query(self, query_words: List[str]) -> List[str]:
        cutoff = 0.8
        exact_words = set(query_words) & set(self.lexicon)
        approx_words = set(query_words) - exact_words
        exact_query_words = [w for w in query_words if w not in approx_words]
        query_expansion = defaultdict(float)
        for q_word in approx_words:
            self.matcher.set_seq2(q_word)
            for term in self.lexicon:
                self.matcher.set_seq1(term)
                if self.matcher.real_quick_ratio() >= cutoff and \
                   self.matcher.quick_ratio() >= cutoff and \
                   self.matcher.ratio() >= cutoff:
                    query_expansion[term] += self.matcher.ratio()
        query_expansion.update(dict(Counter(exact_query_words)))
        return query_expansion
