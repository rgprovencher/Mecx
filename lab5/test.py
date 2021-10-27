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

pcf = PCF8591(0x48)

# pins = [LED, Stepper_1, Stepper_2, Stepper_3, Stepper_0]
# 
# for pin in pins:
#     GPIO.setup(pin, GPIO.OUT, initial=0)


# # LED Test       
#     
# try:
#     while True:
#         GPIO.output(LED, 1)
# except KeyboardInterrupt:
#     print("acknowledged")
# 
# 

# Stepper test

step = Stepper(Stepper_0, Stepper_1, Stepper_2, Stepper_3, LED, pcf)

# # CW & CCW test
# try:
#     print("cclockwise")
#     while True:
#         step.halfstep(1)
# except KeyboardInterrupt:
#     step.zero(-1)
#     time.sleep(.5)
#     print("now cw")
# 
# try:
#     while True:
#         step.halfstep(-1)
# except KeyboardInterrupt:
#     step.zero(1)
#     time.sleep(.5)
#     print("test complete")


# step test to see how many steps it takes to cover LED
# cardboard width ~ 550 halfsteps
# at edge of LED, goes from uncovered to half covered in 275 steps
# on zero function:
#     take a calibration reading
#     move in direction until edge detected
#         if value INCREASES
#             continue in same direction for 275 steps
#         if it decreases
#             reverse direction for 275 steps
#             
# 

# GPIO.output(LED, 1)
# go = "go"
# dir = 1
# 
# 1
# sum = 0
# while go != 'q':
#     if go == 'a':
#         dir = -1
#     elif go == 'd':
#         dir = 1    
#     step.moveSteps(275, dir)
#     print("Step: {} LED: {}".format(sum, pcf.read(0)))
#     sum += 1
#     go = input()
    


# dir = 1
# topside = 0
# baseline = pcf.read(0)
# sum = 0
# 
# while (topside == 0 || pcf.read(0) < baseline+5):
#     step.halfstep(dir)
#     if

print(61%360)
    

GPIO.cleanup()