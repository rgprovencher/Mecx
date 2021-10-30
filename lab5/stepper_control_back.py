#!/usr/bin/python3.7


import json
from PCF8591 import PCF8591
from stepper import Stepper
import time
import RPi.GPIO as GPIO

# SETUP

# not necessary as all GPIO operations are
# done inside the stepper and PCF classes,
# but useful to during troubleshooting
GPIO.setmode(GPIO.BCM)

LED = 24
Stepper_0 = 5
Stepper_1 = 6
Stepper_2 = 13
Stepper_3 = 19

pcf = PCF8591(0x48)

step = Stepper(Stepper_0, Stepper_1, Stepper_2, Stepper_3, LED, pcf)

try:
    while True:
        with open("step-settings.txt", "r") as f:
            data = json.load(f)
            reset = int(data["reset"])
            angle = float(data["angle"])
            
            if reset: step.zero()
            else: step.goAngle(angle)
            f.close()
        
        # for development
        time.sleep(.2)
        
        # thingspeak compliant
        # time.sleep(15)
            
        
except KeyboardInterrupt:
    GPIO.cleanup()