from machine import Pin, I2C, ADC, PWM
import time
import math

class Count(object):
    def __init__(self,A,B, CPC):
        self.A = A
        self.B = B
        self.counter = 0
        self.angle = 0
        self.ppr = 14
        self.gearRatio = 30
        self.conversion = 1/CPC
        A.irq(self.cb,self.A.IRQ_FALLING|self.A.IRQ_RISING) #interrupt on line A)
        B.irq(self.cb,self.B.IRQ_FALLING|self.B.IRQ_RISING) #interrupt on line B)


    def cb(self,msg):
        other,inc = (self.B,1) if msg == self.A else (self.A,-1) #define other line and increment
        self.counter += -inc if msg.value()!=other.value() else  inc #XOR the two lines and increment
        self.angle = 360 * (self.counter*self.conversion)
    def value(self):
        return self.counter



class myMotor8266():
    def __init__(self, enable, phase, freq):
        self.freq=freq
        self.enable = PWM(enable,self.freq)
        self.enable.duty(0)
        self.phase=phase
        self.phase.off()
        
        self.boot()
        
    #boot function is necessary to eliminate problems that were occuring. helps to re-zero the motor
    def boot(self):
        self.CW(500)
        time.sleep(1e-5)
        self.stop()
        print("Booted")
        time.sleep(2)
        
    
    def CW(self,err):
        self.phase.on()
        self.enable.duty(err)
    def CCW(self, err):
        self.enable.duty(err)
        self.phase.off()
    def drive(self, error):
        goSpeed = abs(int(error))
        if error < 0:
            self.CW(goSpeed)
        elif error > 0:
            self.CCW(goSpeed)
    def stop(self):
        self.enable.duty(0)
        self.phase.off()


        
   
def pinMapper(pin):
    #maps a pin from board space to GPIO space 
   
    pinMap = { #Board Space to GPIO Map
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

    
def sign(val):
    if val<0:
        return -1
    return 1


def main():
    
    #Pins as listed on board: NOT GPIO DO NOT USE
    #phase is direction, enable is power
    C1 = 7
    C2 = 5
    phase = 1
    enable = 4

    #mapped to GPIO using above map
    encoderA = Pin(pinMapper(C1), Pin.IN)
    encoderB = Pin(pinMapper(C2), Pin.IN)
    enable = Pin(pinMapper(enable), Pin.OUT)
    phase = Pin(pinMapper(phase), Pin.OUT)


    #Motor and encoder declaration- unclear why a frequency declaration is required
    Motor = myMotor8266(enable, phase, freq=50)
    #CPC is overall counts for 1 full revolution
    encoder = Count(encoderA, encoderB, CPC = 6892)
  

    try:
        
        
        dt=0.01 
        targetAngle = 120
        
        
        
        #initial Error
        error = targetAngle+encoder.angle
        while abs(error)>0.06:
            Motor.drive(sign(error)*500)
            time.sleep(dt)
            error = targetAngle+encoder.angle
       

        Motor.stop()
    except KeyboardInterrupt:
        Motor.stop()

    
if __name__ == "__main__":
    main()


        
    







