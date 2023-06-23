import asyncio
import time
import board
import keypad
import neopixel
from messaging import Messenger

messenger = Messenger()

pixel_pin = board.A0
num_pixels = 256

#pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False)


class Controls:
    def __init__(self):
        self.Swtch = False
        self.wait = 0.001
        self.msg = {
                    'pixel_pin':'',
                    'num_pixels':256,
                    'bright':0.5,
                    'WidthMulti':4,
                    'NeoPixelWidth':8,
                    'BlockRGB':(0,0,0),
                    'DarkBlockRGB':(100,100,100),
                    'timeset':0.01,
                    'cmd':"off",
                    "timelimit": 5
                    }
        self.resp = {
                    'time' : time.monotonic(),
                    'message_recieved:':'NULL',
                    'error':'None',
                    'message':{},
                    'pixel_box_index':[]
                    }

def white_box( wait, pixels, num_pixels, NeoPixelWidth, BlockWidth, BlockRGB, DarkBlockRGB, controls):
    for i in range(0, num_pixels - (BlockWidth - NeoPixelWidth), NeoPixelWidth):
        for j in range(i, i + BlockWidth):
            pixels[j] = BlockRGB
        for k in range(i - BlockWidth, i):
            pixels[k] = DarkBlockRGB
        controls.resp['pixel_box_index'].append([i,time.monotonic()])
        pixels.show()
        time.sleep(wait)
    # time.sleep(wait)

def pixels_off(pixels):
    pixels.fill((0,0,0))
    pixels.show()
    #time.sleep(wait)

def set_single_led_exc(wait,pixels,led_num_index,RGB):
    pixels.fill((0,0,0))
    pixels.show()
    pixels[led_num_index] = RGB
    pixels.show()
    time.sleep(wait)

def set_single_led_inc(wait, pixels, led_num_index, RGB):
    pixels[led_num_index] = RGB
    pixels.show()
    time.sleep(wait)

async def led_func(controls):
    pixel_pin = board.A0
    msg = controls.msg
        
    num_pixels = msg["num_pixels"]
    bright = msg["bright"]
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=bright, auto_write=False)
    pixels.fill((0, 0, 0))
    pixels.show()

    while True:       
        msg = controls.msg
        num_pixels = msg["num_pixels"]
        bright = msg["bright"]
        WidthMulti = msg["WidthMulti"]
        NeoPixelWidth = msg["NeoPixelWidth"]
        BlockWidth = WidthMulti * NeoPixelWidth
        BlockRGB = tuple(msg["BlockRGB"])
        DarkBlockRGB = tuple(msg["DarkBlockRGB"])
        timeset = msg["timeset"]
        cmd = msg["cmd"]
        led_num_index = msg["i"]
        RGB = tuple(msg["led_RGB"])
        pixels.brightness = bright 

        if controls.Swtch == True and cmd == "off":
            pixels_off(pixels)
            controls.wait = 0.001

        elif controls.Swtch == True and cmd == "white_box":
            white_box(
                timeset,
                pixels,
                num_pixels,
                NeoPixelWidth,
                BlockWidth,
                BlockRGB,
                DarkBlockRGB,
                controls,
                )
            controls.wait = 0.001

        elif controls.Swtch == True and cmd == "xset":
            set_single_led_exc(1,pixels, led_num_index, RGB)
            controls.wait = 0.001

        elif controls.Swtch == True and cmd == "iset":
            set_single_led_inc(1, pixels, led_num_index, RGB)
            controls.wait = 0.001

        elif controls.Swtch == True and cmd == "show":
            pixels.show()
            controls.wait = 0.001

        elif controls.Swtch == True and cmd == "Reset_Num_LEDs":
            pixels.deinit()
            pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=bright, auto_write=False)
            controls.wait = 0.001

        elif controls.Swtch == True and cmd == "num":
            controls.rsp
            controls.wait = 0.001
        
        elif controls.Swtch == False:
            pixels_off(pixels)
            controls.wait = 0.001

        await asyncio.sleep(controls.wait)

async def monitor_message(controls):
    while True:

        # Handle incoming messages 
        msg = messenger.update()

        if msg:
            # We got a new message.  
            
            # Send a response. It can by anything.  
            rsp = {
                    'time' : time.monotonic(),
                    'message' : msg, 
                    'message_count' : messenger.message_count,
                    }
            controls.resp['message'] = msg
            controls.resp['message_count'] = messenger.message_count
            controls.resp['error'] = 'None'
            controls.resp['message_recieved:'] = 'Yes'
            controls.Swtch = True
            controls.msg = msg
            messenger.send(controls.resp)
            controls.resp['pixel_box_index'] = []

        elif messenger.error:
            # We have a message error - we couldn't parse the json. 
            
            # Send error response. Again it can be anything you want  
            rsp = {
                    'time' : time.monotonic(),
                    'error': messenger.error_message,
                    }
            controls.wait = 0.01
            controls.Swtch = False
            controls.resp['message'] = {}
            controls.resp['message_recieved:'] = 'error'
            controls.resp['error'] = messenger.error_message
            messenger.send(controls.resp)
            controls.resp['pixel_box_index'] = []
        else:
            rsp = {
                    'time' : time.monotonic(),
                    'NoMessage': 'NO MESSAGE WAS RECIEVED',
                    }
            controls.wait = 0.01
            controls.Swtch = False
            controls.resp['message'] = {}
            controls.resp['message_recieved:'] = 'No'
            messenger.send(controls.resp)
            controls.resp['pixel_box_index'] = []
        await asyncio.sleep(0)


async def main():
    controls = Controls()

    message_task = asyncio.create_task(monitor_message(controls))
    animation_task2 = asyncio.create_task(led_func(controls))

    # This will run forever, because no tasks ever finish.
    await asyncio.gather(message_task, animation_task2)


asyncio.run(main())