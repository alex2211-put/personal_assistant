import pyaudio
from language_model import model as lang_mod
from language_model import speaker as sp_mod


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
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        text = model.get_text_from_data(data)
        if text:
            speaker.speak(text)


if __name__ == '__main__':
    run_assistant()
