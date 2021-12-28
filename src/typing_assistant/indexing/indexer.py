import math
from collections import Counter
from typing import Dict, List, Optional, Union

from .collector import Collection


class Posting:

    def __init__(self, docId: str, frequency: int):
        self.docId: str = docId
        self.frequency: int = frequency

    def __repr__(self):
        return '(id: ' + str(self.docId) + ', frequency: ' + str(self.frequency) + ')'


class InvertedIndex:

    def __init__(self, collection: Collection):
        self.collection: Collection = collection
        self.collection_size: int = len(self.collection.documents)
        self.index: Optional[Dict[str, List[Posting]]] = dict.fromkeys(self.collection.unique_tokens, [])
        self.lexicon: Dict[str, Dict[str, Union[int, Posting]]] = None

    def __index_document(self, docId: str):
        document = self.collection.get_document(docId)
        term_frequencies = Counter(document.tokens)
        update_dict = {term: self.index[term] + [Posting(docId, freq)] for term, freq in term_frequencies.items()}
        self.index.update(update_dict)

    def index_collection(self):
        for docId in self.collection.docIds:
            self.__index_document(docId)

    def build_lexicon(self):
        self.lexicon = {
            term: {
                'n_docs': len(postings),
                'tot_freq': sum(p.frequency for p in postings),
                'idf': math.log((self.collection_size + 1) / len(postings)),
                'postings': postings,
            }
            for term, postings in self.index.items()
        }
        self.index = None
