from machine import Pin, SoftI2C, PWM, ADC
import time
import smartssd1306

i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
display = smartssd1306.SSD1306_I2C(128, 64, i2c)

display.text("hello", 0, 0, 1)
display.show()