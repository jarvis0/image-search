import itertools
from collections import Counter, defaultdict
from typing import DefaultDict, List, Tuple

from joblib import Parallel, delayed

from . import Collection


class Posting:

    def __init__(self, doc_id: int, frequency: int):
        self.doc_id: int = doc_id
        self.frequency: int = frequency

    def __repr__(self) -> str:
        return f'(id: {self.doc_id}, frequency: {self.frequency})'


class InvertedIndex:

    def __init__(self, collection: Collection):
        self.collection: Collection = collection
        self.inv_index: DefaultDict[str, List[Posting]] = defaultdict(list)

    @staticmethod
    def __index_document(doc_id, document):
        term_frequencies = Counter(document.tokens)
        partial_term_postings = [(term, [Posting(doc_id, freq)]) for term, freq in term_frequencies.items()]
        return partial_term_postings

    def index_collection(self):
        map_responses = Parallel(n_jobs=4)(delayed(InvertedIndex.__index_document)(
            doc_id,
            self.collection.get_document(doc_id),
        ) for doc_id in self.collection.get_docs_id())
        for term, postings in itertools.chain(*map_responses):
            self.inv_index[term] += postings

    def get_items(self) -> List[Tuple[str, List[Posting]]]:
        return self.inv_index.items()
