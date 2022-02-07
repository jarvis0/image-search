from typing import Any, Dict, List
from blessings import Terminal

import getch

from .config import config
from .context import Context
from .indexing.images_handler import ImagesHandler
from .indexing.indexes_loader import load_indexes
from .ranking import OkapiBM25Ranker


class CLIApp():

    @staticmethod
    def acquire_input_char() -> str:
        return getch.getch()

    @staticmethod
    def init_suggestions() -> dict:
        return {
            'query_completion': {},
            'word_correction': {},
            'word_prediction': {},
            'word_completion': {},
        }

    @staticmethod
    def replace_from_right(query: str, old_word: str, new_word: str) -> str:
        return new_word.join(query.rsplit(old_word, 1))

    @staticmethod
    def apply_suggestion(query: str, suggestions: Dict[str, Any]) -> str:
        if bool(suggestions['word_correction']):
            query = CLIApp.replace_from_right(
                query,
                suggestions['word_correction']['wrong_word'],
                suggestions['word_correction']['right_word'],
            )
        elif bool(suggestions['word_prediction']):
            query += suggestions['word_prediction']['next_word']
        elif bool(suggestions['word_completion']):
            query = CLIApp.replace_from_right(
                query,
                suggestions['word_completion']['incomplete_word'],
                suggestions['word_completion']['complete_word'],
            )
        return query

    def __init__(self, ctx: Context):
        self.__term: Terminal = ctx.term
        self.__special_characters: Dict[str, Any] = ctx.special_characters
        collection, lexicon, images_handler = load_indexes(config.ROOT)
        self.__ranker: OkapiBM25Ranker = OkapiBM25Ranker(collection, lexicon)
        self.__images_handler: ImagesHandler = images_handler

    def __is_allowed(self, char: str) -> bool:
        return char.isalpha() or char in self.__special_characters.values()

    def __is_escape(self, char: str) -> bool:
        return char == self.__special_characters['escape']

    def __is_empty(self, query: str) -> bool:
        return query == self.__special_characters['empty']

    def __is_space(self, char: str) -> bool:
        return char == self.__special_characters['space']

    def __is_apply_suggestion(self, char: str) -> bool:
        return char == self.__special_characters['tab']

    def __is_delete(self, char: str) -> bool:
        return char == self.__special_characters['backspace']

    def __update_input_query(self, query: str, char: str, suggestions: Dict[str, Any]) -> str:
        if self.__is_delete(char):
            if not self.__is_empty(query):
                query = query[: -1]
        elif self.__is_apply_suggestion(char):
            query = CLIApp.apply_suggestion(query, suggestions)
        else:
            query += char
        return query

    def __init_insertion_print(self):
        print(self.__term.clear() + self.__term.move(0, 0) + 'Caption: ""')

    def __update_insertion_print(self, query: str):
        print(self.__term.clear() + self.__term.move(0, 0) + f'Caption: "{query}"')

    def __compute_suggestions(self, query: str) -> Dict[str, Any]:
        suggestions = CLIApp.init_suggestions()
        suggestions['query_completion'] = self.__ranker.lookup_query(query)
        # if self.__is_space(query[-1]):
        #     suggestions['word_correction'] = self.__assistant.correct(words)
        #     if not bool(suggestions['word_correction']):
        #         suggestions['word_prediction'] = self.__assistant.predict(words)
        # else:
        #     suggestions['word_completion'] = self.__assistant.complete(words)
        return suggestions

    def __print_suggestions(self, query: str, suggestions: dict):
        query_length = len(query)
        words = None
        if bool(suggestions['query_completion']):
            print(self.__term.move(1, 0) + self.__term.cyan)
            for _, query_completion, _ in suggestions['query_completion']:
                print(self.__special_characters['tab'] + query_completion.text)
            print(self.__term.normal)
        if bool(suggestions['word_correction']):
            prefix = self.__term.move(1, query_length - len(words[-1]) + 8) + self.__term.green
            suffix = self.__term.normal
            print(prefix + str(suggestions['word_correction']['right_word']) + suffix)
        elif bool(suggestions['word_prediction']):
            prefix = self.__term.move(0, query_length + 8 + 1) + self.__term.dim
            suffix = self.__term.normal + '"'
            print(prefix + suggestions['word_prediction']['next_word'] + suffix)
        elif bool(suggestions['word_completion']):
            prefix = self.__term.move(1, query_length - len(words[-1]) + 8) + self.__term.dim
            suffix = self.__term.normal
            print(prefix + suggestions['word_completion']['complete_word'] + suffix)

    def __show_images(self, query_completions: List):
        images = self.__images_handler.download_images([doc_id for doc_id, _, _ in query_completions])
        self.__images_handler.draw_images(images)

    def run(self):
        self.__init_insertion_print()
        suggestions = None
        query = self.__special_characters['empty']
        while True:
            input_char = CLIApp.acquire_input_char()
            if not self.__is_allowed(input_char):
                continue
            if self.__is_escape(input_char):
                self.__show_images(suggestions['query_completion'])
                break
            if self.__is_empty(query):
                if self.__is_space(input_char) or self.__is_apply_suggestion(input_char):
                    continue
            elif self.__is_space(query[-1]) and self.__is_space(input_char):
                continue
            query = self.__update_input_query(query, input_char, suggestions)
            self.__update_insertion_print(query)
            if not self.__is_empty(query):
                suggestions = self.__compute_suggestions(query)
                self.__print_suggestions(query, suggestions)


if __name__ == '__main__':
    ctx = Context('src/typing_assistant/config/configs.json')
    cli_app = CLIApp(ctx)
    cli_app.run()
