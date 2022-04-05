import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util



TIMEOUT = 10
TIMEOUT_360 = 30
LONGLEFT = 0.15
LONGRIGHT = 0.15
LEFT = 0.15
RIGHT = 0.15
CENTRETHRESHOLD = 0.2

# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
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
        
        time.sleep(1)
	
    # This is where movement will be called when object is found	
    def start(self, obj):

        # Timeout boolean.
        isTimeout = False

        # Start the thread that searches for objects
        self.TARGET = obj
        if(self.labels.count(self.TARGET) > 0):
            self.videostream = VideoStream(resolution=(self.imW,self.imH),framerate=30).start()
            self_thread = Thread(target=self.search,args=())
            startTime = time.perf_counter()
            self_thread.start()
		
            # Lift arm prior to search.
            from object_detection.movement.lift_servo import up as lift_up, down as lift_down
            lift_up()

		    #Check if object has been found
            found = self.searchResults()
            while(not found):
                if(time.perf_counter()-startTime < TIMEOUT_360 ):
                    self.spinSearch()
                    found = self.searchResults()

                    # except KeyboardInterrupt:
                    # print("KeyboardInterrupt at start()")
                else:
                    
                    isTimeout = True

                    # Lower arm after failed search.
                    lift_down()
                    break
					
		    #Run movement if object found and not timeout
            if(not isTimeout):
                self.align()
                self.runRobot()
				
			#close streams
            ObjectDetection.stop(self)		
            self.videostream.stop()   
        return self
	
    def align(self):
        from object_detection.movement.motor_controls import spin_right, spin_left 
        
        while(self.side != "centre"):

            if(self.side == "fullright"):
                spin_right(LONGRIGHT)

            elif(self.side == "fullleft"):
                spin_left(LONGLEFT)

            elif(self.side == "right"):
                spin_right(RIGHT)

            elif(self.side == "left"):
                spin_left(LEFT)

            time.sleep(0.2)				
	
    def stop(self):
        self.objectFound = False
        self.look = False
		
    def searchResults(self):
        return self.objectFound
    
    def spinSearch(self):
        from object_detection.movement.motor_controls import spin_right 
        spin_right(3.5)	

		
    def runRobot(self):

        from object_detection.ultrasensor.ultrasonic import distance
        from object_detection.movement.lift_servo import up as lift_up, down as lift_down
        from object_detection.movement.arm_movement import open as arm_open, close
        from object_detection.movement.motor_controls import run, back, spin_left

        counter = 0
        opened = False
        MOVE_INCREMENT = 0.3


        # Get to and pick up object
        while(True):       

            current_distance = distance()

            if((current_distance < 25) and (opened == False)):
                print(f'Close to object: distance = {current_distance}')
                lift_down()
                arm_open()
                opened = True

            elif(current_distance < 10):
                print(f'Around object: distance = {current_distance}')
                close()
                lift_up()
                break
            else:
                print(f'Moving, distance = {current_distance}')
                counter += 1
                run(MOVE_INCREMENT)

        # Return and drop object
        for i in range(counter):
            back(MOVE_INCREMENT)

        # spin_left(6)
        lift_down()
        arm_open()
        back(1.5)
        close()
        # spin_left(6)

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
            leftArea=0
            rightArea=0.1
            ratio = 0
            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                if ((scores[i] > self.min_conf_threshold) and (scores[i] <= 1.0) and (self.TARGET=="NA" or (self.TARGET==self.labels[int(classes[i])]))):
                    self.objectFound = True
					
                    ymin = int(max(1,(boxes[i][0] * self.imH)))
                    xmin = int(max(1,(boxes[i][1] * self.imW)))
                    ymax = int(min(self.imH,(boxes[i][2] * self.imH)))
                    xmax = int(min(self.imW,(boxes[i][3] * self.imW)))
					
                    leftArea = (ymax-ymin)*((self.imW/2.0)-xmin)
                    rightArea = (ymax-ymin)*(xmax-(self.imW/2.))
					
                    if(leftArea <= 0):
                        leftArea = 0
                        self.side = "fullright"
                    elif(rightArea <= 0):
                        rightArea = 0
                        self.side = "fullleft"
                    elif(leftArea/rightArea > (1-CENTRETHRESHOLD) and leftArea/rightArea < (1+CENTRETHRESHOLD)):
                        ratio = leftArea/rightArea
                        self.side = "centre"
                    elif (leftArea > rightArea):
                        self.side = "left"
                    else:
                        self.side = "right"
					

                    # cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

                    # # Draw label
                    # object_name = self.labels[int(classes[i])] # Look up object name from "labels" array using class index
                    # label = '%s: %f%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                    # labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                    # label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                    # cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                    # cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
			
            # cv2.imshow('Object detector', frame)			
            print(self.objectFound)
            print(ratio)			

            # except KeyboardInterrupt:
            #     print("KeyboardInterrupt at search()")
