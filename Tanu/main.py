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

from math import log
from machine import Pin, SoftI2C, PWM, ADC

from web import web_page

i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
display = smarttools.SSD1306_SMART(128, 64, i2c)

# connect to wifi 
wlan=network.WLAN(network.AP_IF)
wlan.active(False)
wlan.active(True)

mac = ubinascii.hexlify(network.WLAN().config("mac")).decode()
lastmac=bytearray(mac[-6:])
lastmac[5]=lastmac[5]+1
SSID= 'ESP_'+lastmac.decode().upper()

display.text(SSID, 20,20,1)
display.show()
print("Waiting for connection...")
while (not wlan.isconnected()):
    time.sleep(1)
    
print("Wifi has been connected...")
print("Connect to ip address 192.168.4.1")
display.text(SSID, 20,20,1)
display.text("Now connect to", 10,30,1)
display.text("192.168.4.1", 20,50,1)
display.show()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

# CODE below is for Web Server
# connect servo
motor = servo.Servo(Pin(2))
motor.write_angle(90)

# light pin GPIO5
Sensor = ADC(Pin(5))
Sensor.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V

global_sensor_data = 0
global_motor_data = 0

# this is the dynamic training data 
training_data = []
# this is the training data that is read from the data file 
training_data_from_file = []
datafilename = "trainData.txt"

STATE = 1

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

def updateSensor(data):
    global global_sensor_data
    global_sensor_data = data

def updateMotor(data):
    global global_motor_data
    global_motor_data = data
    print("global motor data changed to...")
    print(global_motor_data)

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
    motor.write_angle(pos)
    
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
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
            
        print('Content = %s' % request)
            
        # setting the sensor reading     
        if request.find('/getDHT') == 6:
            t = read_sensor()
            x = int((100 * int(t))/4095)
            updateSensor(x)
            # set sensor variable
            reply = str(x) + "|"
        
        if(STATE == 0):
            runData()
        
        if request.find('/slider') == 6:
            splitval = request.split("=", 1)
            number = splitval[1].split(" ", 1)
            value = number[0]
            motor.write_angle(180-int(value))
            # set motor variable 
            updateMotor(180-int(value))
                
        if request.find('/?addvalue') == 6:
            # write the data to the file
            t = read_sensor()
            x = int((100 * int(t))/4095)
            updateSensor(x)
            addData(global_motor_data, global_sensor_data)
                
        # removes the last data from the list    
        if request.find('/?deletevalue') == 6:
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
        print(e)
        break
gc.collect()
display.text("Error encountered", 20,20,1)
display.show()
s.close()

