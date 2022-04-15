#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

#Definition of  motor pin 
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#Motor pin initialization operation
def motor_init():

    #Set the GPIO port to BCM encoding mode
    GPIO.setmode(GPIO.BCM)

    #Ignore warning information
    GPIO.setwarnings(False)

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
    pwm_ENA = GPIO.PWM(ENA, 1000)
    pwm_ENB = GPIO.PWM(ENB, 1000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)

#advance
def run(delaytime):
    motor_init()
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(6)
    pwm_ENB.ChangeDutyCycle(6)
    time.sleep(delaytime)
    brake()

#back
def back(delaytime):
    motor_init()
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(6)
    pwm_ENB.ChangeDutyCycle(6)
    time.sleep(delaytime)
    brake()

#turn left in place
def spin_left(delaytime):
    motor_init()
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(4)
    pwm_ENB.ChangeDutyCycle(4)
    time.sleep(delaytime)
    brake()

#turn right in place
def spin_right(delaytime):
    motor_init()
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(4)
    pwm_ENB.ChangeDutyCycle(4)
    time.sleep(delaytime)
    brake()

#brake
def brake():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.stop()
    pwm_ENB.stop()
    GPIO.cleanup()