import json
from os.path import join
from typing import Any, Dict

from blessings import Terminal


class Context():

    CONFIG_PATH: str = 'src/typing_assistant/config/configs.json'

    def __init__(self, root: str):
        with open(join(root, Context.CONFIG_PATH)) as fp:
            self.__configs: Dict[str, Any] = json.load(fp)
        self.__term: Terminal = Terminal()

    @property
    def special_characters(self) -> Dict[str, str]:
        return self.__configs['special_characters']

    @property
    def term(self) -> Terminal:
        return self.__term

    @property
    def max_completions(self) -> int:
        return self.__configs['max_completions']

    @property
    def max_images(self) -> int:
        return self.__configs['max_images']

    @property
    def sequencediff_cutoff(self) -> float:
        return self.__configs['sequencediff_cutoff']

    @property
    def semantic_cutoff(self) -> float:
        return self.__configs['semantic_cutoff']

    @property
    def n_semantic_neighbors(self) -> int:
        return self.__configs['n_semantic_neighbors']
