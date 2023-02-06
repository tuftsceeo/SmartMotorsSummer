# COM speed 115200
# with SCL in D1 and SDA in D2
# desktop COM9
# laptop  COM11


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

# OTHER TOOLS GUIDE
#import os
#os.remove("main.py")
#os.listdir()
#f = open("main.py", "w")
#f.write(a)
#f.close()
#hit control D to restart the board.


#no longer needed:
#import framebuf
#import ssd1306


#from machine import Pin, I2C
#import ssd1306
#i2c = I2C(sda = Pin(4), scl = Pin(5))
#display = ssd1306.SSD1306_I2C(128, 64, i2c)

from time import sleep
from random import getrandbits

from machine import Pin, I2C
import aengussd1306
i2c = I2C(sda = Pin(4), scl = Pin(5))
#screen = SSD1306_I2C(128, 64, i2c)
#display = SSD1306_SMART(128, 64, i2c, scale = 8)
display = aengussd1306.SSD1306_SMART(128, 64, i2c, scale = 8)


def changepointrandomly(point, scale):
	if(getrandbits(1)):
		if(getrandbits(1) and point[0] < 128/scale - 1):
			return [point[0] + 1, point[1]]
		elif(point[0] > 0):
			return [point[0] - 1, point[1]]
	else:
		if(getrandbits(1) and point[1] < 64/scale - 4): # used to be 64/scale - 1, but was changed to - 4 because of the 'learn' text
			return[point[0], point[1] + 1]
		elif(point[1] > 0):
			return[point[0], point[1] - 1]
	return point



points = []
point = [0,0]


while(True):
	point = changepointrandomly(point, display.scale)
	display.update(points, point)
	if(getrandbits(3) == 0):
		test = [i[0] for i in points]
		if(not point[0] in test):
			points.append(point)


	sleep(getrandbits(2)/6)
	if(getrandbits(7) == 0):
		display.mode = 1
		display.update(points, [])
		break
