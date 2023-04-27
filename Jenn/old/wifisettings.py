import ssd1306
import network

class SELECTOR():
    def __init__(self, screen, width, height, x, y, options):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.options = options
        self.selectedchar = 0
        self.active = False
    
    
    def draw_top_char(self):
        pass
    def draw_main_char(self):
        pass
    def draw_bottom_char(self):
        pass
    
    def draw():
        pass
    def draw_inactive(self):
        pass
    def draw_active(self):
        pass
    
    def char_up(self):
        pass
    def char_down(self):
        pass
    def grab_char(self):
        pass

def do_connect(ssid = "Tufts_Wireless", key=''):
    print('attempting network connection')
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, key)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
do_connect()