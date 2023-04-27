# This is a modification to the ssd1306.py package that includes 
# the superclass SSD1306_SMART with many graphics functions for the smart motor.

# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
import framebuf
import ssd1306
from machine import Pin
import time


class BUTTON(Pin):
    def __init__(self, pin, holdthreshold = 500):
        self.holdthreshold = holdthreshold # the number of miliseconds before a 'tap' becomes a 'hold'
        self.lastup = False # This is False if the button is up and equal to time.ticks_ms() when the button was pressed if down
        self.tapped = False # This becomes True for one update after the button is released for less than holdthreshold
        self.held = False   # This becomes True for one update after the button has been held for more than holdthreshold
        self.stillheld = False # This becomes and stays True if the button is held for more than holdthreshold
        super().__init__(pin, Pin.IN) # inherits self.value() which is 1 if not pressed, 0 if pressed
    def update(self):
        if self.value() == 1: # not pressed
            if self.lastup == False: # not pressed and was never pressed
                self.tapped = False
                self.held = False
                self.stillheld = False
            elif time.ticks_ms() - self.lastup < self.holdthreshold: # not pressed, but just released from tap
                self.lastup = False
                self.tapped = True
                self.held = False
                self.stillheld = False
            else: # not pressed, but just released from hold
                self.lastup = False
                self.tapped = False
                self.held = False
                self.stillheld = False
        else: # pressed
            if self.lastup == False: # This is the first update it was pressed
                self.lastup = time.ticks_ms()
                self.tapped = False
                self.held = False
                self.stillheld = False
            elif time.ticks_ms() - self.lastup < self.holdthreshold: # It has not been long enough for a hold
                pass
            else: # The button has been held
                if self.stillheld == False: # This is the first update since it was held
                    self.tapped = False
                    self.held = True


                    self.stillheld = True
                else: # It has been held for a while
                    self.held = False

class SSD1306_SMART(ssd1306.SSD1306_I2C): #<-----added framebuf by wchurch 4/12/2023
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
        if mode == 0:
            self.rectangle((124 - 8*4, 10), (127, 21))
        if mode == 1:
            self.rectangle((124 - 8*5, 26), (127, 37))
        if mode == 2:
            self.rectangle((124 - 8*4, 42), (127, 53))
        
        # x from (123 - 8 * letters) to 127
        # y values: 10 to 21

        #           26 to 37
        #           42 to 53
        
    def writewords(self, mode, iterator): # <---- WChurch added iterator 4/19/2023 to help with the animation
        orientation = 'vertical'
        zero_or_one = 0 #<----- used to animate a dot showing the mode you are in
        del_factor = 5 #< ---- used to slow/speed up animation
        # define framebuffers for graphics
        gear_buf = framebuf.FrameBuffer(bytearray(b'\x0f\x00\t\x00p\xe0\x00\x00\x8f\x10I I \x8f\x10\x00\x00p\xe0\t\x00\x0f\x00'), 12, 12, framebuf.MONO_HLSB)
        train_buf = framebuf.FrameBuffer(bytearray(b'\xff\xf0\x00\x10`\x10\x90\x10`\x10\x01\x10F\x10\xf8\x10\xf0\x10\xe3\xf0\xe0\x00\xe0\x00'), 12, 12, framebuf.MONO_HLSB)
        play_buf = framebuf.FrameBuffer(bytearray(b'\x0f\x00 @@ \x00\x00\x8c\x10\x8a\x10\x89\x10\x8a\x10\x0c\x00@  @\x0f\x00'), 12, 12, framebuf.MONO_HLSB)
        fb_dot0 = framebuf.FrameBuffer(bytearray(b' P\x88P '), 5, 5, framebuf.MONO_HLSB)
        fb_dot1 = framebuf.FrameBuffer(bytearray(b'\x00 p \x00'), 5, 5, framebuf.MONO_HLSB)

        # check orientation and display menu items
        if orientation == 'vertical':
            self.blit(gear_buf, 140-8*4, 12)
            self.blit(train_buf, 148-8*5, 28)
            self.blit(play_buf,138-8*4, 44)

            # display graphic to show which mode is currently selected
            if mode == 0:
                if (iterator%del_factor == 0):
                    self.blit(fb_dot0,124 - 8*3, 10)
                else:
                    self.blit(fb_dot1,124 - 8*3, 10)
            if mode == 1:
                if (iterator%del_factor == 0):
                    self.blit(fb_dot0,124 - 8*3, 26)
                else: 
                    self.blit(fb_dot1,124 - 8*3, 26)
            if mode == 2:
                if (iterator%del_factor == 0):
                    self.blit(fb_dot0,124 - 8*3, 42)
                else:
                    self.blit(fb_dot1,124 - 8*3, 42)
                
        print (iterator)

        if orientation == 'horizontal':
            self.text('setup', 4, 4, 1)  # its rectangle is ((2, 2), (45, 13))
            self.text('train', 47, 4, 1) # its rectangle is ((45, 2), (88, 13))
            self.text('test', 90, 4, 1)  # its rectangle is ((88, 2), (123, 13))
            if mode == 0 or mode == 'setup':
                self.rectangle((2, 2), (45, 13))
            if mode == 1 or mode == 'train':
                self.rectangle((45, 2), (88, 13))
            if mode == 2 or mode == 'test':
                self.rectangle((88, 2), (123, 13))

        return iterator 


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
        
    def writeall(self, point, points, mode, iterator):


        self.fill(0)
        self.writewords(mode,iterator)
        orientation = 'vertical'
        if orientation == 'vertical':
            self.rectangle((0, 0), (84, 63))
        elif orientation == 'horizontal':
            self.rectangle((0, 16), (127, 63))
        self.box7(point)
        for i in points:
            self.plot3(i)
        self.show()