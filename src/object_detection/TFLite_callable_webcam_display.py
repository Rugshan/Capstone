import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util

# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
TIMEOUT = 10
TIMEOUT_360 = 20
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(640,480),framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

	# Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
	# Return the most recent frame
        return self.frame

    def stop(self):
	# Indicate that the camera and thread should be stopped
        self.stopped = True
		
class ObjectDetection:
    def __init__(self):
        self.TARGET = "apple"
        self.objectFound = False
        MODEL_NAME = "TFLite_Model"
        GRAPH_NAME = "detect.tflite"
        LABELMAP_NAME = "labelmap.txt"
        self.min_conf_threshold = 0.6
        resW= 1280
        resH = 720
        self.imW, self.imH = int(resW), int(resH)
        use_TPU = 0
        self.look = True
		
        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            from tflite_runtime.interpreter import Interpreter
            if use_TPU:
                from tflite_runtime.interpreter import load_delegate
        else:
            from tensorflow.lite.python.interpreter import Interpreter
            if use_TPU:
                from tensorflow.lite.python.interpreter import load_delegate

        # If using Edge TPU, assign filename for Edge TPU model
        if use_TPU:
            # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
            if (GRAPH_NAME == 'detect.tflite'):
                GRAPH_NAME = 'edgetpu.tflite'       

        # Get path to current working directory
        CWD_PATH = os.getcwd()

        # Path to .tflite file, which contains the model that is used for object detection
        PATH_TO_CKPT = os.path.join(CWD_PATH,"src/object_detection",MODEL_NAME,GRAPH_NAME)

        # Path to label map file
        PATH_TO_LABELS = os.path.join(CWD_PATH,"src/object_detection",MODEL_NAME,LABELMAP_NAME)

        # Load the label map
        with open(PATH_TO_LABELS, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        # Have to do a weird fix for label map if using the COCO "starter model" from
        # https://www.tensorflow.org/lite/models/object_detection/overview
        # First label is '???', which has to be removed.
        if self.labels[0] == '???':
            del(self.labels[0])

        # Load the Tensorflow Lite model.
        # If using Edge TPU, use special load_delegate argument
        if use_TPU:
            self.interpreter = Interpreter(model_path=PATH_TO_CKPT,
                                      experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
            print(PATH_TO_CKPT)
        else:
            self.interpreter = Interpreter(model_path=PATH_TO_CKPT)

        self.interpreter.allocate_tensors()

        # Get model details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

        self.floating_model = (self.input_details[0]['dtype'] == np.float32)

        self.input_mean = 127.5
        self.input_std = 127.5


        # Initialize video stream
        self.videostream = VideoStream(resolution=(self.imW,self.imH),framerate=30).start()
        time.sleep(1)
	
    # This is where movement will be called when object is found	
    def start(self, obj):
        isTimeout = False
        # Start the thread that searches for objects
        self.TARGET = obj
        if(self.labels.count(self.TARGET) > 0):
            self_thread = Thread(target=self.search,args=())
            startTime = time.perf_counter()
            self_thread.start()
		
		    #Check if object has been found
            found = self.searchResults()
            while(not found):
                if(time.perf_counter()-startTime < TIMEOUT ):
                    # try:
                    found = self.searchResults()

                    # except KeyboardInterrupt:
                    # print("KeyboardInterrupt at start()")
                else:
                    isTimeout = True
                    break
					
		    #Run movement if object found and not timeout
            if(not isTimeout):
                self.runRobot()
				
			#close streams	
            self.videostream.stop()
            ObjectDetection.stop(self)
            return self
	
    def stop(self):
        self.objectFound = False
        self.look = False
		
    def searchResults(self):
        return self.objectFound

    def runRobot(self):

        # from src.object_detection.ultrasensor.ultrasonic import distance 
        from object_detection.ultrasensor.ultrasonic import distance
        from object_detection.movement.arm_movement import open, close

        counter = 0
        opened = False

        while(True):       

            current_distance = distance()

            if((current_distance < 21) and (opened == False)):
                print(f'Close to object: distance = {current_distance}')
                open()
                opened = True

            elif(current_distance < 7):
                print(f'Around object: distance = {current_distance}')
                close()
                break
            else:
                print(f'Moving, distance = {current_distance}')
                # from src.object_detection.movement.motor_controls import run
                from object_detection.movement.motor_controls import run
                counter += 1
                run(1)

        for i in range(counter)
            back(1)

    def search(self):
        while (self.look):

            # try:

            # Grab frame from video stream
            frame1 = self.videostream.read()

            # Acquire frame and resize to expected shape [1xHxWx3]
            frame = frame1.copy()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (self.width, self.height))
            input_data = np.expand_dims(frame_resized, axis=0)

            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if self.floating_model:
                input_data = (np.float32(input_data) - self.input_mean) / self.input_std

            # Perform the actual detection by running the model with the image as input
            self.interpreter.set_tensor(self.input_details[0]['index'],input_data)
            self.interpreter.invoke()

            # Retrieve detection results
            boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0] # Bounding box coordinates of detected objects
            classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0] # Class index of detected objects
            scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0] # Confidence of detected objects
            #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)

            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                if ((scores[i] > self.min_conf_threshold) and (scores[i] <= 1.0) and (self.TARGET=="NA" or (self.TARGET==self.labels[int(classes[i])]))):
                    self.objectFound = True
            
            print(self.objectFound)	

            # except KeyboardInterrupt:
            #     print("KeyboardInterrupt at search()")
