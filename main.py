#APRIL 26 Commit Version

import gc
gc.collect()
import time
import servo

import ujson
import network
import smarttools

import usocket as socket
import random as r
import re

import ubinascii
import ujson

import random

from math import log
from machine import Pin, SoftI2C, PWM, ADC

from web import web_page

i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
display = smarttools.SSD1306_SMART(128, 64, i2c)


# connect servo
motor = servo.Servo(Pin(2))
motor.write_angle(90)

# sensor pin GPIO5
Sensor = ADC(Pin(5))
Sensor.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V

# this is the dynamic training data 
training_data = []
# this is the training data that is read from the data file 
training_data_from_file = []
datafilename = "trainData.txt"

# get mac address
mac = ubinascii.hexlify(network.WLAN().config("mac")).decode()
lastmac=bytearray(mac[-6:])
lastmac[5]=lastmac[5]+1
#SSID= 'ESP_'+lastmac.decode().upper()

chan = random.randrange(1, 11)
print("Using channel: ", chan)

# Enable Access Point
wlan=network.WLAN(network.AP_IF)
wlan.config(channel=chan)
wlan.active(False)
wlan.active(True)


# get SSID
SSID = wlan.config('essid')


# Wait for Connection and Update Display
display.text(SSID, 20,20,1)
display.show()
print("Waiting for connection...")
while (not wlan.isconnected()):
    time.sleep(1)

# Initialize Socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

# Wait 3 Seconds
display.fill(0)
display.text("Connecting .", 5,30,1)
display.show()
time.sleep(1)
display.text("Connecting ..", 5,30,1)
display.show()
time.sleep(1)
display.text("Connecting ...", 5,30,1)
display.show()
time.sleep(1)

display.fill(0)
display.show()
    
print("Wifi has been connected...")
display.text(SSID, 20,20,1)
print("Connect to IP address 192.168.4.1")
display.text("Now connect to", 10,40,1)
display.text("192.168.4.1", 20,50,1)
display.show()



STATE = 1 #STATE 1 = training, STATE 0 = testing/playing

# during test, saves the motor value associated with the sensor 
global_TEST_motor = 0

def updateStateTEST():
    global STATE
    if (STATE != 0):
        STATE = 0

def updateStateTRAIN():
    global STATE
    if (STATE != 1):
        STATE = 1
    
def read_sensor():
    sens = str(Sensor.read())
    return sens


# saves training_data to a file trainData.txt
# each line is motorData,lightSensor
def saveDataToFile():
    f=open("trainData.txt","w")
    length = len(training_data)
    for ind, val in enumerate(training_data):
        lightSensor = val[0]
        motor = val[1]
        f.write(str(motor))
        f.write(",")
        f.write(str(lightSensor))
        f.write('\n')
    f.close()

def removeData():
    global training_data
    if(len(training_data) != 0):
        training_data.pop()
        saveDataToFile()

# adds (motor, light) pair to training data 
def addData(motor, light):
    tup = (int(motor), int(light))
    global training_data
    training_data.append(tup)
    saveDataToFile()
  
# updates training_data_from_file
def updateDataReadFromFile(data_list):
    global training_data_from_file
    training_data_from_file = data_list
  
def runData():
    sens = Sensor.read()
    sens = int((100 * int(t))/4095)
    light_val = []
    motor_val = []
    for (light, mot) in training_data_from_file:
        dist = abs(sens - light)
        light_val.append(dist)
        motor_val.append(mot)
    # get the index of the least light_val
    index = light_val.index(min(light_val))
    pos = motor_val[index]
    print("SENSOR VALUE IS...")
    print(sens)
    print("MOTOR VALUE ROTATE TO IS...")
    print(pos)
    global global_TEST_motor
    global_TEST_motor = pos
    motor.write_angle(180-pos)
    
# reads the file where each line is the motor,light data
# returns [(motor,light), (motor,light)]
def readFileAndStoreData(filename):
    with open("trainData.txt", "r") as values:
        lines = values.readlines()
    data_tuples = []
    for l in lines:
        as_list = l.split(",")
        motor= as_list[0]
        light = as_list[1]
        tuples = (int(motor), int(light))
        data_tuples.append(tuples)
        updateDataReadFromFile(data_tuples)
    
while True:
    try:
        conn, addr = s.accept()
        reply = web_page()
        
        #heartbeat
        if addr[1]%10<5:
            display.rect(0,0,2,2,1)
            display.show()
        else:
            display.rect(0,0,2,2,0)
            display.show()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
            
        #print('Content = %s' % request)
        
        if(STATE == 0):
            runData()
            
        # setting the sensor reading     
        if request.find('/getDHT') == 6:
            
            t = read_sensor()
            x = int((100 * int(t))/4095)
            print("Read Sensor:", x)
    
            # if on testing, then send the nearest motor value 
            if (STATE == 0):
                motor_rotation = str(global_TEST_motor)
            # otherwise send "-1"
            else:
                motor_rotation = "-1"
            # set sensor variable
            reply = str(x) + "|" + motor_rotation 
        
        if request.find('/slider') == 6:
            
            splitval = request.split("=", 1)
            number = splitval[1].split(" ", 1)
            value = number[0]
            print("Move Motor: ", value)
            motor.write_angle(180-int(value))
            
                
        if request.find('/?addvalue') == 6:
            print("Add Value")
            # request comes in form /?addvalue="+sliderValue+"="+sensorValue
            split_values = request.split("=", 1)
            motor_light = split_values[1].split(" ", 1)[0]
            mot_val_save = motor_light.split("=")[0]
            lit_val_save = motor_light.split("=")[1]
            print(mot_val_save)
            print(lit_val_save)
            addData(int(mot_val_save), int(lit_val_save))
                
        # removes the last data from the list    
        if request.find('/?deletevalue') == 6:
            print("Delete Value")
            removeData()
        
        if request.find('/?test') == 6:
            print("TEST clicked")
            # read the data from the file
            updateStateTEST()
            readFileAndStoreData(datafilename)
        
        if request.find('/?stop') == 6:
            print("STOP clicked")
            # read the data from the file
            updateStateTRAIN()
            
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(reply)
        conn.close()       
        
    except Exception as e:
        print("Main Loop Exception - ERROR")
        print(e)
        break
gc.collect()

display.fill(0) # Clear Screen before Error
display.show()

display.text("Error - Restart", 20,20,1)
display.show()
s.close()



