
from machine import Pin, SoftI2C, PWM, ADC
import time
from machine import Timer
#import smarttools
import servo
import icons
import os
import sys
import ubinascii
import machine
    
import bleFunctions
import bluetooth


import sensors
sens=sensors.SENSORS()

#unique name 
ID= ubinascii.hexlify(machine.unique_id()).decode()


STATE=[[0,3],[0,4],[0,4],[0,4],[0,3]] #[homescreen, trainscreen, playscreen, playthefilesscreen, settingsscreen]
whereamI=0
wherewasI=-1
whenPressed=0
prev=0
filenumber=0

point = [9,9]
points = []


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
#3 - Playthefiles
#4 - ConnectSCREEN


#Defining all flags
#Train screen flags
adddata=False
deletedata=False
run=False

#Play screen flags
toggle=False
pause=False

#Play files screen flags
prev=False
nxt=False
load=False

#Settings screen flags
leader=False
follower=False


#switch flags
switch_state_up = False 
switch_state_down = False 
switch_state_select = False 

last_switch_state_up = False
last_switch_state_down = False
last_switch_state_select = False

switched_up = False
switched_down = False
switched_select = False


#mainloop flags
clearscreen=False

i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
display = icons.SSD1306_SMART(128, 64, i2c)



#define buttons , sensors and motors
#servo
s = servo.Servo(Pin(2))

#nav switches
switch_down = Pin(8, Pin.IN)
switch_select = Pin(9, Pin.IN)
switch_up= Pin(10, Pin.IN)


#interrupt functions
def downpressed(count=-1):
    time.sleep(0.1)
    if(time.ticks_ms()-whenPressed>500):
        displayselect(count)

    
def uppressed(count=1):
    time.sleep(0.1)
    if(time.ticks_ms()-whenPressed>500):
        displayselect(count)


def displayselect(count):
    global whereamI
    global STATE
    global whenPressed
    global changed
    global prev

    STATE[whereamI][0]=(STATE[whereamI][0]+count)%STATE[whereamI][1]
    display.selector(whereamI,STATE[whereamI][0],prev) #draw circle at selection position, and remove from the previous position
    prev=STATE[whereamI][0]
    changed=True
    whenPressed=time.ticks_ms()
    
def selectpressed():
    global points
    time.sleep(0.3)
    #declare all global variables, include all flags
    global whereamI
    global state
    global whenPressed
    global adddata
    global deletedata
    global save
    global run
    global toggle
    global pause
    global prev
    global nxt
    global load
    global clearscreen
    global leader
    global follower
    
    #iconFrames=[[fb_Train,fb_Play,fb_Setting],[fb_add,fb_delete,fb_smallplay,fb_home],[fb_save,fb_pause,fb_home,fb_toggle],[fb_next,fb_home,fb_toggle]]
    #Home screen
    if(whereamI==0):
        if(STATE[0][0]==0):
            whereamI=1      #Train Screen
        elif(STATE[0][0]==1):
            whereamI=3      #select the play Screen   - with choices of dataset
        elif(STATE[0][0]==2):
            #display.showmessage("Coming soon")
            print("going to setting")
            whereamI=4     #Settings Screen - ble connection, wifi, etc.
            prev=0
        display.fill(0)
        display.selector(whereamI,STATE[whereamI][0],-1)
        #display.displayscreen(whereamI)
        
    #Train screen
    elif(whereamI==1): 
        if(STATE[whereamI][0]==0): #add data point    
            adddata=True         
        elif(STATE[whereamI][0]==1):#delete data point
            deletedata=True 
        elif(STATE[whereamI][0]==2): #run using the train data
            if (points):
                whereamI=2
            else:
                display.showmessage("No data to run")
                clearscreen=True
        elif(STATE[1][0]==3): # go back to homescreen
            resettohome()
            clearscreen=True

        display.selector(whereamI,STATE[whereamI][0],-1) # load the selector on relevant icon

        
    #Play screen 
    elif(whereamI==2): 
        if(STATE[whereamI][0]==0): # save data
            save=True    
        elif(STATE[whereamI][0]==1):  # pause the run 
            pause=True  
        elif(STATE[whereamI][0]==2): #go home
            resettohome()
            clearscreen=True
        elif(STATE[whereamI][0]==3):# toggle screeen view
            toggle=True
        

        display.selector(whereamI,STATE[whereamI][0],-1) # load the selector on relevant icon

        
    #Play the files screen 
    elif(whereamI==3): 
        if(STATE[whereamI][0]==0): # show next data 
            nxt=True
        elif(STATE[whereamI][0]==1): #delete dataset
            deletedata=True

        elif(STATE[whereamI][0]==2): #go home
            resettohome()
            clearscreen=True
        elif(STATE[whereamI][0]==3): #toggle
            toggle=True     
        
        display.fill(0) # clear screen
        display.selector(whereamI,STATE[whereamI][0],-1) # load the selector on relevant icon


    #Settings screen
    elif(whereamI==4):
        print("I was checked")
        if(STATE[whereamI][0]==0): # look for followers
            leader=True
        elif(STATE[whereamI][0]==1): # look for leaders
            follower=True
        elif(STATE[whereamI][0]==1): # Go home
            resettohome()
            clearscreen=True
        
        display.fill(0) # clear screen
        display.selector(whereamI,STATE[whereamI][0],-1) # load the selector on relevant icon

        
#call back to check the button presses
        
def resettohome():
    global whereamI
    global STATE
    global points
    global prev
    whereamI=0      
    STATE=[[0,3],[0,4],[0,4],[0,4],[0,4]]
    #display.fill(0) # clear screen
    points=[]
    prev=0
    
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
         
    if switch_state_up != last_switch_state_up:
        switched_up = True
        
    elif switch_state_down != last_switch_state_down:
        switched_down = True
        
    elif switch_state_select != last_switch_state_select:
        switched_select = True
        
        
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
    
    last_switch_state_up = switch_state_up
    last_switch_state_down = switch_state_down
    last_switch_state_select = switch_state_select



def displaybatt(p):
    batterycharge=sens.readbattery()
    display.showbattery(batterycharge)
    return batterycharge
    


def mappot(value):
    initial = [0, 4095]
    final =  [0, 180]
    return int((final[1]-final[0]) / (initial[1]-initial[0]) * (value - initial[0]) + final[0])


def fakebattery(value):
    initial = [0, 180]
    final =  [2600, 2900]
    return int((final[1]-final[0]) / (initial[1]-initial[0]) * (value - initial[0]) + final[0])



def savetofile(pointstosave):
    import os
    if(os.listdir().count('data.py')):
        import data
        datapoints=[]
        del sys.modules["data"]
        import data
        try:
            datapoints=data.points
            datapoints.append(pointstosave)
        except:
            datapoints.append(pointstosave)
        del sys.modules["data"]
        #getting ready to reimporting data file
    else:
        datapoints=[]
        datapoints.append(pointstosave)
        print("new file")
    #writing files to the data.py
    
    f=open("data.py","w")
    f.write("points="+str(datapoints)+"\r\n")
    f.close()

def replacefile(pointstosave):
    import os
    if(os.listdir().count('data.py')):
        f=open("data.py","w")
        f.write("points="+str(pointstosave)+"\r\n")
        f.close()
    else:
        return 0

    
def readfile():
    global clearscreen
    import os
    if(os.listdir().count('data.py')):
        import data
        if(data.points):
            return(data.points)
        else:
            display.showmessage("No data saved")
            resettohome()
            clearscreen=True
            return([])
    else:
        display.showmessage("No data saved")
        resettohome()
        clearscreen=True
        return([])
    
        #also make this go home



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





def on_scan(addr_type, addr, name):
    if addr_type is not None:
        print("Found sensor:", addr_type, addr, name)
        #central.connect()

    else:
        print("I don't know what this is")

def on_rx():
    print("rx: ", uart.read().decode().strip())
            
def broadcast(point, LEVEL0 , LEVEL1, displayMessage = "" ):
    uart.write(str(point)+str(LEVEL0)+str(LEVEL1)+ str(displaybatt(1))+ displayMessage)
    
def closeconn():
    uart.close()

def waitforconnection():
    print("waiting")
    
    
    
    
#setting up Timers
tim = Timer(0)
tim.init(period=50, mode=Timer.PERIODIC, callback=check_switch)
batt = Timer(2)
batt.init(period=500, mode=Timer.PERIODIC, callback=displaybatt)

#setting up BLE irq


display.welcomemessage()

#bluetooth functions

ble = bluetooth.BLE()
uart = bleFunctions.BLEUART(ble)
#uart.scan(callback=on_scan)
uart.irq(handler=on_rx)

#setup with homescreen  #starts with whereamI=0
display.selector(whereamI,STATE[whereamI][0],-1)
oldpoint=[-1,-1]
oldbattery=1

while True:
    point = sens.readpoint()
    broadcast(point, whereamI, STATE[whereamI][0],ID)

    if(whereamI==1): # Training Screen
        if(adddata):
            points.append(list(point))
            display.graph(oldpoint, point, points)
            
        elif(deletedata):
            if(points): #delete only when there is something
                points.pop()
            display.cleargraph()
            display.graph(oldpoint, point, points)
                
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
        if(toggle):
            # put toggle function here - create a dashboard view
            pass
            
        elif(save):
            # save function here
            savetofile(points)
            uppressed(count=2)
                
        elif(pause):
            #pause the data
            pass
            
            
        if(not point==oldpoint): #only when point is different now
            
            point = nearestNeighbor(points,point)
            s.write_angle(point[1])
            display.graph(oldpoint, point, points)
    
        oldpoint=point
        #reset all flags
        toggle=False
        save=False
        pause=False

    
    elif(whereamI==3): # Load saved files screen
        datapoints=readfile()
        if(datapoints):
            numberofdata=len(datapoints)
            points=datapoints[filenumber]
            if(nxt):
                filenumber=((filenumber+1)%numberofdata)
                points=datapoints[filenumber]
                display.cleargraph()
            elif(deletedata):
                del datapoints[filenumber]
                replacefile(datapoints)
                filenumber=0
                display.cleargraph()
                

            elif(toggle):
                #toggle the screen
                pass
       
            if(not point==oldpoint): #only when point is different now
                point = nearestNeighbor(points,point)
                s.write_angle(point[1])
                display.graph(oldpoint, point, points)
                
            oldpoint=point
            #reset all flags
            
            deletedata=False
            nxt=False
            toggle=False
            
        
    elif(whereamI==4): # Settings Screen
        if(leader):
            display.showmessage(ID)
            waitforconnection()
            
        elif(follower):
            
            print("I shall follow you")
            
        oldpoint=point
        #reset all flags
        
        leader=False
        follower=False


    oldpoint=point
    #time.sleep(1)
    #oldbattery=newbattery
    if clearscreen:
        #display.clearscreen()
        display.fill(0)
        display.selector(whereamI,STATE[whereamI][0],-1)
        clearscreen=False



