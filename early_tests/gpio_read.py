#! /usr/bin/python373all

import RPi.GPIO as GPIO

pin = 14


GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)

print("Content-type: text/html\n\n")
print('<html><body><font color = red'>')


print('GPIO pin % is: ' %pin, end = '')
if GPIO.input(pin):
  print("HIGH")
else:
  print("LOW")

print('</body></html>')