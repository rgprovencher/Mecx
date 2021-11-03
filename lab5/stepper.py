import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

# no. of half to move the cardboard arm by one cardboard width
FULL_ANGLE = 550

# no. of halfsteps to turn the arm by one half cardboard width
HALF_ANGLE  = 275

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
        
        self.state = 0 # tracks location within the stator sequence
        

        # defines the current angle of the cardboard arm,
        # with the LED at 180.
        # initialized to an arbitrary value
        self.theta = 90.0
        
       

    def __delay_us(self, tus): # use microseconds to improve time resolution
      endTime = time.time() + float(tus)/ float(1E6)
      while time.time() < endTime:
        pass
    
    
    def __halfstep(self, dir):
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
            
        self.__delay_us(2500)

        # 8 half-steps per cycle, 8 cycles per revolution, into a 1:64 gearbox = half-steps per full revolusion 
        # # 360 degrees per rev  /  no. of half-steps pre rev = degrees per half-step
        # = 0.0879 deg; 
        stepAngle = 0.0879 

        self.theta += dir*stepAngle
        self.theta = self.theta % 360.0
        
        
    def __moveSteps(self, steps, dir):
        # move actuation sequence a given number of half-steps
        
        for step in range(steps):
            self.__halfstep(dir)
    
    
    # reports current angle when called.
    # The class considers the position of
    # the LED to be 180 degrees, which simplifies some logic in other
    # class methods. this method adds 180 degrees to the internal
    # variable theta, and thus reports a current angle of the arm that
    # considers the LED to be at zero.
    def angle(self):
        return (self.theta+180)%360
              

        
    # given an angle, determines the nearest direction for the arm to
    # turn. Returns +1 for ccw, -1 for cw.
    def __nearest(self, angle):
      
      if (self.theta - angle)%360 < 180: dir = -1
      else: dir = 1

      return dir

    # gien an angle, rotates the cardboard arm to that angle.
    def goAngle(self, angle):
      # %360 short circuits any clever clogs who want to type in out of range angles.
      # adds 180 to input angle bc to user, LED is at 0; to class LED is at 180.
      angle = float((angle+180) % 360 )

      # find nearest turning direction 
      dir = self.__nearest(angle) 
      
      while abs(self.theta-angle) > .0879:
        self.__halfstep(dir)
        # print("angle:  {} theta: {} diff: {}".format(angle, self.theta, abs(self.theta-angle)))
      

    # Uses an optical sensor to return the cardboard arm to
    # the zero position
    def zero(self):

        # turn on LED
        GPIO.output(self.pins[4], 1)
        # pause to let LED fully illum before taking reading;
        self.__delay_us(500000)
        # take a reference reading
        calibration = self.pcf.read(0)     
        
        # find nearest direction to the LED at "0"
        # Note that internally, class sees LED at 180, not 0
        dir = self.__nearest(180)
        
        # turn until photocell registers a change
        read = calibration
        while (abs(calibration-read) < 10):
            
            self.__halfstep(dir)
            
            read = self.pcf.read(0)

        # if the value of the photocell DECREASES, it means the arm
        # was covering the photocell when this command was entered,
        # and moving has just uncovered it; the direction needs to
        # be reversed.
        if self.pcf.read(0) < calibration:
            print("reverse")
            dir *= -1
        else: print("forward")
        
        # rotates the cardboard one half-cardboard width to center
        # it in front of the LED
        self.__moveSteps(HALF_ANGLE, dir)

        # resets internal angle.
        self.theta = 180

        # turn off LED
        GPIO.output(self.pins[4], 0)       
        
