# Necessary Imports
import struct
import pyaudio
import pvporcupine
from utilities.error_handler import noalsaerr

# Access Key
from decouple import config
access_key = config('SECRET_KEY')

# Variables
porcupine = None
pa = None
audio_stream = None

try:
 
    # Set up porcupine with wake word.
    porcupine = pvporcupine.create(access_key=access_key, keywords=['picovoice', 'jarvis'])
    #print('\nKEYWORDS:' + str(pvporcupine.KEYWORDS))
    print('\nHandle Created')

    # Set up PyAudio.
    with noalsaerr():
        pa = pyaudio.PyAudio()
    print('PyAudio Created')
    
    # Debug Audio Input Device
    #for i in range(0, pa.get_device_count()):
    #    print('\n\nDevice Info: ' + str(pa.get_device_info_by_index(i)))

    # Set up audio stream.
    audio_stream = pa.open(
        rate = porcupine.sample_rate,
        channels = 1,
        format = pyaudio.paInt16,
        input = True,
        frames_per_buffer = porcupine.frame_length,
        input_device_index = 1
    )
    print('Audio Stream Created')

    # Listen for wake words.
    while True:

        # Read and pass audio to Porcupine
        pcm = audio_stream.read(porcupine.frame_length)
        audio_frame = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(audio_frame)

        if keyword_index == 0 :
            print("Wake Word 'picovoice' detected")
        if keyword_index == 1 :
            print("Wake word 'jarvis' detected")
 
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
