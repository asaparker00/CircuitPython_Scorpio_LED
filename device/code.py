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
        self.wait = 0.0
        self.msg = {'pixel_pin':'','num_pixels':256, 'bright':0.5, 'WidthMulti':4, 'NeoPixelWidth':8, 'BlockRGB':(0,0,0),'DarkBlockRGB':(100,100,100),'timeset':0.01,'func':"white_box","timelimit": 5}

def white_box( wait, pixels, num_pixels, NeoPixelWidth, BlockWidth, BlockRGB, DarkBlockRGB):
    for i in range(0, num_pixels - (BlockWidth - NeoPixelWidth), NeoPixelWidth):
        for j in range(i, i + BlockWidth):
            pixels[j] = BlockRGB
        for k in range(i - BlockWidth, i):
            pixels[k] = DarkBlockRGB
        pixels.show()
        time.sleep(wait)
    # time.sleep(wait)

async def led_func(controls):
    
    num_pixels = 256
    pixel_pin = board.A0
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False)
    msg = controls.msg
    bright = msg["bright"]
    
    pixels.brightness = bright
    while True:
        msg = controls.msg
        bright = msg["bright"]
        
        pixels.brightness = bright

        pixels.fill((0, 0, 0))
        pixels.show()
        WidthMulti = msg["WidthMulti"]
        NeoPixelWidth = msg["NeoPixelWidth"]
        BlockWidth = WidthMulti * NeoPixelWidth
        BlockRGB = tuple(msg["BlockRGB"])
        DarkBlockRGB = tuple(msg["DarkBlockRGB"])
        timeset = msg["timeset"]
        func = msg["func"]
        if controls.Swtch == True:
            white_box(
                timeset,
                pixels,
                num_pixels,
                NeoPixelWidth,
                BlockWidth,
                BlockRGB,
                DarkBlockRGB,
                )
        await asyncio.sleep(controls.wait)
        # while controls.Swtch == False:
        #     BlockRGB = (100,0,0)
        #     DarkBlockRGB = (0,0,0)
        #     white_box(
        #         timeset,
        #         pixels,
        #         num_pixels,
        #         NeoPixelWidth,
        #         BlockWidth,
        #         BlockRGB,
        #         DarkBlockRGB,
        #         )
        #     await asyncio.sleep(controls.wait)

async def monitor_buttons(controls):
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
            controls.Swtch = not controls.Swtch
            controls.msg = msg
            messenger.send(rsp)

        elif messenger.error:
            # We have a message error - we couldn't parse the json. 
            
            # Send error response. Again it can be anything you want  
            rsp = {
                    'time' : time.monotonic(),
                    'error': messenger.error_message,
                    }
            controls.wait = controls.wait + 0.001
            messenger.send(rsp)
        await asyncio.sleep(0)


async def main():
    controls = Controls()

    buttons_task = asyncio.create_task(
        monitor_buttons(controls)
    )
    #animation_task = asyncio.create_task(rainbow_cycle(controls))
    animation_task2 = asyncio.create_task(led_func(controls))

    # This will run forever, because no tasks ever finish.
    await asyncio.gather(buttons_task, animation_task2)


asyncio.run(main())