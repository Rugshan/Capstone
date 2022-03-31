from gpiozero import Servo
from time import sleep
import math
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()
vertical = Servo(11, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
camera = Servo(23, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
vertical.value = math.sin(math.radians(30))
camera.max()
def v_up():
    for i in range (0, 90):
        vertical.value = math.sin(math.radians(i))
        sleep(0.01)
def v_down():
    for i in range (90,1, -1):
        vertical.value = math.sin(math.radians(i))
        sleep(0.01)
def c_up():
    for i in range (270, 360):
        camera.value = math.sin(math.radians(i))
        sleep(0.01)
def c_down():
    for i in range (360,270, -1):
        camera.value = math.sin(math.radians(i))
        sleep(0.01)
#vertical.max
#v_up()
#sleep(2)
#v_down()
#sleep(2)
#c_up()
#sleep(2)
#c_down()
#vertical.value = math.sin(math.radians(30))
#camera.max()
