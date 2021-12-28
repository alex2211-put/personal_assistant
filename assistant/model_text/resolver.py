from assistant import types_text
from . import base_phrases
import random

TYPES_FOR_TEXT_ANSWERS_ON_MESSAGE = [types_text.CommandType.greeting]
TYPES_FOR_FUNC_ANSWERS_ON_MESSAGE = [types_text.CommandType.search]


class Resolver:

    @staticmethod
    def get_answer(type_, text):
        if type_ in TYPES_FOR_TEXT_ANSWERS_ON_MESSAGE:
            return random.choice(base_phrases.MOST_USEFUL_PHRASES.get(type_))
        elif type_ in TYPES_FOR_FUNC_ANSWERS_ON_MESSAGE:
            pass
