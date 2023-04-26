from machine import Pin, SoftI2C, PWM, ADC
import time
import smarttools
import servo
import smartfunctions


STATE=[[0,3],[0,4],[0,3],[0,3]]
whereamI=0
wherewasI=-1
whenPressed=0

#Defining all flags
add=False
delete=False
save=False

#STATE=[(ICONnumber,TotalIcons),...]
# First number is ICON - default is 0 or first icon
# Second is Total number of ICONS in the SCREEN - 3 icons on Homescreen, 2 icons on PlayScreen and so on
#whereamI gives the SCREEN number I am at
#STATE[whereamI] gives the selected icon and total number of icons on that screen

#ICON
#0 - FirstICON
#1 - SecondICON
#2- ThirdICON

#SCREEN
#0 - HOMESCREEN
#1 - PlaySCREEN
#2 - TrainSCREEN
#3 - ConnectSCREEN


i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
display = smarttools.SSD1306_SMART(128, 64, i2c)


bdown = smarttools.BUTTON(8)
bselect = smarttools.BUTTON(9)
bup = smarttools.BUTTON(10)

s = servo.Servo(Pin(2))

#interrupt functions
def decrease(Pin):
    global whereamI
    global STATE
    global whenPressed
    global changed
    
    if(time.ticks_ms()-whenPressed>500):
        if(STATE[whereamI][0]>0):
            STATE[whereamI][0]-=1
        whenPressed=time.ticks_ms()
        print(STATE[whereamI])
        display.selector(whereamI,STATE[whereamI][0],STATE[whereamI][0]+1) #draw circle at selection position, and remove from the previous position
        changed=True
    
        
def selector(Pin):
    global whereamI
    global STATE
    global changed
    global add
    global delete
    global save
    time.sleep(0.2)
    if(whereamI==0):
        if(STATE[0][0]==0):
            whereamI=1 #training
        elif(STATE[0][0]==1):
            whereamI=2 #playing
        elif(STATE[0][0]==2):
            whereamI=3 #setup
        display.fill(0)
        display.selector(whereamI,STATE[whereamI][0],-1)
        display.displayscreen(whereamI)
        
    elif(whereamI==1):
        if(STATE[1][0]==0):
            add=True     #add data point         
        elif(STATE[1][0]==1):
            delete=True #delete data point
        elif(STATE[1][0]==2):
            save= True #save data to file
        elif(STATE[1][0]==3):# whereamI set to homescreen
            whereamI=0 
        display.fill(0)
        display.selector(whereamI,STATE[whereamI][0],-1)
        display.displayscreen(whereamI)
        changed=True
    

def increase(Pin):
    global whereamI
    global STATE
    global whenPressed
    global changed


    if(time.ticks_ms()-whenPressed>500):
        if(STATE[whereamI][0]<STATE[whereamI][1]-1):
            STATE[whereamI][0]+=1
        whenPressed=time.ticks_ms()
        display.selector(whereamI,STATE[whereamI][0],STATE[whereamI][0]-1) #draw circle at selection position, and remove from the previous position
        changed=True
    
#setting interrupts for button presses
bdown.irq(trigger=Pin.IRQ_RISING, handler=decrease)
bup.irq(trigger=Pin.IRQ_RISING, handler=increase)
bselect.irq(trigger=Pin.IRQ_RISING, handler=selector)
# pot pin GPIO3, A1, D1

pot = ADC(Pin(3))
pot.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V
# pot.read() returns integers in [0, 4095]


# light pin GPIO5
light = ADC(Pin(5))
light.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V

# plot ranges from 4,4 to 78, 59 for the box not to overlap with the border
ranges = {'pot': [0, 4095], 'light': [0, 4095], 'motor': [0, 180], 'screenx': [4, 123], 'screeny': [59, 20], 'oldscreenx': [4, 78], 'oldscreeny': [59, 4]} # screeny is backwards because it is from top to bottom
def transform(initial, final, value):
    initial = ranges[initial]
    final = ranges[final]
    return int((final[1]-final[0]) / (initial[1]-initial[0]) * (value - initial[0]) + final[0])

mode = 0
point = [9,9]
points = []


#setup with homescreen
#starts with whereamI=0
display.selector(whereamI,STATE[whereamI][0],-1)
oldpoint=[-1,-1]
#display.displayscreen(whereamI)

while True:

    if(whereamI==1): # Training Screen
        a=[]
        for i in range(10):
            a.append(light.read())
            a.average()
            
        point = [transform('light', 'oldscreenx', light.read()), transform('pot', 'oldscreeny', pot.read())]
        


        if(add):
            points.append(list(point))
            print("changed")
            print(points)
            
        elif(delete):
            if(points): #delete only when there is something
                points.pop()
                print(points)
        elif(save):
            print("write the points to a file")
        else:
            if(not point==oldpoint): #only when point is different now
                s.write_angle(transform('pot', 'motor', pot.read()))
                display.graph(oldpoint, point, points)

        #reset all flags
        add=False
        delete=False
        save=False
        oldpoint=point

        
    time.sleep(0.001)
        