from assistant import types_text
import random
from assistant import information_from_yaml

MOST_USEFUL_PHRASES = {
    types_text.CommandType.greeting: [
        f'привет!', f'здравствуй!',
    ]
}

AUTHORIZING = {
    True: "Авторизация прошла успешно. " + random.choice(MOST_USEFUL_PHRASES.get(types_text.CommandType.greeting)),
    False: "Мне не удалось вас распознать. Желаете повторить попытку идентификации личности?"
}
