# Imports
from gpiozero import Servo
from time import sleep
import math
from gpiozero.pins.pigpio import PiGPIOFactory

# Start PiGPIOD
factory = PiGPIOFactory()
servo = Servo(2, pin_factory=factory)

# Functions
def up():
    # Do not max out the range (sin(-90) to sin(90)), keep in this range (sin(x) + sin(y) = 1.25)
    for i in range (-12, 90):
        servo.value = math.sin(math.radians(i))
        sleep(0.01)

def down():
    # Do not max out the range (sin(-90) to sin(90)), keep in this range (sin(x) + sin(y) = 1.25)
    for i in range (90,-12, -1):
        servo.value = math.sin(math.radians(i))
        sleep(0.01)

