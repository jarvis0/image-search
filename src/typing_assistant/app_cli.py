from typing import Any, Dict, List

from blessings import Terminal

import getch

from .config import config
from .context import Context
from .indexing.images_handler import ImagesHandler
from .indexing.indexes_loader import load_indexes
from .suggestions import OkapiBM25Ranker, TypingAssistant


class CLIApp():

    @staticmethod
    def acquire_input_char() -> str:
        return getch.getch()

    @staticmethod
    def init_suggestions() -> Dict[str, Any]:
        return {
            'query_completion': {},
            'term_correction': {},
            'term_prediction': {},
            'term_completion': {},
        }

    @staticmethod
    def replace_from_right(query: str, old_term: str, new_term: str) -> str:
        return new_term.join(query.rsplit(old_term, 1))

    @staticmethod
    def apply_suggestion(query: str, suggestions: Dict[str, Any]) -> str:
        if bool(suggestions['term_correction']):
            query = CLIApp.replace_from_right(
                query,
                suggestions['term_correction']['wrong_term'],
                suggestions['term_correction']['right_term'],
            )
        elif bool(suggestions['term_prediction']):
            query += suggestions['term_prediction']['next_term']
        elif bool(suggestions['term_completion']):
            query = CLIApp.replace_from_right(
                query,
                suggestions['term_completion']['incomplete_term'],
                suggestions['term_completion']['complete_term'],
            )
        return query

    def __init__(self, context: Context):
        self.__term: Terminal = ctx.term
        self.__special_characters: Dict[str, Any] = ctx.special_characters
        collection, lexicon, images_handler = load_indexes(config.ROOT)
        self.__ranker: OkapiBM25Ranker = OkapiBM25Ranker(context, collection, lexicon)
        self.__assistant: TypingAssistant = TypingAssistant(context, lexicon)
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
        if self.__is_space(query[-1]):
            # suggestions['term_correction'] = self.__assistant.correct(terms)
            if not bool(suggestions['term_correction']):
                suggestions['term_prediction'] = self.__assistant.predict(query)[0]
        # else:
        #     suggestions['term_completion'] = self.__assistant.complete(terms)
        return suggestions

    def __print_suggestions(self, query: str, suggestions: dict):
        query_length = len(query)
        terms = ''
        if bool(suggestions['query_completion']):
            print(self.__term.move(1, 0) + self.__term.cyan)
            for _, query_completion, _ in suggestions['query_completion']:
                print(self.__special_characters['tab'] + query_completion)
            print(self.__term.normal)
        if bool(suggestions['term_correction']):
            prefix = self.__term.move(1, query_length - len(terms[-1]) + 9) + self.__term.green
            suffix = self.__term.normal
            print(prefix + str(suggestions['term_correction']['right_term']) + suffix)
        elif bool(suggestions['term_prediction']):
            prefix = self.__term.move(0, query_length + 9 + 1) + self.__term.dim
            suffix = self.__term.normal + '"'
            print(prefix + suggestions['term_prediction']['next_term'] + suffix)
        elif bool(suggestions['term_completion']):
            prefix = self.__term.move(1, query_length - len(terms[-1]) + 9) + self.__term.dim
            suffix = self.__term.normal
            print(prefix + suggestions['term_completion']['complete_term'] + suffix)

    def __show_images(self, query_completions: List):
        images = self.__images_handler.download_images([doc_id for doc_id, _, _ in query_completions])
        captions = [caption for _, caption, _ in query_completions]
        images_captions = [*zip(images, captions)]
        self.__images_handler.draw_images(images_captions)

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
    ctx = Context(config.ROOT)
    cli_app = CLIApp(ctx)
    cli_app.run()
