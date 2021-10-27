
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


dcpin = 13
t = 2000


GPIO.setup(dcpin,GPIO.OUT)

pwm = GPIO.PWM(dcpin, 50)

begin = time.time()
run = 100.0
pwm.ChangeDutyCycle(100)
try:
	for i in range (0,5):
		run -= 20
		pwm.ChangeDutyCycle(run)
		time.sleep(.4)

except KeyboardInterrupt:
	print("end")
GPIO.cleanup()
