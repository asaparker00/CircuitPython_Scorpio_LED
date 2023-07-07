basic_led_strip
--------
Python basic library for controlling a strip of neopixel leds via an arduino.
This library is a stripped down version for controlling the neopixels leds from
a lower power microcontroller such as a Arduino Uno or Nano. 

Example
--------

```python
from __future__ import print_function
from basic_led_strip import BasicLedStrip

led_strip = BasicLedStrip('/dev/ttyUSB0')
num_led = led_strip.number_of_leds()
led_strip.off()

for led in range(num_led):
    rgb = 0,50,50
    led_strip.set(led,rgb,mode='exclusive')

led_strip.off()

```


Installation
------------

```bash

$ python setup.py install 

or 

$ python setup.py develop


```


Links
-----

* Download https://github.com/willdickson/basic_led_strip


