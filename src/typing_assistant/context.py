import json
from os.path import join
from typing import Any, Dict, Set

from blessings import Terminal

import nltk


class Context():

    CONFIG_PATH: str = 'src/typing_assistant/config/configs.json'

    def __init__(self, root: str):
        with open(join(root, Context.CONFIG_PATH)) as fp:
            self.__configs: Dict[str, Any] = json.load(fp)
        self.__term: Terminal = Terminal()

    @property
    def regex(self) -> str:
        return self.__configs['regex']

    @property
    def special_characters(self) -> Dict[str, str]:
        return self.__configs['special_characters']

    @property
    def term(self) -> Terminal:
        return self.__term

    @property
    def en_stop_terms(self) -> Set[str]:
        nltk.download('stopwords', quiet=True)
        return {*nltk.corpus.stopwords.words('english')}

    @property
    def stop_terms_fraction(self) -> float:
        return self.__configs['stop_terms_fraction']

    @property
    def max_completions(self) -> int:
        return self.__configs['max_completions']

    @property
    def max_images(self) -> int:
        return self.__configs['max_images']

    @property
    def sequence_similarity_cutoff(self) -> float:
        return self.__configs['sequence_similarity_cutoff']

    @property
    def max_sequence_similarities(self) -> int:
        return self.__configs['max_sequence_similarities']

    @property
    def semantic_similarity_cutoff(self) -> float:
        return self.__configs['semantic_similarity_cutoff']

    @property
    def max_semantic_similarities(self) -> int:
        return self.__configs['max_semantic_similarities']

    @property
    def max_predictions(self) -> int:
        return self.__configs['max_predictions']

    @property
    def max_corrections(self) -> int:
        return self.__configs['max_corrections']
