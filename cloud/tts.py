from google.cloud import texttospeech
import os
from playsound import playsound


class TextToSpeechManager:
    def __init__(self):
        # write path of Google Cloud Credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"
        """Synthesizes speech from the input string of text."""
        self.client = texttospeech.TextToSpeechClient()
        if not os.path.exists("../cached_speech"):
            os.mkdir("../cached_speech")

    def say(self, text, file_name="out.mp3", remove=True):
        input_text = texttospeech.SynthesisInput(text=text)
        # choose voice
        voice = texttospeech.VoiceSelectionParams(
            language_code="it-IT",
            name="it-IT-Wavenet-D",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )
        # choose encoding
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        # send request to Google Cloud
        response = self.client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

        # play received text
        with open(file_name, "wb") as out:
            out.write(response.audio_content)

        playsound(file_name)
        if remove:
            os.remove(file_name)

    def cached_say(self, text):
        ord3 = lambda x: '%.3d' % ord(x)
        hash_txt = str(hex(hash(int(''.join(map(ord3, text))))))[2:]

        file_path = "cached_speech/" + hash_txt + ".mp3"
        if os.path.exists(file_path):
            playsound(file_path)
        else:
            self.say(text, file_name=file_path, remove=False)
