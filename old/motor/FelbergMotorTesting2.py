from machine import Pin, I2C, ADC, PWM
import utime
import keyboard

class Count(object):
    def __init__(self,A,B):
        self.A = A
        self.B = B
        self.counter = 0
        self.gearRatio = 120
        self.circleDeg = 360
        self.resolution = 2
        self.angle = 0
        self.degreesPerPulse = 360/16
        self.gearedDegrees = self.degreesPerPulse/self.gearRatio
        A.irq(self.cb,self.A.IRQ_FALLING|self.A.IRQ_RISING) #interrupt on line A)
        B.irq(self.cb,self.B.IRQ_FALLING|self.B.IRQ_RISING) #interrupt on line B)

# Degrees per Pulse = Number of degrees in a circle/Number of encoder pulses per rotation
# Degrees per Pulse = 360 / 1920
# Gear Ratio means that every degree is 1/GR of a true degree






    def cb(self,msg):
        other,inc = (self.B,1) if msg == self.A else (self.A,-1) #define other line and increment
        if msg.value()!=other.value():
            self.counter+= - inc
        else:
            self.counter+= inc
            
        
        #self.counter += -inc if msg.value()!=other.value() else  inc #XOR the two lines and increment
        self.angle = self.counter*self.gearedDegrees
    def value(self):
        return self.counter



class myMotor():
    def __init__(self, inA, inB):
        self.engage = PWM(inA)
        self.engage.duty_u16(0)
        self.direction=inB
        self.direction.off()
        self.maxSpeed = 65535
        self.someSpeed= int(self.maxSpeed*1)
        self.halfSpeed = int(self.maxSpeed/2)
        self.quarterSpeed = int(self.halfSpeed/4)
        self.eigthSpeed = int(self.maxSpeed/8)
    def forwards(self,err=0):
        self.direction.on()
        self.engage.duty_u16(err)
    def backwards(self, err=0):
        self.direction.off()
        self.engage.duty_u16(err)
    def off(self):
        self.engage.duty_u16(0)
        self.direction.off()
class myMotor2():
    def __init__(self, inA, inB):
        self.engage = PWM(inA)
        self.engage.duty_u16(0)
        self.direction=PWM(inB)
        self.engage.duty_u16(0)
        self.maxSpeed = 65535
        self.someSpeed= int(self.maxSpeed*1)
        self.halfSpeed = int(self.maxSpeed/2)
        self.quarterSpeed = int(self.halfSpeed/4)
        self.eigthSpeed = int(self.maxSpeed/8)
    def CW(self,err=1): #forwards DIRECTIONS DEFINED WHEN FACING THE MOTOR SHAFT WITH THE ENCODER ON THE LEFT
        self.direction.duty_u16(0)
        self.engage.duty_u16(self.halfSpeed)
    def CCW(self, err=1): #backwards
        self.direction.duty_u16(self.halfSpeed)
        self.engage.duty_u16(0)
    def stop(self):
        self.engage.duty_u16(0)
        self.direction.duty_u16(0)
    def drive(self, error):
        goSpeed = abs(int(error*65536))
        if error < 0:
            self.CCW(goSpeed)
        elif error > 0:
            self.CW(goSpeed)
        else:
            self.stop()

encoderA = Pin(4, Pin.IN)
encoderB = Pin(5, Pin.IN)
inA = Pin(8, Pin.OUT)
inB = Pin(14, Pin.OUT)
stupidMotor = myMotor2(inA, inB)
encoder = Count(encoderA, encoderB)
t0 = utime.time()

#Not working pins
#Pin 6, 7
#working pins: 4, 5, 9
print("---", KeyboardInterrupt)
try:
    
    target= 90
    error = encoder.angle-target

    while abs(error)>0:
        utime.sleep(0.01)
        #print(encoder.angle, target, error)
        stupidMotor.drive(error)
        error = encoder.angle-target
        print(encoder.angle, target)
        
#     print(encoder.counter)
    stupidMotor.stop()
    utime.sleep(5)
except KeyboardInterrupt:
    stupidMotor.stop()


    



        
    




