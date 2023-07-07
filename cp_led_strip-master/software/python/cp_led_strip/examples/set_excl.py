from __future__ import print_function
import time
from basic_led_strip import BasicLedStrip

led_strip = BasicLedStrip('/dev/ttyUSB0')
num_led = led_strip.number_of_leds()
led_strip.off()

color_list = [
        (0,  100,  50),
        (100, 50,   0), 
        (50, 100,   0),
        (100, 0,   50),
        (0,   50, 100),
        (50,   0, 100),
        ]


for rgb in color_list:
    for led in range(num_led):
        t0 = time.time()
        led_strip.set(led,rgb,mode='exclusive')
        print(led, rgb)

    for led in reversed(range(num_led)):
        t0 = time.time()
        led_strip.set(led,rgb,mode='exclusive')
        print(led, rgb)


print()
led_strip.off()
