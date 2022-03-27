from assistant import information_from_yaml
from assistant.language_model import initialization
from assistant.language_model import model as lang_mod, speaker as sp_mod
from assistant.model_text import base_phrases
from assistant.model_text import resolver as model_resolver
from assistant.resolve_text import resolver as person_resolver
import pyaudio
import pymorphy2


def run_assistant():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8000
    )
    stream.start_stream()

    model = lang_mod.LanguageModel()
    morph = pymorphy2.MorphAnalyzer()
    resolver_model_answer = model_resolver.Resolver
    resolver_person_text = person_resolver.Resolver
    speaker = sp_mod.Speaker()
    information_from_yaml.set_name('')
    speaker.speak(base_phrases.greeting() + " Я твой голосовой помошник.")
    initialization.initialization(model=model, stream=stream, speaker_=speaker, p=p)
    while True:
        text = model.get_text_from_stream(stream)
        text = ' '.join(morph.parse(word)[0].normal_form for word in text.split())
        text = text.strip()
        if text:
            command_type = resolver_person_text.get_type(text)
            answer = resolver_model_answer.get_answer(text=text, type_=command_type)
            if answer:
                speaker.speak(answer)
            else:
                speaker.speak('Я не поняла')


if __name__ == '__main__':
    run_assistant()
