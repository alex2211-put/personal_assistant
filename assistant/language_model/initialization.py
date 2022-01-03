from assistant.language_model import speaker
from assistant.language_model.recognition_by_voice import authorization_by_voice
from assistant.model_text import base_phrases
from assistant.resolve_text import base_phrases as person_phrases

from vosk import KaldiRecognizer
from vosk import Model

import json
import os
import pathlib
import pyaudio
import shutil
import yaml
import wave

_PATH_TO_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def initialization(model, stream, speaker_: speaker.Speaker, p):
    name, file = _get_name_and_file(speaker_, stream, p)
    person_name_with_ = '_'.join(name.split())
    path = pathlib.Path(_PATH_TO_BASE_DIR).parent.joinpath('person_files', person_name_with_)
    if not os.path.exists(path):
        speaker_.speak(f"Такого пользователя еще нет. Желаете создать пользователя {name}?")
        text = model.get_text_from_stream(stream)
        if any(phrase in text for phrase in person_phrases.AFFIRMATIVE_PHRASES):
            os.mkdir(path)
            os.rename(file, person_name_with_ + '.wav')
            shutil.move(person_name_with_ + '.wav', path.parent)
            speaker_.speak("Пользователь успешно создан. Всё настроено. Я готова к использованию.")
            authorizing = True
        else:
            speaker_.speak("Провести авторизацию еще раз?")
            text = model.get_text_from_stream(stream)
            if any(phrase in text for phrase in person_phrases.AFFIRMATIVE_PHRASES):
                return initialization(model, stream, speaker_, p)
            else:
                speaker_.speak("Хорошо. Вы в неавторизованном режиме. Я готова к использованию.")
                authorizing = False
    else:
        auth = authorization_by_voice.comparing_voices("_".join(name.split()))
        if auth:
            speaker_.speak(base_phrases.AUTHORIZING[auth])
            authorizing = True
        else:
            speaker_.speak(base_phrases.AUTHORIZING[auth])
            data = stream.read(4000, exception_on_overflow=False)
            text = model.get_text_from_stream(data)
            if any(phrase in text for phrase in person_phrases.AFFIRMATIVE_PHRASES):
                return initialization(model, stream, speaker_, p)
            speaker_.speak("Хорошо. Вы в неавторизованном режиме. Я готова к использованию.")
            authorizing = False
    with open(pathlib.Path(_PATH_TO_BASE_DIR).parent.joinpath('settings.yaml'), 'w') as f:
        yaml.dump({'name': name.split()[1], 'authorization': authorizing}, f)


def _get_name_and_file(speaker_, stream, p):
    file_name = 'voice.wav'
    speaker_.speak("Скажи пожалуйста свои фамилию, имя и отчество, чтобы я смогла тебя распознать.")
    frames = []
    for i in range(int(80)):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)
    wf = wave.open(file_name, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b"".join(frames))
    wf.close()
    wave_audio_file = wave.open(file_name, "rb")
    model = Model(_PATH_TO_BASE_DIR + '\\vosk-model-small-ru-0.22')
    file_recognizer = KaldiRecognizer(model,
                                      wave_audio_file.getframerate())
    data = wave_audio_file.readframes(wave_audio_file.getnframes())
    if len(data) > 0:
        if file_recognizer.AcceptWaveform(data):
            name = json.loads(file_recognizer.Result())['text']
            return name, file_name
    else:
        speaker_.speak("Я не смогла распознать речь. ")
        return _get_name_and_file(speaker_=speaker_, stream=stream, p=p)
