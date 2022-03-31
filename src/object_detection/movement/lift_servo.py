from gpiozero import Servo
from time import sleep
import math
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()
servo = Servo(2, pin_factory=factory)
def up():
    for i in range (0, 90):
        servo.value = math.sin(math.radians(i))
        sleep(0.01)
def down():
    for i in range (90,1, -1):
        servo.value = math.sin(math.radians(i))
        sleep(0.01)