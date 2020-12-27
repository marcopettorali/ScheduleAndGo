import stt
import tts
import nlp_google

s = stt.SpeechToTextManager("googlekey.json")
n = nlp_google.NaturalProcessingLanguageGoogleCloud()
t = tts.TextToSpeechManager()

while(True):
    sentence = s.listen()
    task = n.analyze_task(sentence)
    print("task = ", end="")
    print(task)
    speech = "Ok, vado a " + task['destination'] + " per il seguente motivo: "
    for k in task['action']:
        speech += k + " " + task['action'][k] + ", "
    speech += ". Per confermare dire \"OK\""
    t.cached_say(speech)

    confirm = s.listen()
    if confirm.strip().lower() == "ok":
        # send command
        t.cached_say("Ok, richiesta inviata")
        #get response from task management system
    else:
        continue




