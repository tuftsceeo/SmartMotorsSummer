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
import smartssd1306

i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
display = smartssd1306.SSD1306_SMART(128, 64, i2c)

mode = 2
point = [9,9]
points = []

def writeall():
# plot ranges from 4,4 to 78, 59 for the box not to overlap with the border
    display.fill(0)
    display.writewords(mode)
    display.rectangle((0, 0), (82, 63))
    
    display.box7(point)
    for i in points:
        display.plot3(i)

    display.show()



while(True):
    for i in range(8):
        point[0] += 2*i
        writeall()
    
    points.append(list(point))
    for i in range(8):
        point[0] -= 2*i
        point[1] += 5
        writeall()
    points.append(list(point))
    
    for i in range(8):
        point[1] -= 5
        writeall()
    points.append(list(point))
        
    for i in range(10):
        point[0] += 5
        point[1] +=4
        writeall()
    points.append(list(point))
        
    for i in range(10):
        point[0] -= 5
        point[1] -=4
        writeall()
    points.append(list(point))
    
    for i in (3, 1, 2):
        mode = i
        writeall()
        time.sleep(0.3)
    