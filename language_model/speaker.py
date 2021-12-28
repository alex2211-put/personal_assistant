from . import language_consts
import pyttsx3


class Speaker:

    def __init__(self, language='ru', gender='w'):
        self.language = language
        self.engine = pyttsx3.init()
        self.gender = gender

        self.change_language(language)

    def change_language(self, language):
        self.language = language
        try:
            if self.gender == 'w':
                self.engine.setProperty(
                    'voice', language_consts.VOICES.get(language)[0],
                )
            else:
                self.engine.setProperty(
                    'voice', language_consts.VOICES.get(language)[-1],
                )
        except TypeError:
            raise NotImplementedError(
                f'Language {language} is not supported yet',
            )

    def change_gender(self, gender):
        self.gender = gender

        self.change_language(self.language)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
