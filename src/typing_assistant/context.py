import json
from typing import Any, Dict

from blessings import Terminal


class Context():

    def __init__(self, config_file: str):
        with open(config_file) as fp:
            self.__configs: Dict[str, Any] = json.load(fp)
        self.__term: Terminal = Terminal()

    @property
    def max_results(self) -> int:
        return self.__configs['max_results']

    @property
    def special_characters(self) -> Dict[str, str]:
        return self.__configs['special_characters']

    @property
    def term(self) -> Terminal:
        return self.__term
