import json

import os

from vosk import KaldiRecognizer
from vosk import Model
import random
import assistant.language_model.speaker
from assistant.model_text import base_phrases
from assistant import types_text
from assistant.resolve_text import base_phrases as person_phrases
import wave
import pyaudio
import shutil
from assistant.language_model.recognition_by_voice import authorization_by_voice
import pathlib
import yaml
from assistant import information_from_yaml

_PATH_TO_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# TODO: Проверка что в имени 3 слова


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

    def initialization(self, stream, speaker: assistant.language_model.speaker.Speaker, p):

        speaker.speak(random.choice(base_phrases.MOST_USEFUL_PHRASES.get(types_text.CommandType.greeting)) +
                      "Я твой голосовой помошник.")
        name, file = self._get_name_and_file(speaker, stream, p)
        person_name_with_ = '_'.join(name.split())
        path = pathlib.Path(_PATH_TO_BASE_DIR).parent.joinpath('person_files', person_name_with_)
        if not os.path.exists(path):
            speaker.speak(f"Такого пользователя еще нет. Желаете создать пользователя {name}?")
            text = None
            while text is None:
                data = stream.read(4000, exception_on_overflow=False)
                text = self.get_text_from_data(data)
            print(text)
            if any(phrase in text for phrase in person_phrases.AFFIRMATIVE_PHRASES):
                os.mkdir(path)
                os.rename(file, person_name_with_ + '.wav')
                shutil.move(person_name_with_ + '.wav', path.parent)
                speaker.speak("Пользователь успешно создан. Всё настроено. Я готова к использованию.")
                with open(pathlib.Path(_PATH_TO_BASE_DIR).parent.joinpath('settings.yaml'), 'w') as f:
                    yaml.dump({'name': name.split()[1]}, f)
                    yaml.dump({'authorization': True})

            else:
                speaker.speak("Провести авторизацию еще раз?")
                text = None
                while text is None:
                    data = stream.read(4000, exception_on_overflow=False)
                    text = self.get_text_from_data(data)
                if any(phrase in text for phrase in person_phrases.AFFIRMATIVE_PHRASES):
                    return self.initialization(stream, speaker, p)
                else:
                    speaker.speak("Хорошо. Вы в неавторизованном режиме. Я готова к использованию.")
                    with open(pathlib.Path(_PATH_TO_BASE_DIR).parent.joinpath('settings.yaml'), 'w') as f:
                        yaml.dump({'name': name.split()[1]}, f)
                        yaml.dump({'authorization': False})
        else:
            auth = authorization_by_voice.comparing_voices("_".join(name.split()))
            if auth:
                speaker.speak(base_phrases.AUTHORIZING[auth])
                with open(pathlib.Path(_PATH_TO_BASE_DIR).parent.joinpath('settings.yaml'), 'w') as f:
                    yaml.dump({'name': name.split()[1]}, f)
                    yaml.dump({'authorization': True})
            else:
                speaker.speak(base_phrases.AUTHORIZING[auth])
                data = stream.read(4000, exception_on_overflow=False)
                text = self.get_text_from_data(data)
                if any(phrase in text for phrase in person_phrases.AFFIRMATIVE_PHRASES):
                    return self.initialization(stream, speaker, p)
                speaker.speak("Хорошо. Вы в неавторизованном режиме. Я готова к использованию.")
                with open(pathlib.Path(_PATH_TO_BASE_DIR).parent.joinpath('settings.yaml'), 'w') as f:
                    yaml.dump({'name': name.split()[1]}, f)
                    yaml.dump({'authorization': False})
        for i in range(len(base_phrases.MOST_USEFUL_PHRASES.get(types_text.CommandType.greeting))):
            base_phrases.MOST_USEFUL_PHRASES[types_text.CommandType.greeting][i] += information_from_yaml.get_name()

    def _get_name_and_file(self, speaker, stream, p):
        file_name = 'voice.wav'
        speaker.speak("Скажи пожалуйста свои фамилию, имя и отчество, чтобы я смогла тебя распознать.")
        frames = []
        for i in range(int(44100 / 1024 * 2)):
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
        wf = wave.open(file_name, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b"".join(frames))
        wf.close()
        wave_audio_file = wave.open('voice.wav', "rb")
        offline_recognizer = KaldiRecognizer(self._model,
                                             wave_audio_file.getframerate())
        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                name = json.loads(offline_recognizer.Result())['text']
                return name, file_name
        else:
            speaker.speak("Я не смогла распознать речь.")
            return self._get_name_and_file(speaker=speaker, stream=stream, p=p)
