from machine import Pin, SoftI2C , PWM , ADC
import time
import ssd1306


#setting the pot
pot=ADC(Pin(3))
pot.atten(ADC.ATTN_11DB)
#button
down= Pin(10,Pin.IN)
select = Pin(9, Pin.IN)
up = Pin(8, Pin.IN)

i2c=SoftI2C(scl=Pin(7), sda=Pin(6))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.text("Booting Up",40,0)

valLookup={0:(64,90),1:(97,122),2:(48,57),3:(33,47),4:(-1,-1),5:(-1,-1)}
old_sel=0

def decrease(Pin):
    s.decreaseVal()
def selector(Pin):
    s.selectVal()
def increase(Pin):
    s.increaseVal()

class ConnectWifi():
    def __init__(self):
        self.ssid=""
        self.password=""
        self.charBoxWidth=  15
        self.charBoxHeigth= 30
        self.charBoxGap= 5 
        self.msg= [65,97,48,33,1,2]
        self.selection= 0
        self.x=10
        self.y=30
        
    def drawRect(self):
        for i in range(6):
            display.fill_rect(self.x + (self.charBoxWidth + self.charBoxGap) * i, self.y, self.charBoxWidth, self.charBoxHeigth, 1)
            display.text(chr(self.msg[i]-1),self.x+3 + (self.charBoxWidth + self.charBoxGap) * i,self.y-3, 0)
            display.text(chr(self.msg[i]),self.x+3 + (self.charBoxWidth + self.charBoxGap) * i,self.y +10, 0)
            display.text(chr(self.msg[i]+1),self.x+3 + (self.charBoxWidth + self.charBoxGap) * i,self.y+27, 0)
        display.rect(self.x + (self.charBoxWidth + self.charBoxGap) * self.selection - 3 , self.y-3, self.charBoxWidth + 6, self.charBoxHeigth + 6, 1)
        display.show()
        
    def writeletter(self):
        display.show()
    
    def decreaseVal(self):
        print(self.selection,"selection")
        print( self.msg,"before")
        if(self.msg[self.selection] == valLook[self.selection][0])
        self.msg[self.selection]-=1
        print( self.msg,"after")
        print("dec")
        
    def selectVal(self):
        print("sel")

        
    def increaseVal(self):
        print(self.selection,"selection")
        print( self.msg,"before")
        self.msg[self.selection]+=1
        print( self.msg,"after")
        print("inc")

    
    def changeSelectionValue(self,val):
        display.rect(self.x- 3 + (self.charBoxWidth + self.charBoxGap) * self.selection  , self.y-3, self.charBoxWidth + 6, self.charBoxHeigth + 6, 0)
        self.selection= val
        display.rect(self.x- 3 + (self.charBoxWidth + self.charBoxGap) * self.selection  , self.y-3, self.charBoxWidth + 6, self.charBoxHeigth + 6, 1)
        display.show()
        
s=ConnectWifi()
down.irq(trigger=Pin.IRQ_RISING, handler=decrease)
up.irq(trigger=Pin.IRQ_RISING, handler=increase)
select.irq(trigger=Pin.IRQ_RISING, handler=selector)
#select.irq(trigger=Pin.IRQ_RISING, callback=s.selectVal)
#up.irq(trigger=Pin.IRQ_RISING, callback=s.increaseVal)

while True:
    sel = 6-int(pot.read_u16()/65535 *6)
    if(not sel==old_sel):
        s.changeSelectionValue(sel)
    old_sel=sel
    s.drawRect()
    time.sleep(0.1)
    

