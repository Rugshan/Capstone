#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

#Definition of  motor pin 
IN1 = 23
IN2 = 11


#Motor pin initialization operation
def motor_init():

    #Set the GPIO port to BCM encoding mode.
    GPIO.setmode(GPIO.BCM)

    #Ignore warning information
    GPIO.setwarnings(False)

    global pwm_servo1
    global pwm_servo2
    GPIO.setup(IN1,GPIO.OUT)
    GPIO.setup(IN2,GPIO.OUT)
    pwm_servo1 = GPIO.PWM(IN1, 50)
    pwm_servo2 = GPIO.PWM(IN2, 50)
    pwm_servo1.start(0)
    pwm_servo2.start(0)
#right
def right():

    #Init
    motor_init()
    pwm_servo1.ChangeDutyCycle(1)
    GPIO.output(IN1, GPIO.HIGH)
    off()

#left
def left():

    #Init
    motor_init()
    servo_control_color()
    off()
def servo_pulse(myangle):
    pulsewidth = (myangle * 11) + 500
    GPIO.output(IN1, GPIO.HIGH)
    time.sleep(pulsewidth/1000000.0)
    GPIO.output(IN1, GPIO.LOW)
    time.sleep(20.0/1000-pulsewidth/1000000.0)

def servo_control_color():
    # for pos in range(181):
    #     servo_pulse(pos)
    #     time.sleep(0.009)
    #for pos in reversed(range(181)):
    servo_pulse(181)
         #time.sleep(0.009)
#up
def up():
    
    # Init
    motor_init()
    pwm_servo2.ChangeDutyCycle(1)
    GPIO.output(IN2, GPIO.HIGH)
    off()
#down
def down():

    #Init
    motor_init()
    servo_control_color2()
    off()
def servo_pulse2(myangle):
    pulsewidth = (myangle * 11) + 500
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(pulsewidth/1000000.0)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(20.0/1000-pulsewidth/1000000.0)

def servo_control_color2():
    # for pos in range(181):
    #     servo_pulse(pos)
    #     time.sleep(0.009)
    #for pos in reversed(range(181)):
    servo_pulse2(181)
         #time.sleep(0.009)

# Stop and cleanup.
def off():

    pwm_servo1.stop()
    pwm_servo2.stop()
    GPIO.cleanup()



