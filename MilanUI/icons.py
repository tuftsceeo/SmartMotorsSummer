f=open('icons.py','w')
a='''
import framebuf
import ssd1306
from machine import Pin
import time

#define icons here

#*****************
#copy and paste this section and edit accordingly
# 
# direction = 0 or 1 # 0 means horizontal 1 means vertical
# iconSize= 12 # size of icons - square icons only supported
# offsetX = 0 # default is zero - where does the first icon appear in x axis
# offsetY =0 # default is zero - where does the first icon appear in Y axis

# returns (x,y,framebuf) of icons in an array
def createIcons(iconSize, iconFrames, offsetx=0, offsety=0, direction=0): 
    icons=[]
    padding=2
    spacingV=int((screenHeight - iconSize*len(iconFrames))/ (len(iconFrames))-padding)
    spacingH=int((screenWidth - iconSize*len(iconFrames))/ (len(iconFrames))-padding)
    
    for i in range(len(iconFrames)):
        Iconx=offsetx + i * (spacingH + iconSize) * ((direction+1)%2)
        Icony=offsety + i * (spacingV + iconSize) * ((direction)%2)

        icons.append([Iconx,Icony,iconFrames[i]])
        print(icons)
    return icons




#Homescreen icons
Icons=[]

screenWidth=128
screenHeight=64

#HomeScreen Icons
fb_Train = framebuf.FrameBuffer(bytearray(b"\x00\x0f\xf0\x00\x00p\x0e\x00\x01\xc0\x03\x80\x03\x00\x00\xc0\x04\x00\x00 \x08\xff\xff\x10\x10\x80\x01\x080\x80\x01\x0c \xe0\x01\x04a\xf0\x01\x06A\xf8\x01\x02C\xf8\x01\x02\x81\xf0\x01\x01\x81\xf0A\x01\x80\xe0\x81\x01\x81\xf1\x81\x01\x83\xfb\x01\x01\x83\xfe\x01\x01\x87\xfc\x01\x01\x87\xfc\x01\x01G\xff\xff\x02G\xfc\x00\x02g\xfc\x00\x06'\xfc\x00\x043\xf8\x00\x08\x13\xf8\x00\x08\t\xf0\x00\x10\x04\x00\x00 \x03\x00\x00\xc0\x01\xc0\x03\x00\x00p\x0e\x00\x00\x0f\xf0\x00"), 32, 32, framebuf.MONO_HLSB)
fb_Play = framebuf.FrameBuffer(bytearray(b'\x00\x0f\xf0\x00\x00p\x0e\x00\x01\xc0\x03\x80\x03\x00\x00\xc0\x04\x00\x00 \x08\x00\x00\x10\x10\x00\x00\x080\x00\x00\x0c \x00\x00\x04`\x08\x00\x06@\x0e\x00\x02@\x0f\x00\x02\x80\x0f\xc0\x01\x80\x0f\xf0\x01\x80\x0f\xfc\x01\x80\x0f\xfe\x01\x80\x0f\xfe\x01\x80\x0f\xf8\x01\x80\x0f\xf0\x01\x80\x0f\xc0\x01@\x0f\x00\x02@\x0e\x00\x02`\x08\x00\x06 \x00\x00\x040\x00\x00\x08\x10\x00\x00\x08\x08\x00\x00\x10\x04\x00\x00 \x03\x00\x00\xc0\x01\xc0\x03\x00\x00p\x0e\x00\x00\x0f\xf0\x00'), 32, 32, framebuf.MONO_HLSB)
fb_Setting = framebuf.FrameBuffer(bytearray(b'\x00\x0f\xf0\x00\x00p\x0e\x00\x01\xc0\x03\x80\x03\x00\x00\xc0\x04\x00\x00 \x08\x00\x00\x10\x10\x00\x00\x080\x030\x0c 7\xf0\x04`?\xfa\x06@?\xff\x02@\xfc>\x02\x81\xf0\x0e\x01\x80\xf0\x0f\x81\x80\xe0\x07\x81\x81\xe0\x07\x01\x83\xe0\x07\xc1\x80\xe0\x07\x81\x80\xf0\x0f\x01\x80\xf0\x0e\x01@\xfc?\x02@\xbf\xff\x02`\x1f\xf8\x06 ?\xf8\x040\x01\x90\x08\x10\x01\x00\x08\x08\x00\x00\x10\x04\x00\x00 \x03\x00\x00\xc0\x01\xc0\x03\x00\x00p\x0e\x00\x00\x0f\xf0\x00'), 32, 32, framebuf.MONO_HLSB)


#TrainScreen Icons
fb_Add = framebuf.FrameBuffer(bytearray(b'\xff\xf0\x80\x10\x80\x10\x86\x10\x86\x10\x9f\x90\x9f\x90\x86\x10\x86\x10\x80\x10\x80\x10\xff\xf0'), 12, 12, framebuf.MONO_HLSB)
fb_Delete = framebuf.FrameBuffer(bytearray(b'\xff\xf0\x80\x10\x80\x10\x90\x90\x89\x10\x86\x10\x86\x10\x89\x10\x90\x90\x80\x10\x80\x10\xff\xf0'), 12, 12, framebuf.MONO_HLSB)
fb_Run = framebuf.FrameBuffer(bytearray(b'\xff\xf0\x80\x10\xb0\x10\xbc\x10\xbe\x10\xbf\x90\xbf\x90\xbe\x10\xbc\x10\xb0\x10\x80\x10\xff\xf0'), 12, 12, framebuf.MONO_HLSB)
fb_Back = framebuf.FrameBuffer(bytearray(b'\xff\xf0\x80\x10\x80\x10\x83\x10\x86\x10\x8c\x10\x98\x10\x8c\x10\x86\x10\x83\x10\x80\x10\xff\xf0'), 12, 12, framebuf.MONO_HLSB)


#PlayScreen Icons
fb_toggle = framebuf.FrameBuffer(bytearray(b'\xff\xf0\x80\x10\x80\x10\xbc\x10\xa4\x10\xa7\x90\xa4\x10\xbc\x10\x80\x10\x80\x10\x80\x10\xff\xf0'), 12, 12, framebuf.MONO_HLSB)
fb_pause = framebuf.FrameBuffer(bytearray(b'\xff\xf0\x80\x10\x80\x10\x99\x90\x99\x90\x99\x90\x99\x90\x99\x90\x80\x10\x80\x10\x80\x10\xff\xf0'), 12, 12, framebuf.MONO_HLSB)
fb_Save = framebuf.FrameBuffer(bytearray(b'\xff\xf0\x80\x10\x80\x10\xbf\x10\xa2\x90\xa0P\xafP\xa9P\xa9P\xbf\xd0\x80\x10\xff\xf0'), 12, 12, framebuf.MONO_HLSB)
fb_home = framebuf.FrameBuffer(bytearray(b'\xff\xf0\x80\x10\x86\x10\x8f\x10\x9f\x90\xbf\xd0\x9f\x90\x99\x90\x99\x90\x99\x90\x80\x10\xff\xf0'), 12, 12, framebuf.MONO_HLSB)

#Add the icons to the array, add iconsizes add the direction 0 - horizontal , 1 - vertical
iconFrames=[[fb_Train,fb_Play,fb_Setting],[fb_Add,fb_Delete,fb_Run,fb_Back],[fb_toggle,fb_pause,fb_Save,fb_home]]
iconSize=[32,12,12]
offsets= [(5,20),(112,2),(112,2)] #where you want to display your first icon
direction=[0,1,1]                # 0 horizonal and 1 vertical arrangement

for index,icon in enumerate(iconFrames):
    icons = createIcons(iconSize[index], icon, offsetx=offsets[index][0], offsety=offsets[index][1] , direction=direction[index])
    Icons.append(icons)

print("Icons",Icons)


class SSD1306_SMART(ssd1306.SSD1306_I2C):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False, scale = 8, mode = 0, plotsize = [[3,3],[100,60]]):
        self.scale = scale
        self.mode = mode # 0 for learn, 1 for repeat
        self.plotsize = plotsize
        self.ranges = {'light': [0, 4095], 'motor': [0, 180], 'screenx': [4, 108], 'screeny': [59, 4]} # screeny is backwards because it is from top to bottom

        super().__init__(width, height, i2c, addr = 0x3C, external_vcc = external_vcc)

  
    def displayscreen(self,whereamI):    
        for IconX,IconY,frame in Icons[whereamI]:
            self.blit(frame, IconX, IconY, 0)
        self.show()

    def selector(self,whereamI,icon,previcon):
        padding=2
        width=height=iconSize[whereamI]+2*padding
        self.rect(Icons[whereamI][previcon][0]-padding,Icons[whereamI][previcon][1]-padding,width,height, 0) #delete previous selector icon
        self.rect(Icons[whereamI][icon][0]-padding,Icons[whereamI][icon][1]-padding,width,height, 1) #display current selector
        self.displayscreen(whereamI)
        self.show()
    
    def showbattery(self, batterylevel,on):
        self.text(str(batterylevel),1,40,on)
        self.show()
    def box(self,on, point,size):
        self.rect
    
    def transform(self,initial, final, value):
        initial = self.ranges[initial]
        final = self.ranges[final]
        return int((final[1]-final[0]) / (initial[1]-initial[0]) * (value - initial[0]) + final[0])
    
    def graph(self, oldpoint,point, points):
        rectsize=6
        dotsize=4
        ox,oy=oldpoint
        x,y=point
        ox=self.transform('light', 'screenx', ox)
        oy=self.transform('motor','screeny',oy)
        x=self.transform('light', 'screenx', x)
        y=self.transform('motor','screeny',y)
        
        self.rect(ox-int(rectsize/2),oy-int(rectsize/2),rectsize,rectsize,0)
        self.rect(x-int(rectsize/2),y-int(rectsize/2),rectsize,rectsize,1)
        for i in points:
            x,y=i
            x=self.transform('light', 'screenx', x)
            y=self.transform('motor','screeny',y)
            self.fill_rect(x-int(dotsize/2),y-int(dotsize/2),dotsize,dotsize,1)
        self.show()
'''
f.write(a)
f.close()




