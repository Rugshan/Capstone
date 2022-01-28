# This file can be used to write several functions (defs) containing finite movement/control of the robot's tracks.
# Could make the functions have default values, and accept arguments if specific values are required (i.e. turnLeft(units: 5))

# Necessary Imports
from gpiozero import Robot
from time import sleep, time
from RPi import GPIO as GPIO

# Variables
# The number of seconds an action should be performed for.
howLong = 1

#Since we haven't connected the Raspberry Pi to the robot, the GPIO pins in this statement may change.
robot = Robot(left = (7, 8), right = (9, 10)) 

#Makes the robot turn left for the given time.
def turnLeft(howLong):
	print('Moving to the left for ' + howLong + ' seconds.\n')
	robot.left()
	sleep(howLong)
	robot.stop

#Makes the robot turn right for the given time.
def turnRight(howLong):
	print('Moving to the right for ' + howLong + ' seconds.\n')
	robot.right()
	sleep(howLong)
	robot.stop

#Makes the robot move forward for the given time.
def moveForward(howLong):
	print('Moving forward for ' + howLong + ' seconds.\n')
	robot.forward()
	sleep(howLong)
	robot.stop

#Makes the robot move backward for the given time.
def moveBackward(howLong):
	print('Moving backward for ' + howLong + ' seconds.\n')
	robot.backward()
	sleep(howLong)
	robot.stop

#Makes the robot move in a square shape.
def moveSquare():
	print('Moving in a square shape.\n')
	robot.forward()
	sleep(3)
	robot.stop()
	robot.right()
	sleep(1)
	robot.stop()

while True:
	turnLeft(2)
	turnRight(3)
	moveForward()
	moveBackward()
