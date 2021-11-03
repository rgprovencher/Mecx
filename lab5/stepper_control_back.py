#!/usr/bin/python3.7

# for running the motor
import json
from PCF8591 import PCF8591
from stepper import Stepper
import time
import RPi.GPIO as GPIO
import copy


# # for communicating with thingspeak
# from urllib.request import urlopen
# from urllib.parse import urlencode

from urllib.request import urlopen
from urllib.parse import urlencode


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

api = "ATAWP7YV71CFSMGK"

# sends an initial reset segnal so the
# code always begins with the arm set to 0

with open("/usr/lib/cgi-bin/lab5/step-settings.txt", "w") as file:
    file.write("""{"reset":"1", "angle":"0"}""")
    file.close()


try:
    while True:
        
        # refreshes url
        url = "https://api.thingspeak.com/update?"
        
        # updates current to the current angle of the motor
        # slight delay before this reading is required, or
        # it may read current a split second before
        # motor has finished turning; this causes the if(angle==current)
        # test later in the code to fail erroneously and leads to
        # a 30sec delay between user inputs instead of 15 sec.
        time.sleep(.2)
        current = step.angle()
        
        with open("/usr/lib/cgi-bin/lab5/step-settings.txt", "r") as f:
            data = json.load(f)
            reset = int(data["reset"])
            angle = copy.deepcopy(float(data["angle"]))
            
            # if the user hasn't either hit the reset button or
            # declared a new angle since the last iteration of this loop,
            # returns to the top pf the loop. This prevents calls GET
            # requests from being sent to thingspeak when no changes
            # have been made, and so when the user does enter a value,
            # they won't be in the middle of a 15 second wait before
            # a new request can be sent immediately
            
            if ((not reset) and (angle == current)):
                
                time.sleep(.2)
                # it took me literal hours to figure out that this entire
                # code breaks if this delay isn't here
                
                continue

            
            
            
            
            # motor actuation
            if reset:
                step.zero()
                
                # edits the text file to prevent code from
                # continually running the zero function
                initial = {"reset":"0", "angle":"0"}
                with open("/usr/lib/cgi-bin/lab5/step-settings.txt", "w") as file:
                    file.write("""{"reset":"0", "angle":"0"}""")
                    file.close()
                
            else: step.goAngle(angle)
                
            
        
            # updating thingspeak
            # shortenint angle output to x.xx
            motorAngle = step.angle()
            motorAngle = float("{:.3f}".format(motorAngle))
            status = {
                "api_key":api,   # API key
                1: motorAngle  # sends current angle into field 1
                }
            status = urlencode(status)
            url = url + status
            
            response = urlopen(url)  # update thingspeak field

            print("I changed to {}".format(angle))
            
            # thingspeak compliant. The continue command earlier in this
            # loop prevents this from being executed unless a change has
            # actually been made.
            time.sleep(15.5)
            
            
        
except KeyboardInterrupt:
    GPIO.cleanup()
    