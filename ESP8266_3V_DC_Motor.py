from machine import Pin, I2C, ADC, PWM
#import utime
import time


class Count(object):
    def __init__(self,A,B):
        self.A = A
        self.B = B
        self.counter = 0
        self.gearRatio = 150
        self.circleDeg = 360
        self.resolution = 2
        self.angle = 0
        self.degreesPerPulse = 360/28 #7 is pulses per revolution (ppr)
        self.gearedDegrees = self.degreesPerPulse/self.gearRatio
        A.irq(self.cb,self.A.IRQ_FALLING|self.A.IRQ_RISING) #interrupt on line A)
        B.irq(self.cb,self.B.IRQ_FALLING|self.B.IRQ_RISING) #interrupt on line B)

# Degrees per Pulse = Number of degrees in a circle/Number of encoder pulses per rotation
# Degrees per Pulse = 360 / 28
# Gear Ratio means that every degree is 1/GR of a true degree






    def cb(self,msg):
        other,inc = (self.B,1) if msg == self.A else (self.A,-1) #define other line and increment
        self.counter += -inc if msg.value()!=other.value() else  inc #XOR the two lines and increment
        self.angle = self.counter*self.gearedDegrees
    def value(self):
        return self.counter



class myMotor8266():
    def __init__(self, enable, phase):
        self.enable = PWM(enable)
        self.enable.duty(0)
        self.phase=phase
        self.phase.off()
        self.maxSpeed = 1023
        self.someSpeed= int(self.maxSpeed*1)
        self.halfSpeed = int(self.maxSpeed/2)
    def CW(self,err=0):
        self.phase.on()
        self.enable.duty(err)
        print(self.phase.value())
    def CCW(self, err=0):
        self.phase.off()
        self.enable.duty(err)
    def drive(self, error):
        goSpeed = abs(int((error/1023)*1023))
        if error < 0:
            self.CCW(goSpeed)
        elif error > 0:
            self.CW(goSpeed)
        else:
            self.off()
    def off(self):
        self.enable.duty(0)
        self.phase.off()
    
        
   
def pinMapper(pin):
    #maps a pin from D-space (board space) to GPIO space 
   
    pinMap = { #D-space to GPIO Map
        0:16,
        1:5,
        3:0,
        4:2,
        5:14,
        6:12,
        7:13,
        8:15,
        2:4,
        }     

    return pinMap[pin]

    

def main():
    
    #Pins as listed on board: NOT GPIO DO NOT USE
    C1 = 7
    C2 = 6
    phase = 1
    enable = 4

    #mapped to GPIO using above map
    encoderA = Pin(pinMapper(C1), Pin.IN)
    encoderB = Pin(pinMapper(C2), Pin.IN)
    enable = Pin(pinMapper(enable), Pin.OUT)
    phase = Pin(pinMapper(phase), Pin.OUT)


    #Motor and encoder declaration
    stupidMotor = myMotor8266(enable, phase)
    encoder = Count(encoderA, encoderB)
    
    #some variable declaration. With controls, i could specify the necessary K values- dont do that (yet). for now it will work to get them experimentally
    Kp = 0.25
    Ki = 1
    Kd = 1
    
    #setup for PID controller
    dedt = 0
    previousError = 0
    totalError = 0

    try:
        
        target= 720
        
        
        #initial Error
        error = encoder.angle-target
        print(encoder.angle)
        s=0.01 #shrinking s may possibly impact my data collection. if i shrink much more i will need to get rid of prints
        while abs(error)>0:
            time.sleep(s)
            #print(encoder.angle, target, error)
            error = encoder.angle-target
            
            
            #derivative numerical
            dedt = (error-previousError)/dt
            #accumulate error- integral term
            totalError += error
            
            #Apply PID Controller onto error term
            controlledError = Kp*error + Kd*dedt + Ki*totalError
            
            #Replace Error Values
            previousError = error
            
            #drive at new error
            stupidMotor.drive(controlledError)
            
            print(encoder.angle, error) #take this out when i need speeeeeeeed good for debugging though
        stupidMotor.off()
    except KeyboardInterrupt:
        stupidMotor.off()

    
if __name__ == "__main__":
    main()


        
    





