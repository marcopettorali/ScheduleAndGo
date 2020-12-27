import speech_recognition as sr


class SpeechToTextManager:
    mic = None
    google_cloud_credentials = None

    def __init__(self, json_credentials_path):
        # init microphone
        self.mic = sr.Recognizer()

        # read Google Cloud API credentials
        file = open(json_credentials_path, mode='r')
        self.google_cloud_credentials = file.read()

    def listen(self):
        # listen until pause is detected
        with sr.Microphone() as source:
            print('$ ', end='')
            audio = self.mic.listen(source)
            sentence = self.recognize(audio)
            print(sentence)
            return sentence

    def recognize(self, audio):
        try:
            # recognize sentence using Google Cloud Speech
            sentence = self.mic.recognize_google_cloud(audio, credentials_json=self.google_cloud_credentials,
                                                language="it-IT")
            return sentence
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))
            return None


