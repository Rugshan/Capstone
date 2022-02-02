# Capstone Project

## Git/GitHub Instructions

- This paragraph will make sense **after you read the GIT_INSTRUCTIONS.md page**:
    - Make sure to do a ```git pull``` on the developer branch any time you want to see the most up-to-date developer branch or when you are about to branch out from the developer branch to add a new function/change. This is important because the remote developer branch might have updated while you were gone, working on another feature, or when you accept your own pull request. Yes, you could do a ```git pull``` for other branches.

- Team, please refer to [**GIT_INSTRUCTIONS.md**](GIT_INSTRUCTIONS.md) for instructions on setting up and using our Git + GitHub repository.


## Config

### 1. Operating System:  
	
Currently using Linux (Ubuntu) for development.

### 2. Packages  

Please install the following packages required for Porcupine:

#### Porcupine
1. ```pip install pvporcupine```  
2. ```pip install python-decouple```

#### PyAudio
1. ```sudo apt-get install portaudio19-dev python3-pyaudio```  
2. ```pip install pyaudio```  
3. ```sudo apt-get install libasound2:i386```

##### This part of the code is used to debug for the correct audio input. Make sure your VM or robot has audio input enabled.
1. ```print('Device Count: ' + str(pa.get_device_count()))```  
2. ```print('Device Info: ' + str(pa.get_device_info_by_index(0)))```  

### JackControl
1. ```sudo apt install multimedia-jack```  
2. ```pulseaudio --kill```  
3. ```jack_control start```  

#### Permissions
1. ```sudo usermod -a -G audio $USER```  
2. **Log out and log back in.**  
3. **After every log in, please run: ```jack_control start```**

#### Change User Limits ((src)[https://jackaudio.org/faq/linux_rt_config.html])
1. ```sudo nano /etc/security/limits.d/audio.conf```  
2. Add the following two lines and save to the file:
   1. ```@audio   -  rtprio     95```
   2. ```@audio   -  memlock    unlimited```

#### OpenCV
1. ```pip install opencv-python```

### 3. Picovoice Access Keys  

In the src/ directory, create a file called '.env'. Open .env in a text editor and paste the following line:

```SECRET_KEY=COPY_PASTE_YOUR_ACCESS_KEY_HERE```

Where, the access key can be obtained by creating a free account at https://picovoice.ai/console/ and copying it from the 'AccessKey' tab.

### Starting The Program
1. `cd Capstone`
2. `jack_control start`
3. `python3 src/porcupine.py`  

#### Current Voice Commands:
The free Picovoice license is limits the number of custom wake-words, so the current wake words are:
- `grapefruit` for fetch
- `terminator` for follow
- `view glass` for selfie
   - Images are saved in `Capstone/saved_images/`
   - The *saved_images/* directory is added to .gitignore to keep it out of the repository.

Say any of the wake-words above to execute their corresponding functions.

Refer to earlier instructions for any environment issues.

### More Instructions to Come...
