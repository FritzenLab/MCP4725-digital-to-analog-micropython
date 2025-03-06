# MCP4725 library: https://github.com/wayoda/micropython-mcp4725
from machine import Pin, SPI
import gc9a01py as gc9a01
from machine import I2C
import time
import mcp4725
from mcp4725 import MCP4725, BUS_ADDRESS
import sys
import uselect

i2c = I2C(id=0, scl=5, sda=4, freq=400_000)

initialtime= time.ticks_ms() #https://docs.micropython.org/en/latest/library/time.html
    
def main():
    
    spi = SPI(0, baudrate=60000000, sck=Pin(18), mosi=Pin(19))
    tft = gc9a01.GC9A01(
        spi,
        dc=Pin(20, Pin.OUT),
        cs=Pin(21, Pin.OUT),
        reset=Pin(22, Pin.OUT),
        backlight=Pin(1, Pin.OUT),
        rotation=90)
    
    tft.fill(gc9a01.GREEN) # fill screen in green
    initialtime= time.ticks_ms() #https://docs.micropython.org/en/latest/library/time.html
    dac=mcp4725.MCP4725(i2c,mcp4725.BUS_ADDRESS[0])
    
    # from fonts import vga1_8x8 as font
    from fonts import vga2_8x8 as font1
    # from fonts import vga1_8x16 as font
    from fonts import vga2_8x16 as font2
    # from fonts import vga1_16x16 as font
    # from fonts import vga1_bold_16x16 as font
    # from fonts import vga2_16x16 as font
    from fonts import vga2_bold_16x16 as font3
    # from fonts import vga1_16x32 as font
    # from fonts import vga1_bold_16x32 as font
    # from fonts import vga2_16x32 as font
    from fonts import vga2_bold_16x32 as font
    
    # lines below are the ones to read user keyboard in Thonny IDE
    spoll=uselect.poll()
    spoll.register(sys.stdin,uselect.POLLIN)
    def read1():
        return(sys.stdin.read(4) if spoll.poll(0) else None)
    
    while True:
        try:
            currenttime= time.ticks_ms() #Every time it passes here, gets the current time
            if time.ticks_diff(time.ticks_ms(), initialtime) > 3000: # this IF will be true every 2000 ms
                initialtime= time.ticks_ms() #update with the "current" time
                
                c = read1() # verify whether user typed a number
                if c != None:
                    print(c)
                    d= float(c)
                    if d > 3.3:
                        d = 0
                    valuetowrite= int(d * 4095 / 3.3)
                    dac.write(valuetowrite)
                    #showonscreen= str(round((valuetowrite/4095 * 3.3), 3))
                    showonscreen= str(round(d, 3))
                    tft.text(font, showonscreen, 70, 120, gc9a01.WHITE, gc9a01.GREEN)
                    pass
            
                
                
                #dac.read()
                tft.text(font3, "MCP4725", 70, 40, gc9a01.BLACK, gc9a01.GREEN)
                tft.text(font3, "D/A", 70, 60, gc9a01.BLACK, gc9a01.GREEN)
                tft.text(font, "Value:", 70, 80, gc9a01.WHITE, gc9a01.GREEN)
                
                tft.text(font, " V", 140, 120, gc9a01.WHITE, gc9a01.GREEN)
                #print(user)
                
            
            
        except OSError as e:
            print('Failed reception')
            # If the Pi Pico 2 does not receive the measurements from the sensor 


main()