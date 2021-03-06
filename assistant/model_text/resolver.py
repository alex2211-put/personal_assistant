from assistant import types_text
from assistant.language_model.recognition_by_voice import authorization_by_voice
from . import base_phrases

import random

TYPES_FOR_TEXT_ANSWERS_ON_MESSAGE = [types_text.CommandType.greeting]
TYPES_FOR_FUNC_ANSWERS_ON_MESSAGE = [types_text.CommandType.search]


class Resolver:

    @staticmethod
    def authorization(file_with_received_voice):
        if authorization_by_voice.comparing_voices(file_with_received_voice):
            return base_phrases.AUTHORIZING[True]
        else:
            return base_phrases.AUTHORIZING[False]

    @staticmethod
    def get_answer(type_, text):
        if type_ in TYPES_FOR_TEXT_ANSWERS_ON_MESSAGE:
            if type_ == types_text.CommandType.greeting:
                return base_phrases.greeting()
            return random.choice(base_phrases.MOST_USEFUL_PHRASES.get(type_))
        elif type_ in TYPES_FOR_FUNC_ANSWERS_ON_MESSAGE:
            pass
