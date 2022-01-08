import math
from collections import Counter, defaultdict
from typing import DefaultDict, Dict, List

from .collector import Collection


class Posting:

    def __init__(self, doc_id: str, frequency: int):
        self.doc_id: str = doc_id
        self.frequency: int = frequency

    def __repr__(self):
        return f'(id: {self.doc_id}, frequency: {self.frequency})'


class InvertedIndex:

    def __init__(self, collection: Collection):
        self.collection: Collection = collection
        self.index: DefaultDict[str, List[Posting]] = defaultdict(list)

    def __index_document(self, doc_id: str):
        document = self.collection.get_document(doc_id)
        term_frequencies = Counter(document.tokens)
        update_dict = {term: self.index[term] + [Posting(doc_id, freq)] for term, freq in term_frequencies.items()}
        self.index.update(update_dict)

    def index_collection(self):
        for doc_id in self.collection.get_docs_id():
            self.__index_document(doc_id)

    def build_lexicon(self):
        collection_size = self.collection.get_size()
        lexicon = Lexicon()
        lexicon.build_lexicon(collection_size, self.index)
        return lexicon


class WordLexicon:

    def __init__(self, total_frequency: int, inverse_term_frequency: float, postings: List[Posting]):
        self.tot_freq: int = total_frequency
        self.idf: float = inverse_term_frequency
        self.postings: List[Posting] = postings

    def __repr__(self):
        return f'$tot_freq: {self.tot_freq} - idf: {self.idf} - postings: {self.postings}$'


class Lexicon:

    def __init__(self):
        self.lexicon: Dict[str, WordLexicon] = {}

    def __add_word_lexicon(self, collection_size: int, term: str, postings: List[Posting]):
        self.lexicon[term] = WordLexicon(
            sum(p.frequency for p in postings),
            math.log((collection_size + 1) / len(postings)),
            postings,
        )

    def build_lexicon(self, collection_size: int, inv_index: InvertedIndex):
        for term, postings in inv_index.items():
            self.__add_word_lexicon(collection_size, term, postings)

    def get_words_lexicon(self):
        return self.lexicon.values()

    def get_word_lexicon(self, word: str) -> WordLexicon:
        return self.lexicon[word]
