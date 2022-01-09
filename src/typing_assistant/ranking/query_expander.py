from collections import Counter, defaultdict
from difflib import SequenceMatcher
from typing import List

from ..indexing import Lexicon


class QueryExpander:

    def __init__(self, lexicon: Lexicon):
        self.terms: List[str] = lexicon.get_terms()
        self.matcher: SequenceMatcher = SequenceMatcher(isjunk=None, autojunk=False)

    def expand_query(self, query_words: List[str]) -> List[str]:
        cutoff = 0.8
        known_words = set(query_words) & set(self.terms)
        unknown_words = set(query_words) - known_words
        known_query_words = [w for w in query_words if w not in unknown_words]
        query_expansion = defaultdict(float)
        for q_word in unknown_words:
            self.matcher.set_seq2(q_word)
            for term in self.terms:
                self.matcher.set_seq1(term)
                if self.matcher.real_quick_ratio() >= cutoff and \
                   self.matcher.quick_ratio() >= cutoff and \
                   self.matcher.ratio() >= cutoff:
                    query_expansion[term] += self.matcher.ratio()
        query_expansion.update(dict(Counter(known_query_words)))
        return query_expansion
