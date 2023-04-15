# This is a modification to the ssd1306.py package that includes 
# the superclass SSD1306_SMART with many graphics functions for the smart motor.
# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
f=open('smarttools.py','w')
a='''
import ssd1306
from machine import Pin


class BUTTON(Pin):
    def __init__(self, pin, holdthreshold = 30):
        self.holdthreshold = holdthreshold
        self.holdcount = 0
        self.tapped = False
        self.held = True
        super().__init__(pin, Pin.IN, Pin.PULL_UP)
    def update(self):
        if self.value() == 1: # not pressed
            if self.holdcount > 0 and not self.held:
                self.tapped = True
            else:
                self.tapped = False
            self.held = False
            self.holdcount = 0
        if self.value() == 0: # pressed
            self.holdcount += 1
            if self.holdcount >= self.holdthreshold:
                self.held = True
            else:
                self.held = False
            self.tapped = False

class SSD1306_SMART(ssd1306.SSD1306_I2C):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False, scale = 8, mode = 0, plotsize = [[3,3],[100,60]]):
        self.scale = scale
        self.mode = mode # 0 for learn, 1 for repeat
        self.plotsize = plotsize
        super().__init__(width, height, i2c, addr = 0x3C, external_vcc = external_vcc)

    def hline(self, *args):

        if len(args) == 3:
            x, y, length = args
            for i in range(x, x + length):
                self.pixel(i, y, 1)
        if len(args) == 4:
            x1, y1, x2, y2 = args
            def f(x):
                return int((y2-y1)/(x2-x1)*(x-x1) + y1)
            for i in range(x1, x2 + 1):

                self.pixel(i, f(i), 1)

        return None

    def vline(self, *args):
        if len(args) == 3:

            x, y, length = args
            for j in range(y, y + length):
                self.pixel(x, j, 1)
        if len(args) == 4:
            x1, y1, x2, y2 = args
            def f(y):

                return int((x2-x1)/(y2-y1)*(y-y1) + x1)
            for j in range(y1, y2 + 1):
                self.pixel(f(j), j, 1)

        return None
        
    def rectangle(self, *args):
        if len(args) == 2:
            x1, y1, x2, y2 = args[0][0], args[0][1], args [1][0], args[1][1]
        if len(args) == 4:
            x1, y1, x2, y2 = args[0], args[1], args[2], args[3]
        self.hline(x1, y1, x2, y1)



        self.hline(x1, y2, x2, y2)
        self.vline(x1, y1 + 1, x1, y2 - 1)
        self.vline(x2, y1 + 1, x2, y2 - 1)

    
    def filled(self, *args):
        if len(args) == 2:

            x1, y1, x2, y2 = args[0][0], args[0][1], args [1][0], args[1][1]
        elif len(args) == 4:
            x1, y1, x2, y2 = args

        else:
            return None
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                self.pixel(i, j, 1)

    def box7(self, *args):
        if len(args) == 1:
            x, y = args[0]

        elif len(args) == 2:
            x, y = args
        self.rectangle((x - 3, y - 3), (x + 3, y + 3))

    def box9(self,*args):
        if len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        self.rectangle((x - 4, y - 4), (x + 4, y + 4))
    
    def plot3(self, *args):
        if len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        self.filled((x - 1, y - 1), (x + 1, y + 1))
    

    def plot5(self, *args):
        if len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        self.filled((x - 2, y - 2), (x + 2, y + 2))

    
        
    def oldwritewords(self, mode):
        self.text('edit', 126-8*4, 12, 1)
        self.text('train', 126-8*5, 28, 1)
        self.text('test', 126-8*4, 44, 1)
        if mode == 1:
            self.rectangle((124 - 8*4, 10), (127, 21))
        if mode == 2:
            self.rectangle((124 - 8*5, 26), (127, 37))
        if mode == 3:

            self.rectangle((124 - 8*4, 42), (127, 53))
        
        # x from (123 - 8 * letters) to 127
        # y values: 10 to 21

        #           26 to 37
        #           42 to 53
        
    def writewords(self, mode):
        self.text('setup', 4, 4, 1)  # its rectangle is ((2, 2), (45, 13))
        self.text('train', 47, 4, 1) # its rectangle is ((45, 2), (88, 13))
        self.text('test', 90, 4, 1)  # its rectangle is ((88, 2), (123, 13))
        if mode == 0 or mode == 'setup':
            self.rectangle((2, 2), (45, 13))
        if mode == 1 or mode == 'train':
            self.rectangle((45, 2), (88, 13))
        if mode == 2 or mode == 'test':
            self.rectangle((88, 2), (123, 13))
        
        # x from (123 - 8 * letters) to 127
        # y values: 10 to 21

        #           26 to 37
        #           42 to 53

    def hplot(self, *args):

        if len(args) == 1:

            f = args[0]
            for i in range(self.width):
                try:
                    display.pixel(i, int(f(i)), 1)
                except (ValueError, ZeroDivisionError):

                    pass
        return None

    def vplot(self, *args):
        if len(args) == 1:
            f = args[0]

            for j in range(self.height):
                try:

                    display.pixel(int(f(j)), j, 1)
                except (ValueError, ZeroDivisionError):
                    pass
        return None
        
    def writeall(self, point, points, mode):

        self.fill(0)
        self.writewords(mode)
        self.rectangle((0, 16), (127, 63))
        self.box7(point)
        for i in points:
            self.plot3(i)
        self.show()
        
'''
f.write(a)
f.close()