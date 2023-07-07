from __future__ import print_function
import time
import random
from basic_led_strip import BasicLedStrip


led_strip = BasicLedStrip('/dev/ttyUSB0')
num_led = led_strip.number_of_leds() 
led_strip.off()

# Test set all 
for c in ('r', 'g', 'b'):
    for i in range(0,100):
        if c == 'r':
            rgb = i, 0, 0
        elif c == 'g':
            rgb = 0, i, 0
        else:
            rgb = 0, 0, i
        led_strip.set_all(rgb)
        print(c, i, rgb)

print()
led_strip.off()

for i in range(10): 
    r,g,b = 0,0,0
    if i%3 == 0:
        r = random.randint(0,100)
        g = random.randint(0,100)
    elif i%3 == 1:
        r = random.randint(0,100)
        b = random.randint(0,100)
    else:
        g = random.randint(0,100)
        b = random.randint(0,100)
    rgb = (r,g,b)
    led_strip.set_all(rgb)
    time.sleep(1.0)
    led_strip.set_all(rgb)
    print(c, i, rgb)

print()
led_strip.off()

# Test exclusive and inclusive set
for mode in ('inclusive', 'exclusive'):
    for led in range(num_led):
        t0 = time.time()
        r = random.randint(0,100)
        g = random.randint(0,100)
        b = random.randint(0,100)
        rgb= (r,g,b)
        led_strip.set(led,rgb,mode=mode)
        t1 = time.time()
        dt = t1-t0
        print(mode, led, rgb, 1/dt)
    print()
    led_strip.off()









