from __future__ import print_function
from basic_led_strip import BasicLedStrip

led_strip = BasicLedStrip('/dev/ttyUSB0')
num_led = led_strip.number_of_leds()
led_strip.off()

for led in range(num_led):
    rgb = 0,50,50
    led_strip.set(led,rgb,mode='exclusive')

led_strip.off()
