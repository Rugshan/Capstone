# This file can be used to write several functions (defs) containing finite movement/control of the robot's tracks.
# Could make the functions have default values, and accept arguments if specific values are required (i.e. turnLeft(units: 5))

# Necessary Imports
from gpiozero import PhaseEnableRobot
from time import sleep, time
from RPi import GPIO as GPIO

#Definition of  motor pin 
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#Set the GPIO port to BCM encoding mode
GPIO.setmode(GPIO.BCM)

#Ignore warning information
GPIO.setwarnings(False)
#Motor pin initialization operation
def motor_init():
    global pwm_ENA
    global pwm_ENB
    global delaytime
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
# Variables
# The number of seconds an action should be performed for.
howLong = 1

#Since we haven't connected the Raspberry Pi to the robot, the GPIO pins in this statement may change.
#motor_init()
robot = PhaseEnableRobot(left = (20, 21), right = (19, 26)) 

#Makes the robot turn left for the given time.
def turnLeft(howLong):
	print('Moving to the left for ' + str(howLong) + ' seconds.\n')
	robot.left()
	sleep(howLong)
	robot.stop

#Makes the robot turn right for the given time.
def turnRight(howLong):
	print('Moving to the right for ' + str(howLong) + ' seconds.\n')
	robot.right()
	sleep(howLong)
	robot.stop

#Makes the robot move forward for the given time.
def moveForward(howLong):
	print('Moving forward for ' + str(howLong) + ' seconds.\n')
	robot.forward()
	sleep(howLong)
	robot.stop

#Makes the robot move backward for the given time.
def moveBackward(howLong):
	print('Moving backward for ' + str(howLong) + ' seconds.\n')
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
	moveForward(4)
	moveBackward(8)
