from machine import Pin,I2C
from machine import Pin, SoftI2C, PWM, ADC
import adxl345
import time

i2c = SoftI2C(scl = Pin(7), sda = Pin(6))


class SENSORS:
    def __init__(self,connection=i2c):
        self.i2c=connection
        self.adx = adxl345.ADXL345(self.i2c)
        
        self.initial = [0, 4095]
        self.final =  [0, 180]
        self.pot = ADC(Pin(3))
        self.pot.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V
 
        
        self.light = ADC(Pin(5))
        self.light.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V

        self.battery = ADC(Pin(4))
        self.battery.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V
        
        self.x=None
        self.y=None
        self.z=None
        self.roll=None
        self.pitch=None
        
        
    def readlight(self):
        return self.light.read()
    
    def readpot(self):
        return self.pot.read()
    
    def accel(self):
        self.x =self.adx.xValue
        self.y =self.adx.yValue
        self.z =self.adx.zValue
        

    def readaccel(self):
        self.accel()
        return self.x, self.y,self.z
    
    def readroll(self):
        self.accel()
        self.roll, self.pitch =  adx.RP_calculate(self.x,self.y,self.z)
        return self.roll,self.pitch
    
        
    def readpoint(self):
        l=[]
        p=[]
        for i in range(1000):
            l.append(self.readlight())
            p.append(self.readpot())
        l.sort()
        p.sort()
        l=l[300:600]
        p=p[300:600]
        avlight=sum(l)/len(l)
        avpos=sum(p)/len(p)
    
        point = avlight, self.mappot(avpos)
        return point
    
    def mappot(self, value):
        return int((self.final[1]-self.final[0]) / (self.initial[1]-self.initial[0]) * (value - self.initial[0]) + self.final[0])
  
    def readbattery(self):
        batterylevel=self.battery.read()

        if(batterylevel>2850): #charging
            return 'charging'
            
        elif(batterylevel>2700 and batterylevel <2875): #full charge
            return 'full'
        elif(batterylevel>2500 and batterylevel <2700): #medium charge
            return 'half'
        elif(batterylevel<2500): # low charge
            return 'low'
        else:
            pass
        
        return ""
        

        
