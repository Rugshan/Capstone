# Imports
from gpiozero import Servo
from time import sleep
import math
from gpiozero.pins.pigpio import PiGPIOFactory

# Setup
factory = PiGPIOFactory()
vertical = Servo(11, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
horizontal = Servo(23, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

# Used to set a vertical positioning of the camera (0 to 360)
def change_vertical(i):
    vertical.value = math.sin(math.radians(i))

def change_horizontal(i):
    horizontal.value = math.sin(math.radians(i))

# Initial Position of the camera (Foward, angled down.)
def default_pos():
    vertical.value = math.sin(math.radians(170))
    horizontal.value = math.sin(math.radians(-57))