# This file can be used to read values from the robot's ultrasonic sensor.

# Necessary Imports
from RPi import GPIO as GPIO
import time

# Finds the distance between the sensor and an object and returns it.
def distance():
    
    # GPIO Mode (BOARD/BCM)
    # BOARD is used for physical pin numbers.
    # BCM is used for the BCM channel names from the Broadcom SOC that the pins are connected to (GPIO numbers).
    GPIO.setmode(GPIO.BCM)
    
    # Setting GPIO pins as constants.
    # Since we haven't connected the Raspberry Pi to the robot, the GPIO pins in these statements may change.
    GPIO_TRIGGER = 1
    GPIO_ECHO = 0
    
    # Setting GPIO direction (IN/OUT).
    # Setting up GPIO_TRIGGER as an output.
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    # Setting up GPIO_ECHO as an output.
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # GPIO Mode (BOARD/BCM)
    # BOARD is used for physical pin numbers.
    # BCM is used for the BCM channel names from the Broadcom SOC that the pins are connected to (GPIO numbers).
    GPIO.setmode(GPIO.BCM)
    
    # Setting GPIO pins as constants.
    # Since we haven't connected the Raspberry Pi to the robot, the GPIO pins in these statements may change.
    GPIO_TRIGGER = 1
    GPIO_ECHO = 0
    
    # Setting GPIO direction (IN/OUT).
    # Setting up GPIO_TRIGGER as an output.
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    # Setting up GPIO_ECHO as an output.
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    
    # Setting Trigger to High.
    GPIO.output(GPIO_TRIGGER, True)
 
    # Setting Trigger after 0.01 ms to Low.
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # Saving the time it starts.
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # Saving the time of arrival.
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # The time difference between start and arrival.
    TimeElapsed = StopTime - StartTime

    GPIO.cleanup()

    # Multiply the time elapsed with the speed of sound (34300 cm/s) and divide it by 2.
    distance = (TimeElapsed * 34300) / 2
 
    return float(distance)


