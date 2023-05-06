
from machine import Pin, SoftI2C, PWM, ADC
import time
from machine import Timer
#import smarttools
import servo
import icons


STATE=[[0,3],[0,4],[0,4],[0,3]]
whereamI=0
wherewasI=-1
whenPressed=0
prev=0



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

#Battery
MAX_BATTERY=2900
MIN_BATTERY=2600
#Defining all flags
#Train screen flags
adddata=False
deletedata=False
run=False

#Play screen flags
toggle=False
pause=False

i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
display = icons.SSD1306_SMART(128, 64, i2c)


bdown = Pin(8, Pin.IN)
bselect = Pin(9, Pin.IN)
bup = Pin(10, Pin.IN)

s = servo.Servo(Pin(2))

#interrupt functions
def downpressed():
    time.sleep(0.1)
    global whereamI
    global STATE
    global whenPressed
    global changed
    global prev
    
    if(time.ticks_ms()-whenPressed>500):
        print(STATE[whereamI][0])
        STATE[whereamI][0]=(STATE[whereamI][0]-1)%STATE[whereamI][1]
        whenPressed=time.ticks_ms()
        display.selector(whereamI,STATE[whereamI][0],prev) #draw circle at selection position, and remove from the previous position
        prev=STATE[whereamI][0]
        changed=True
    
def uppressed():
    time.sleep(0.1)
    global whereamI
    global STATE
    global whenPressed
    global changed
    global prev

    if(time.ticks_ms()-whenPressed>500):
        print(STATE[whereamI][0])
        STATE[whereamI][0]=(STATE[whereamI][0]+1)%STATE[whereamI][1]
        whenPressed=time.ticks_ms()
        display.selector(whereamI,STATE[whereamI][0],prev) #draw circle at selection position, and remove from the previous position
        prev=STATE[whereamI][0]
        changed=True
   
def selectpressed():
    time.sleep(0.1)
    #declare all global variables, include all flags
    global whereamI
    global adddata
    global deletedata
    global save

    #Home screen
    if(whereamI==0):
        if(STATE[0][0]==0):
            whereamI=1      #Train Screen
        elif(STATE[0][0]==1):
            whereamI=2      #select the play Screen   - with choices of dataset
        elif(STATE[0][0]==2):
            whereamI=3      #Settings Screen - ble connection, wifi, etc. 
        display.fill(0)
        display.selector(whereamI,STATE[whereamI][0],-1)
        #display.displayscreen(whereamI)
        
    #Train screen
    elif(whereamI==1): 
        if(STATE[1][0]==0):
            adddata=True     #add data point         
        elif(STATE[1][0]==1):
            deletedata=True #delete data point
        elif(STATE[1][0]==2):
            whereamI=2 #run using the train data
        elif(STATE[1][0]==3):
            whereamI=0 # go back to homescreen
            
        display.fill(0)  #clean screen
        display.selector(whereamI,STATE[whereamI][0],-1) # load the selector on relevant icon
        #display.displayscreen(whereamI)                  # load relevant screen
        
    #Play screen 
    elif(whereamI==2): 
        if(STATE[2][0]==0):
            adddata=True        # toggle screeen view     
        elif(STATE[2][0]==1):
            delete=True     # save data
        elif(STATE[2][0]==2):
            whereamI=2      # pause the run 
        elif(STATE[2][0]==3):
            whereamI=0      # Go back to home screen
        
        display.fill(0) # clear screen
        display.selector(whereamI,STATE[whereamI][0],-1) # load the selector on relevant icon
        #display.displayscreen(whereamI)                  # load relevant screen
        
#call back to check the button presses
def check_switch(p):
    global switch_state_up
    global switch_state_down
    global switch_state_select
    
    global switched_up
    global switched_down
    global switched_select
    
    global last_switch_state_up
    global last_switch_state_down
    global last_switch_state_select
    
    switch_state_up = switch_up.value()
    switch_state_down = switch_down.value()
    switch_state_select = switch_select.value()
    
    
    if switched_up:
        if switch_state_up == 1:
            uppressed()
        switched_up = False
    elif switched_down:
        if switch_state_down == 1:
            downpressed()
        switched_down = False
    elif switched_select:
        if switch_state_select == 1:
            selectpressed()
        switched_select = False
        
    if switch_state_up != last_switch_state_up:
        switched_up = True
        
    elif switch_state_down != last_switch_state_down:
        switched_down = True
        
    elif switch_state_select != last_switch_state_select:
        switched_select = True
    
    last_switch_state_up = switch_state_up
    last_switch_state_down = switch_state_down
    last_switch_state_select = switch_state_select


switch_down = Pin(8, Pin.IN)
switch_select = Pin(9, Pin.IN)
switch_up= Pin(10, Pin.IN)

switch_state_up = switch_up.value()
switch_state_down = switch_down.value()
switch_state_select = switch_select.value()

last_switch_state_up = switch_state_up
last_switch_state_down = switch_state_down
last_switch_state_select = switch_state_select

switched_up = False
switched_down = False
switched_select = False

#def getswitch():



tim = Timer(0)
tim.init(period=50, mode=Timer.PERIODIC, callback=check_switch)




        

  
#setting interrupts for button presses
'''  
bdown.irq(trigger=Pin.IRQ_RISING, handler=decrease)
bup.irq(trigger=Pin.IRQ_RISING, handler=increase)
bselect.irq(trigger=Pin.IRQ_RISING, handler=selector)
'''
# pot pin GPIO3, A1, D1

pot = ADC(Pin(3))
pot.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V
# pot.read() returns integers in [0, 4095]


# light pin GPIO5
light = ADC(Pin(5))
light.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V


battery = ADC(Pin(4))
battery.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V

# plot ranges from 4,4 to 78, 59 for the box not to overlap with the border

def mappot(value):
    initial = [0, 4095]
    final =  [0, 180]
    return int((final[1]-final[0]) / (initial[1]-initial[0]) * (value - initial[0]) + final[0])


def readSensor():
    l=[]
    p=[]  
    for i in range(1000):
        l.append(light.read())
        p.append(pot.read())
    l.sort()
    p.sort()
    l=l[300:600]
    p=p[300:600]
    avlight=sum(l)/len(l)
    avpos=sum(p)/len(p)
    
    point = avlight, mappot(avpos)
    return point

def savetofile(points):
    f=open("data.py","w")
    f.write("tada")
    f.close()
    

def nearestNeighbor(data, point):
    try:
        point = point[0]
    except TypeError:
        print("error")
        pass
    if len(data) == 0:
        return 0
    diff = 10000
    test = None
    for i in data:
        if abs(i[0] - point) <= diff:
            diff = abs(i[0] - point)
            test = i
    return test


point = [9,9]
points = []

#setup with homescreen
#starts with whereamI=0
display.selector(whereamI,STATE[whereamI][0],-1)
oldpoint=[-1,-1]
#display.displayscreen(whereamI)
oldbattery=1
while True:
    #display_battery() #display batter value
    #newbattery=battery.read()
    #display.showbattery(oldbattery,0)
    #display.showbattery(newbattery,1)
    if(whereamI==1): # Training Screen
        point = readSensor() 
        if(adddata):
            points.append(list(point))
            display.graph(oldpoint, point, points)
            print(points)
            
        elif(deletedata):
            if(points): #delete only when there is something
                points.pop()

                
        elif(run):
            whereamI=2 # trigger play screen
            nearestNeighbor(points,point)
            
        if(not point==oldpoint): #only when point is different now
            s.write_angle(point[1])
            display.graph(oldpoint, point, points)

        #reset all flags
        adddata=False
        deletedata=False
        save=False
        oldpoint=point

    elif(whereamI==2): # Play Screen
        point=readSensor()
        
        if(toggle):
            # put toggle function here
            pass
            
        elif(save):
            # save function here
            savetofile(points)
                
        elif(pause):
            #pause the data
            pass
            
            
        if(not point==oldpoint): #only when point is different now
            point = nearestNeighbor(points,point)
            print(point)
            s.write_angle(point[1])
            display.graph(oldpoint, point, points)

        #reset all flags
        add=False
        delete=False
        save=False
        oldpoint=point
    #time.sleep(1)
    #oldbattery=newbattery
    

