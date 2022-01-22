from . import base_phrases
from assistant import types_text


class Resolver:

    @staticmethod
    def get_type(text):
        if any(greeting in text for greeting in base_phrases.GREETINGS_FROM_PEOPLE):
            return types_text.CommandType.greeting
        if any(weather in text for weather in base_phrases.WEATHER_PHRASES):
            pass
        return None
