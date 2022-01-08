from collections import Counter, defaultdict
from typing import DefaultDict, List, Tuple

from .collector import Collection


class Posting:

    def __init__(self, doc_id: str, frequency: int):
        self.doc_id: str = doc_id
        self.frequency: int = frequency

    def __repr__(self) -> str:
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

    def get_items(self) -> List[Tuple[str, List[Posting]]]:
        return self.index.items()
