#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

#Definition of  motor pin 
IN1 = 22
IN2 = 27
ENA = 24


#Motor pin initialization operation
def motor_init():

    #Set the GPIO port to BCM encoding mode.
    GPIO.setmode(GPIO.BCM)

    #Ignore warning information
    GPIO.setwarnings(False)

    global pwm_ENA
    #global pwm_ENB
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)

    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)

#open
def open():

    #Init
    motor_init()

    GPIO.output(IN1, GPIO.HIGH)

    #PWM duty cycle is set to 100（0--100）
    pwm_ENA.start(50)
    time.sleep(0.65)
    GPIO.output(IN1, GPIO.LOW)
    off()
    
#close
def close():
    
    # Init
    motor_init()

    #GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)

    #PWM duty cycle is set to 100（0--100）
    pwm_ENA.start(50)
    time.sleep(1)
    GPIO.output(IN2, GPIO.LOW)
    off()

# Stop and cleanup.
def off():

    pwm_ENA.stop()
    GPIO.cleanup()



