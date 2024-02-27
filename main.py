from tkinter import filedialog
import pyaudio
import speech_recognition as sr
import json
from pocketsphinx import LiveSpeech
from datetime import datetime, timedelta
import tkinter as tk 
import os 



def audio_file_transcribe():
    filetypes = (('audio files', '*.wav'), ("All Files", "*.*"))

    AUDIO_FILE = filedialog.askopenfilename(title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    

    r = sr.Recognizer()
    # Counter for my .srt
    counter = 1
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
    
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        translated_audio =  r.recognize_google(audio)
                # Get current timestamp

        # Calculate the duration based on the duration of the audio
        duration = len(audio.frame_data) / audio.sample_rate
        duration_str = str(timedelta(seconds=duration)).split(".")[0]

        # Format the .srt entry and append to the file
        with open(file="transcribed_audio.srt", mode="a", encoding="utf-8") as subFile:
            subFile.write(f"{counter}\n")
            subFile.write(f"00:00:00 --> {duration_str}\n")
            subFile.write(f"{translated_audio}\n\n")



    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    








def start_button_clicked():
    start_button.config(state=tk.DISABLED)  # Disable the button while the process is running
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
            text = r.recognize_google(audio, language = 'en-US') 
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



# Create the main Tkinter window
root = tk.Tk()
root.title("Start Button Example")

# Create a button widget
start_button = tk.Button(root, text="Start", command=start_button_clicked)
start_button.pack(pady=10)
transcribe_audio_file_button = tk.Button(root, text="Transcribe", command=audio_file_transcribe)
transcribe_audio_file_button.pack(pady=15)

# Create a button widget
# stop_button = tk.Button(root, text="Stop", command=stop_button_clicked)
# stop_button.pack(pady=10)
# Run the Tkinter event loop
root.mainloop()