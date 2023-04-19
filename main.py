# COM speed 115200
# with SCL in D1 and SDA in D2
#
###############
# Smart Motors Main.py code v7, April 19, 2023, bchurch edits
###############

from machine import Pin, SoftI2C, PWM, ADC
import time
import smarttools
import servo
import smartfunctions

# create our dipslay object from smarttools module
i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
display = smarttools.SSD1306_SMART(128, 64, i2c)

# create our button user interface objects from smarttools module
bup = smarttools.BUTTON(8)
bselect = smarttools.BUTTON(9)
bdown = smarttools.BUTTON(10)

# create our servo, potentiometer, and light sensor objects
s = servo.Servo(Pin(2))
pot = ADC(Pin(3))
pot.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V
light = ADC(Pin(5))
light.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V

# Create a range mapping function because we seek to plot values of different ranges (poteniometer of 0 to 4095) on the same scale as a range of the motor (0 to 180) and on a different scale for the screen (screenx and screeny)
ranges = {'pot': [0, 4095], 'light': [0, 4095], 'motor': [0, 180], 'screenx': [4, 123], 'screeny': [59, 20], 'oldscreenx': [4, 78], 'oldscreeny': [59, 4]} # screeny is backwards because it is from top to bottom
def transform(initial, final, value):
    initial = ranges[initial]
    final = ranges[final]
    return int((final[1]-final[0]) / (initial[1]-initial[0]) * (value - initial[0]) + final[0])

# Define variables used in the main while loop
mode = 0
point = [9,9]
points = []
iterator = 0 #<---- for selector animation in smarttools module

# Main  while loop
while(True):
    # check to see if we have any button presses
    bdown.update()
    bselect.update()
    bup.update()

    # act on button presses to change the mode from 0 (settings) to 1 (training) to 2 (play/test training model)
    if bdown.tapped or bselect.held:
        mode = (mode + 1) % 3
    if mode == 1:  #<------ training
        point = [transform('light', 'oldscreenx', light.read()), transform('pot', 'oldscreeny', pot.read())]  #<---- define current point based on measured values of the potentiometer and light sensor
        s.write_angle(transform('pot', 'motor', pot.read()))  #<----- move motor to position cooresponding to the potentiometer
        if bselect.tapped:
            points.append(list(point))   #<------ add data point to training list
    elif mode == 2:  #<------- play/test training model
        point = [transform('light', 'oldscreenx', light.read()), -20]   #<----- define current point
        motor_position =  smartfunctions.nearestNeighbor(points, point)  #<----- get cooresponding motor via nearest neighbor algorithm
        s.write_angle(transform('oldscreeny', 'motor', motor_position))   #<----- move motor accordingly
        point = [transform('light', 'oldscreenx', light.read()), motor_position]  #<---- define a new point to show a live data box around on the graph
    elif mode == 0:
        pass   # fucntion for settings mode not defined yet
    display.writeall(point, points, mode, iterator)  #<----- display everything
    iterator += 1


