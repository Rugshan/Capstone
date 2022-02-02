# Imports
import os
import speech_recognition as sr
from utilities.error_handler import noalsaerr

# Input Index
from decouple import config
input_index = int(config('INPUT_INDEX'))

# Set up Speech Recognizer.
r = sr.Recognizer()
speech = sr.Microphone(device_index = input_index)

# Clear PyAudio spam.
os.system('cls' if os.name == 'nt' else 'clear')

print('-------------------------------------------------------------------------------\n')
print('Speech Recognizer created.')
print("Microphone assigned.\nUse 'src/utilities/get_index.py' to find the correct index")

try:

    # Listen Forever
    while True: 

        # Record Audio:
        with speech as source:
            print("\nListening...")
            audio = r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        # Translate Speech-to-Text:
        recog = r.recognize_google(audio, language = 'en-US')

        # Fetch
        if recog == 'fetch' :

            print("Wake word 'fetch' for fetching detected.")
            # ADD OBJECT DETECTION FUNCTION
                # Also add fetching function.
        
        # Follow
        if recog == 'follow' :

            print("Wake word 'follow' for following detected.")
            # ADD OBJECT DETECTION FUNCTION
                # Also add following function.

        # Selfie
        if recog == 'selfie' :

            print("Wake word 'selfie' for selfie detected.")
            # ADD OBJECT DETECTION FUNCTION
                # Call save_photo() from inside object detection.
            
            from utilities import save_photo
            save_photo.save_photo()






except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")

except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))