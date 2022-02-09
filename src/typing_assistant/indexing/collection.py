import pickle
import re
from os.path import join
from typing import Dict, List


class Document:

    REGEX: str = r'\w+'

    def __init__(self, text: str):
        self.__text: str = text
        self.__tokens: List[str]
        self.__length: int

    def __repr__(self) -> str:
        return self.__text

    @property
    def text(self) -> str:
        return self.__text

    @property
    def tokens(self) -> List[str]:
        return self.__tokens

    @property
    def length(self) -> int:
        return self.__length

    def tokenize_text(self):
        self.__tokens = tuple(re.findall(Document.REGEX, self.__text))
        self.__length = len(self.__tokens)


class Collection:

    DUMP_PATH: str = 'binaries/collection.pkl'

    def __init__(self):
        self.__documents: Dict[int, Document] = {}
        self.__docs_id: List[int]
        self.__n_documents: int

    @property
    def docs_id(self) -> List[int]:
        return self.__docs_id

    @property
    def size(self) -> int:
        return self.__n_documents

    def __add_document(self, doc_id: int, text: str):
        document = Document(text)
        document.tokenize_text()
        self.__documents[doc_id] = document

    def get_document(self, doc_id: int) -> Document:
        return self.__documents[doc_id]

    def get_doc_length(self, doc_id: int) -> int:
        return self.__documents[doc_id].length

    def build_collection(self, corpus: Dict[int, str]):
        for doc_id in corpus:
            self.__add_document(doc_id, corpus[doc_id])
        self.__n_documents = len(self.__documents)
        self.__docs_id = list(self.__documents.keys())

    def dump(self, root: str):
        with open(join(root, Collection.DUMP_PATH), 'wb') as fp:
            pickle.dump(self, fp)


def load_collection(root: str) -> Collection:
    with open(join(root, Collection.DUMP_PATH), 'rb') as fp:
        collection = pickle.load(fp)
    return collection
