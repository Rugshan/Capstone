# Combine this with main.py to keep 'robot' wake word.
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
 
    # Set up porcupine with wake words.
    porcupine = pvporcupine.create(
        access_key=access_key,
        keywords=['grapefruit', 'terminator', 'jarvis']
    )
    #print('\nKEYWORDS:' + str(pvporcupine.KEYWORDS))
    print('\nHandle Created')
    print("Your available keywords are:\n'grapefruit', 'terminator', 'jarvis'")

    # Set up PyAudio.
    with noalsaerr():
        pa = pyaudio.PyAudio()
    print('PyAudio Created')
    
    # Debug Audio Input Device
    #for i in range(0, pa.get_device_count()):
    #    print('\n\nDevice Info: ' + str(pa.get_device_info_by_index(i)))

    # Input Index
    from decouple import config
    input_index = int(config('INPUT_INDEX'))

    # Set up audio stream.
    audio_stream = pa.open(
        rate = porcupine.sample_rate,
        channels = 1,
        format = pyaudio.paInt16,
        input = True,
        frames_per_buffer = porcupine.frame_length,
        input_device_index = input_index
    )
    print('Audio Stream Created')

    # Listen for wake words.
    while True:

        # Read and pass audio to Porcupine
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow = False)
        audio_frame = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(audio_frame)

        # Wake Word 0 (grapefruit)
        if keyword_index == 0 :

            print("Wake word 'grapefruit' for fetching detected.")
            # ADD OBJECT DETECTION FUNCTION
                # Also add fetching function.
        
        # Wake Word 1 (terminator)
        if keyword_index == 1 :

            print("Wake word 'terminator' for following detected.")
            # ADD OBJECT DETECTION FUNCTION
                # Also add following function.

        # Wake Word 2 (view glass)
        if keyword_index == 2 :

            print("Wake word 'jarvis' for selfie detected.")
            # ADD OBJECT DETECTION FUNCTION
                # Call save_photo() from inside object detection.
            
            from utilities import save_photo
            save_photo.save_photo()
 
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
