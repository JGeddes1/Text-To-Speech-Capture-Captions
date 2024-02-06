import pyaudio
import speech_recognition as sr
import json
from pocketsphinx import LiveSpeech
from datetime import datetime
# obtain audio from the microphone
r = sr.Recognizer()
data = {}
run  = True

with open("captions.json", "r") as f:
    data =json.load(f)

while run:
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source, duration=0.3)
        audio = r.listen(source)
        print("DONE")
    # recognize speech using Sphinx
    try:
        text = r.recognize_sphinx(audio)
        print("Sphinx thinks you said " + text)
        print(json.dumps(data,indent = 4))
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        data["notes"].append({
                str(timestamp) : text
        })

        with open("captions.json", "w") as outfile:
            outfile.write(json.dumps(text, indent=4))
        



    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    except:
        run = False
