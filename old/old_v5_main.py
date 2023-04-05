# COM speed 115200
# with SCL in D1 and SDA in D2

# SSD1306 GUIDE
#display.contrast(255)
#display.text('Hello, World!', 0, 0, 1)
#display.pixel(0, 0, 1)
#display.pixel(127, 63, 1)

#display.show()
#display.fill(0)
#display.show()
#display.hline(0, 8, 4, 1) # not working
#display.rect(10, 10, 107, 43, 1) # not working

from machine import Pin, SoftI2C, PWM, ADC
import time
import smarttools
import servo

i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
display = smarttools.SSD1306_SMART(128, 64, i2c)


bup = smarttools.BUTTON(8)
bselect = smarttools.BUTTON(9)
bdown = smarttools.BUTTON(10)

s = servo.Servo(Pin(2))

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






mode = 2
point = [9,9]
points = []


for i in range(0,70,4):
    None #display.rectangle(i, i, i+3, i+3)
#display.rectangle(0, 0, 123, 15)
#display.rectangle((45, 2), (88, 13))

#display.rectangle(0, 16, 123, 63)


#display.text('setup', 4, 4, 1)  # its rectangle is ((2, 2), (45, 13))
#display.text('train', 47, 4, 1) # its rectangle is ((45, 2), (88, 13))
#display.text('test', 90, 4, 1)  # its rectangle is ((88, 2), (123 13))
#display.show()




while(True):
    bdown.update()
    bselect.update()
    bup.update()


    
    
    if bdown.tapped:
        mode = (mode + 1) % 3
    if mode == 1:
        point = [transform('light', 'screenx', pot.read()), transform('pot', 'screeny', light.read())]
        s.write_angle(transform('pot', 'motor', pot.read()))
        if bselect.tapped:
            points.append(list(point))
        if bselect.held: # This is just a test
            points.append([point[0] - 15, point[1] - 15])
    elif mode == 2:
        point = [-20, -20]
    display.writeall(point, points, mode = mode)