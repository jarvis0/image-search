import itertools
from collections import Counter, defaultdict
from typing import DefaultDict, Dict, List, Tuple

from joblib import Parallel, delayed

from .collection import Collection, Document


class Posting:

    def __init__(self, doc_id: int, frequency: int):
        self.__doc_id: int = doc_id
        self.__frequency: int = frequency

    def __repr__(self) -> str:
        return f'(id: {self.__doc_id}, frequency: {self.__frequency})'

    @property
    def doc_id(self) -> int:
        return self.__doc_id

    @property
    def frequency(self) -> int:
        return self.__frequency


class InvertedIndex:

    def __init__(self, collection: Collection):
        self.__collection: Collection = collection
        self.__inv_index: DefaultDict[str, List[Posting]] = defaultdict(list)

    @property
    def items(self) -> List[Tuple[str, List[Posting]]]:
        return list(self.__inv_index.items())

    @staticmethod
    def __index_document(doc_id: int, document: Document):
        term_frequencies: Dict[str, int] = Counter(document.tokens)
        partial_term_postings = [(term, [Posting(doc_id, freq)]) for term, freq in term_frequencies.items()]
        return partial_term_postings

    def index_collection(self):
        map_responses = Parallel(n_jobs=4)(delayed(InvertedIndex.__index_document)(
            doc_id,
            self.__collection.get_document(doc_id),
        ) for doc_id in self.__collection.docs_id)
        for term, postings in itertools.chain(*map_responses):
            self.__inv_index[term] += postings
