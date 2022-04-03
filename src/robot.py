# Imports
import os
import struct
import pyaudio
import pvporcupine
import speech_recognition as sr
from utilities.error_handler import noalsaerr

# Picovoice Access Key (Environment Variable)
from decouple import config
access_key = config('SECRET_KEY')

# Input Index (Environment Variable)
from decouple import config
input_index = int(config('INPUT_INDEX'))

# Platform (Environment Variable)
from decouple import config
platform = str(config('PLATFORM'))

if platform == 'Ubuntu':
    keyword_path = ['src/utilities/keywords/robot_en_linux_v2_1_0.ppn']

elif platform == "Raspberry Pi":
    keyword_path = ['src/utilities/keywords/robot_en_raspberry-pi_v2_1_0.ppn']


# Close Arm
from object_detection.movement.arm_movement import close as arm_close
print('Closing arm...')
arm_close()

# # Default camera pos.
# from object_detection.movement.camera_servos import default_pos as camera_default_pos
# camera_default_pos()

# Porcupine/PyAudio Variables
porcupine = None
pa = None
audio_stream = None

# Speech Recognition Variables
r = sr.Recognizer()
speech = sr.Microphone() # (device_index = input_index) (Set default input in system settings)

# OS Clear (Remove Spam)
os.system('cls' if os.name == 'nt' else 'clear')
print('-------------------------------------------------------------------------------\n')
print('Speech Recognizer created.')

# Start Porcupine and Google SR
try:

    # Porcupine wake-words.
    wake_words = ['grapefruit']
 
    # Set up porcupine with wake words.
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=keyword_path
        # keywords=wake_words
    )
    print('Handle Created')

    # Uncomment to list default Porcupine keywords:
    # print('\nKEYWORDS:' + str(pvporcupine.KEYWORDS))
    
    # Start PyAudio, remove warnings.
    with noalsaerr():
        pa = pyaudio.PyAudio()
    print('PyAudio Created')
    
    # Uncomment to list audio input devices:
    # for i in range(0, pa.get_device_count()):
    #    print('\n\nDevice Info: ' + str(pa.get_device_info_by_index(i)))

    # Set up audio stream.
    audio_stream = pa.open(
        rate = porcupine.sample_rate,
        channels = 1,
        format = pyaudio.paInt16,
        input = True,
        frames_per_buffer = porcupine.frame_length
        # input_device_index = 0 (Set default input in system settings)
    )
    print('Audio Stream Created')

    # Google SR
    with speech as source:
        audio = r.adjust_for_ambient_noise(source, 2)
    listening = False

    # Prompt
    print(f"\nYour wake-word is: 'robot'.")
    print("Say 'robot' to start listening for commands...\n")

    # Listen for Porcupine wake-words.
    while True:

        # Read and pass audio to Porcupine
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow = False)
        audio_frame = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(audio_frame)

        # Detect Wake Word
        if keyword_index >= 0:
            listening = True
            print("Wake word detected, starting up Google speech-to-text...")

        # Google Speech-to-Text
        if listening:
            with speech as source:
                print("\nListening for command...")
                audio = r.listen(source)

            try: 

                # Translate Speech-to-Text, split to list, lowercase:
                recog = r.recognize_google(audio, language = 'en-US')
                recog_list = recog.split()
                for i in range(len(recog_list)):
                    recog_list[i] = recog_list[i].lower()
                print(f"Heard: {str(recog_list)}")

                # Fetch Program
                if recog_list[0] == 'fetch' or recog_list[0] == 'get' or recog_list[0] == 'grab':

                    print(f"Command '{recog_list[0]}' detected.")
                    print(f"Fetching '{recog_list[1]}'...")

                    # ADD OBJECT DETECTION FUNCTION
                    from object_detection.TFLite_callable_webcam_display import ObjectDetection
                    fetch_object_detection = ObjectDetection()
                    fetch_object_detection.start(recog_list[1])
                
                # Follow Program
                if recog_list[0] == 'follow':

                    print("Command 'follow' detected.")
                    print("Following...")
                    # ADD OBJECT DETECTION FUNCTION
                        # Also add following function.

                # Selfie Program
                if recog_list[0] == 'selfie':

                    print("Command 'selfie' detected.")
                    # ADD OBJECT DETECTION FUNCTION
                        # Call save_photo() from inside object detection.
                    
                    from utilities import save_photo
                    save_photo.save_photo()

                # Close Arm
                if recog_list[0] == 'close':
                    print('Closing arm...')
                    arm_close()

                # Open Arm
                if recog_list[0] == 'open':
                    from object_detection.movement.arm_movement import open
                    print('Opening arm...')
                    open()

                # Reverse
                if recog_list[0] == 'reverse' or recog_list[0] == 'back':
                    from object_detection.movement.motor_controls import back
                    print('Reversing...')
                    back(2)

                # Forward
                if recog_list[0] == 'forward' or recog_list[0] == 'move':
                    from object_detection.movement.motor_controls import run
                    print('Going forward...')
                    run(2)

                # Turn Left
                if (recog_list[0] == 'turn' or recog_list[0] == 'spin') and recog_list[1] == 'left':
                    from object_detection.movement.motor_controls import spin_left
                    print('Turning left...')
                    spin_left(3)


                # Turn Right
                if (recog_list[0] == 'turn' or recog_list[0] == 'spin') and recog_list[1] == 'right':
                    from object_detection.movement.motor_controls import spin_right
                    print('Turning right...')
                    spin_right(3)

                print("\nListening for wake-word...")
            
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                print("Say 'robot' to start listening for commands...\n")

            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
            finally:
                listening = False

finally:

    # Release resources after they are done being used.

    if porcupine is not None:
        porcupine.delete() # Resource must be explicitly released after use.
        print('Handle Deleted')
    
    if audio_stream is not None:
            audio_stream.close()
            print('Audio Stream Closed')

    if pa is not None:
        pa.terminate()
        print('PyAudio Terminated')
