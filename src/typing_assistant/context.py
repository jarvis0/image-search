import json
from multiprocessing import Pool
from typing import Any, Dict

from blessings import Terminal


class Context():

    def __init__(self, config_file: str):
        with open(config_file) as fp:
            self.__configs = json.load(fp)
        self.__pool = Pool(self.__configs['num_jobs'])
        self.__term = Terminal()

    @property
    def configs(self) -> Dict[str, Any]:
        return self.__configs

    @property
    def special_characters(self) -> Dict[str, str]:
        return self.__configs['special_characters']

    @property
    def pool(self) -> Pool:
        return self.__pool

    @property
    def term(self) -> Terminal:
        return self.__term
