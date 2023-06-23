import gc
gc.collect()
import time
import servo

import ujson
import network
import ssd1306

import usocket as socket
import random as r
import re

import ubinascii
import ujson

from math import log
from machine import Pin, SoftI2C, PWM, ADC

from web import web_page

i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

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

# this is the dynamic training data 
training_data = []
# this is the training data that is read from the data file 
training_data_from_file = []
datafilename = "trainData.txt"

STATE = 1

# during test, saves the motor value associated with the sensor 
global_TEST_motor = 0
NN_index = -1

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
    print("SAVING DATA TO FILE")
    print(training_data)
    f=open("trainData.txt","w")
    length = len(training_data)
    for ind, val in enumerate(training_data):
        lightSensor = val[1]
        motor = val[0]
        f.write(str(lightSensor))
        f.write(",")
        f.write(str(motor))
        f.write('\n')
    f.close()

def removeData(i):
    global training_data
    print(training_data)
    if(len(training_data) != 0):
        training_data.pop(i)
        saveDataToFile()

# adds (motor, light) pair to training data 
def addData(motor, light):
    tup = (int(motor), int(light))
    global training_data
    training_data.append(tup)
    saveDataToFile()
  
# updates training_data_from_file
def updateDataReadFromFile(data_list):
    print("DATA READ FROM FILE RUN")
    print(data_list)
    global training_data_from_file
    training_data_from_file = data_list
  
def runData():
    sens = Sensor.read()
    sens = int((100 * int(t))/4095)
    light_val = []
    motor_val = []
    print("Trainging data from file ")
    print(training_data_from_file)
    for (mot, light) in training_data_from_file:
        dist = abs(sens - light)
        light_val.append(dist)
        motor_val.append(mot)
    # get the index of the least light_val
    global NN_index
    NN_index = light_val.index(min(light_val))
    pos = motor_val[NN_index]
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
        motor= as_list[1]
        light = as_list[0]
        tuples = (int(motor), int(light))
        data_tuples.append(tuples)
        updateDataReadFromFile(data_tuples)

def add_pair(light, motor):
    tup = (int(motor), int(light))
    global training_data
    training_data.append(tup)

# New function for displaying current values in text file 
# reads the file where each line is the motor,light data
# returns "motor,light;motor,light" as a string
# To avoid an error: If trainData.txt is empty make sure starts with line 1 
def readFile():
    with open("trainData.txt", "r") as values:
        lines = values.readlines()
    web_string = ""
    print(lines)
    print(len(lines))
    if (len(lines) > 0):
        for l in lines:
            print("IN READ FILE")
            print(l)
            as_list = l.split(",")
            motor= as_list[1]
            light = as_list[0].split('\n')[0]
            #add_pair(int(light), int(motor))
            addData(int(motor), int(light))
            web_string = web_string + motor + "," + light + ";"
    else:
        web_string = "0"
    print(training_data)
    return web_string
    
while True:
    try:
        conn, addr = s.accept()
        reply = web_page()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
            
        print('Content = %s' % request)
        
        if(STATE == 0):
            runData()
            
        # request to load the initial data that is stored  
        if request.find('/onLoad') == 6:
            # read current training data from file and send it to web browser
            reply = readFile()
            
        # setting the sensor reading     
        if request.find('/getDHT') == 6:
            t = read_sensor()
            x = int((100 * int(t))/4095)
    
            # if on testing, then send the nearest motor value 
            if (STATE == 0):
                motor_rotation = str(global_TEST_motor)
                NN_index_str = str(NN_index)
            # otherwise send "-1"
            else:
                motor_rotation = "-1"
                NN_index_str = "-1"
            # set sensor variable
            reply = str(x) + "|" + motor_rotation + "|" + NN_index_str
        
        if request.find('/slider') == 6:
            splitval = request.split("=", 1)
            number = splitval[1].split(" ", 1)
            value = number[0]
            motor.write_angle(180-int(value))
            
                
        if request.find('/?addvalue') == 6:
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
            split_values = request.split("=", 1)
            i = int(split_values[1].split(" ", 1)[0])
            print(i)
            removeData(i)
        
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



