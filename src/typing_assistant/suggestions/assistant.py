from context import Context

from nltk import ConditionalFreqDist, bigrams, trigrams

from sklearn.feature_extraction.text import TfidfVectorizer

from text_dataset import TextDataset


class TypingAssistant():

    def __init__(self, ctx: Context, dataset: TextDataset):
        self.__configs = ctx.configs
        self.__ugs_freq = TypingAssistant.build_ugs_freq(dataset.sentences, self.__configs['regex'])
        words = TypingAssistant.words_sentences_to_words(dataset.words_sentences)
        self.__bgs_freq = TypingAssistant.build_bgs_freq(words)
        self.__tgs_freq = TypingAssistant.build_tgs_freq(words)

    def correct(self, input_words: tuple) -> dict:
        known_word = []
        unique_words = set(self.__ugs_freq.keys())
        if input_words[-1] in unique_words:
            known_word = [input_words[-1]]
        edit1_tokens, edit2_tokens = [], []
        for word in unique_words:
            edit_distance = levenshtein_distance(word, input_words[-1])
            if edit_distance == 1:
                edit1_tokens.append(word)
            elif edit_distance == 2:
                edit2_tokens.append(word)
        candidates = known_word or edit1_tokens or edit2_tokens
        candidates = set(candidates)

        predictions = []
        if len(input_words) >= 3:
            tri_grams = dict(self.__tgs_freq[input_words[-3], input_words[-2]])
            selected_candidates = candidates & set(tri_grams.keys())
            if bool(selected_candidates):
                predictions = list(selected_candidates)
                predictions.sort(key=lambda x: tri_grams[x], reverse=True)
        elif len(input_words) == 2:
            bi_grams = dict(self.__bgs_freq[input_words[-2]])
            selected_candidates = candidates & set(bi_grams.keys())
            if bool(selected_candidates):
                predictions = list(selected_candidates)
                predictions.sort(key=lambda x: bi_grams[x], reverse=True)
        if len(predictions) == 0 and len(candidates) >= 1:
            predictions = list(candidates)
            predictions.sort(key=lambda x: self.__ugs_freq[x], reverse=True)

        suggestion = {}
        if len(predictions) >= 1 and predictions[0] != input_words[-1]:
            suggestion = {'right_word': predictions[0], 'wrong_word': input_words[-1]}
        return suggestion

    def predict(self, input_words: tuple) -> dict:
        if len(input_words) >= 2:
            predictions = tuple(self.__tgs_freq[(input_words[-2], input_words[-1])])
        else:
            predictions = tuple(self.__bgs_freq[input_words[-1]])

        suggestion = {}
        if len(predictions) >= 1:
            suggestion = {'next_word': predictions[0]}
        return suggestion

    def complete(self, input_words: tuple) -> dict:
        bi_grams, tri_grams = [], []
        if len(input_words) >= 3:
            tri_grams = self.__tgs_freq[input_words[-3], input_words[-2]]
        elif len(input_words) == 2:
            bi_grams = self.__bgs_freq[input_words[-2]]
        candidates = tri_grams or bi_grams or self.__ugs_freq
        candidates = dict(candidates)

        word_cutoff = len(input_words[-1]) + 1
        selected_candidates = {}
        for candidate, candidate_freq in candidates.items():
            similarity_score = levenshtein_similarity(input_words[-1], candidate[: word_cutoff])
            if similarity_score >= self.__configs['word_completion_threshold']:
                selected_candidates[candidate] = similarity_score

        predictions = []
        if len(selected_candidates) > 0:
            selected_candidates = dict(sorted(selected_candidates.items(), key=lambda x: x[1], reverse=True))
            predictions = tuple(selected_candidates.keys())

        suggestion = {}
        if len(predictions) >= 1 and predictions[0] != input_words[-1]:
            suggestion = {'complete_word': predictions[0], 'incomplete_word': input_words[-1]}
        return suggestion
