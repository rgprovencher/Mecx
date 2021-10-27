import RPi.GPIO as GPIO
from PCF8591 import PCF8591
from stepper import Stepper
import time

# SETUP

GPIO.setmode(GPIO.BCM)

LED = 24
Stepper_0 = 5
Stepper_1 = 6
Stepper_2 = 13
Stepper_3 = 19

pins = [LED, Stepper_1, Stepper_2, Stepper_3, Stepper_0]

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)