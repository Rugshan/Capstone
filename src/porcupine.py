# Necessary Imports
import struct
#import pyaudio
import pvporcupine

# Access Key
from decouple import config
access_key = config('SECRET_KEY')

try:
 
    # Set up porcupine with wake word.
    porcupine = pvporcupine.create(access_key=access_key, keywords=['picovoice'])
    print('Handle Created')
 
finally:
    if porcupine is not None:
        porcupine.delete() # Resource must be explicitly released after use.
        print('Handle Deleted')


# Need to figure out how to set up pyaudio

# # Variables
# porcupine = None
# pa = None
# audio_stream = None
 
# try:
 
#     # Set up porcupine with wake word.
#     porcupine = pvporcupine.create(keywords=["robot", "fetch", "follow", "selfie"])
 
#     # Set up audio streams
#     pa = pyaudio.PyAudio()
 
#     audio_stream = pa.open(
#         rate = porcupine.sample_rate,
#         channels = 1,
#         format = pyaudio.paInt16,
#         input = True,
#         frames_per_buffer = porcupine.frame_length
#     )
 
#     # Listen for wake words.
#     while True:
 
#         # Collect and Process Wake Word
#         pcm = audio_stream.read(porcupine.frame_length)
#         pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
 
#         keyword_index = porcupine.process(pcm)
 
#         # Execute Command
#         if keyword_index == 0: # "robot"
 
#             # Process next word
#             keyword_index = porcupine.process(pcm)
 
#             # Fetch {Obj}
#             if keyword_index == 1:
#                 fetch(obj)
 
#             # Follow Me
#             if keyword_index == 2:
#                 followMe()
 
#             # Take Selfie
#             if keyword_index == 3:
#                 takeSelfie()
 
# finally:
#     if porcupine is not None:
#         porcupine.delete()
 
#     if audio_stream is not None:
#             audio_stream.close()
 
#     if pa is not None:
#             pa.terminate()
 
