import re
from typing import Dict, List, Optional


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

    def get_length(self):
        return self.length


class Collection:

    def __init__(self):
        self.documents: Dict[int, Document] = {}
        self.docs_id: List[int] = None
        self.n_documents: int = 0

    def __add_document(self, doc_id: str, text: str):
        document = Document(text)
        document.tokenize_text()
        self.documents[doc_id] = document

    def build_collection(self, corpus: Dict[int, str]):
        for doc_id in corpus:
            self.__add_document(doc_id, corpus[doc_id])
        self.n_documents = len(self.documents)
        self.docs_id = list(self.documents.keys())

    def get_docs_id(self) -> List[int]:
        return self.docs_id

    def get_document(self, doc_id: str) -> Document:
        return self.documents[doc_id]

    def get_size(self) -> int:
        return self.n_documents

    def get_doc_length(self, doc_id: str) -> int:
        return self.documents[doc_id].get_length()
