import re
from typing import Dict, List, Optional, Set, Union


class Document:

    def __init__(self, text: str):
        self.text: str = text
        self.tokens: Optional[List[str]] = None
        self.length: Optional[int] = None

    def __repr__(self):
        return self.text

    def tokenize_text(self):
        self.tokens = tuple(re.findall(r'\w+', self.text))
        self.length = len(self.tokens)


class Collection:

    def __init__(self, corpus: Dict[int, str]):
        self.corpus: Optional[Dict[int, str]] = corpus
        self.docIds: List[int] = list(self.corpus.keys())
        self.documents: Dict[int, Document] = {}
        self.unique_tokens: Union[Set[str], List[str]] = set()

    def __add_document(self, docId: str, text: str):
        document = Document(text)
        document.tokenize_text()
        self.unique_tokens.update(document.tokens)
        self.documents[docId] = document

    def build_collection(self):
        for docId in self.docIds:
            self.__add_document(docId, self.corpus[docId])
        self.corpus = None
        self.unique_tokens = sorted(list(self.unique_tokens))

    def get_document(self, docId: str) -> Document:
        return self.documents[docId]
