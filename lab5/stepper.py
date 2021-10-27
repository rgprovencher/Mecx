import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

class Stepper:

    def __init__(self, p0, p1, p2, p3, led, pcf):
        self.pins = [p0, p1, p2, p3, led]
        self.pcf = pcf
        
        for pin in self.pins:
          GPIO.setup(pin, GPIO.OUT, initial=0)
        

        # Define the pin sequence for counter-clockwise motion, noting that
        # two adjacent phases must be actuated together before stepping to
        # a new phase so that the rotor is pulled in the right direction:
        self.sequence = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
                [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
        
        self.state = 0
        
        self.theta = 180
       

    def delay_us(self, tus): # use microseconds to improve time resolution
      endTime = time.time() + float(tus)/ float(1E6)
      while time.time() < endTime:
        pass
    
    
    def halfstep(self, dir):
        # dir = +/- 1 for ccw, cw
        
        self.state += dir;
        if self.state > 7:
            self.state = 0
            #print()
        elif self.state < 0:
            self.state = 7
            #print()
        
        for pin in range(4):
            GPIO.output(self.pins[pin], self.sequence[self.state][pin])
        
        #print("{} ".format(self.state), end='')
            
        self.delay_us(2500)        
        
        
    def moveSteps(self, steps, dir):
        # move actuation sequence a given number of half-steps
        
        for step in range(steps):
            self.halfstep(dir)
    
    def zero(self, dir):
        GPIO.output(self.pins[4], 1)       # turn on LED
        calibration = self.pcf.read(0)     # take a reference reading
        
        
        
        GPIO.output(self.pins[4], 0)       # turn off LED
    
    
    
    # reports current angle when called. The class considers the position of
    # the LED to be 180 degrees, which simplifies some logic in other
    # class methods. this method adds 180 degrees to the internal variable theta,
    # and thus reports a current angle of the arm that considers the LED to
    # be at zero.
    def angle(self):
        return (theta+180)%360
        
        
    def nearest(self, angle):
        
