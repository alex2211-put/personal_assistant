import json

import os

from vosk import KaldiRecognizer
from vosk import Model


_PATH_TO_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class LanguageModel:

    def __init__(self, language='ru'):
        self.language = language
        self._model = None
        self._recognizer = None
        self._recognizer = self.change_language(language)

    def change_language(self, language):
        self.language = language
        if self.language == 'ru':
            self._model = Model(_PATH_TO_BASE_DIR + '\\vosk-model-small-ru-0.22')
        else:
            raise NotImplementedError(
                f'Language {language} is not supported yet',
            )
        self._recognizer = None
        return self._get_recognizer()

    def get_text_from_data(self, data):
        if self._recognizer.AcceptWaveform(data):
            return json.loads(self._recognizer.Result())['text']
        return None

    def _get_recognizer(self):
        if self._recognizer is None:
            self._recognizer = KaldiRecognizer(self._model, 16000)
        return self._recognizer

