import pyaudio
import speech_recognition as sr
import json
from pocketsphinx import LiveSpeech
from datetime import datetime, timedelta

# obtain audio from the microphone
r = sr.Recognizer()
data = {}
run = True

with open("captions.json", "r") as f:
    pass

subtitle_counter = 1  # Counter for subtitle sequence
global_start_time = datetime.now()  # Initial timestamp for global start time

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
        print(json.dumps(data, indent=4))

        # Calculate the duration since the global start time
        duration = datetime.now() - global_start_time

        # Format the start time in HH:MM:SS
        start_time_str = str(duration).split(".")[0]

        # Calculate the end time based on the length of the recognized text plus the duration since the global start time
        end_time = global_start_time + timedelta(seconds=len(text.split())) + duration
        end_time_str = str(end_time - global_start_time).split(".")[0]

        # Format the .srt entry and append to the file
        with open(file="captions.srt", mode="a", encoding="utf-8") as subFile:
            subFile.write(f"{subtitle_counter}\n")
            subFile.write(f"{start_time_str} --> {end_time_str}\n")
            subFile.write(f"{text}\n\n")

        subtitle_counter += 1  # Increment subtitle counter

    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    except Exception as e:
        print(f"Error: {e}")
        run = False
