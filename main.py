import pyaudio
from assistant.language_model import model as lang_mod, speaker as sp_mod
from assistant.resolve_text import resolver as person_resolver
from assistant.model_text import resolver as model_resolver

chunk = 1024
frames = []


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
    speaker = sp_mod.Speaker()
    resolver_person_text = person_resolver.Resolver
    resolver_model_answer = model_resolver.Resolver
    model.initialization(stream=stream, speaker=speaker, p=p)
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        text = model.get_text_from_data(data)
        if text:
            print(text)
            command_type = resolver_person_text.get_type(text)
            answer = resolver_model_answer.get_answer(text=text, type_=command_type)
            if answer:
                speaker.speak(answer)
            else:
                speaker.speak('Я не поняла')


if __name__ == '__main__':
    run_assistant()
