from assistant import information_from_yaml
from assistant import types_text
import random
import time

MOST_USEFUL_PHRASES = {
    types_text.CommandType.greeting: [
        f'привет', f'здравствуй',
    ]
}

AUTHORIZING = {
    True: "Авторизация прошла успешно. ",
    False: "Мне не удалось вас распознать. Желаете повторить попытку идентификации личности? "
}


def greeting():
    name = information_from_yaml.get_name()
    with_part_of_day = _get_part_of_day()
    sample_phrases_for_greeting = MOST_USEFUL_PHRASES[types_text.CommandType.greeting].copy()
    sample_phrases_for_greeting.append(with_part_of_day)
    return random.choice(sample_phrases_for_greeting) + ', ' + name


def _get_part_of_day():
    now_time = time.localtime()
    if 23 <= now_time.tm_hour < 5:
        return "доброй ночи"
    if 5 <= now_time.tm_hour < 10:
        return "доброе утро"
    if 10 <= now_time.tm_hour < 17:
        return "добрый день"
    return "добрый вечер"
