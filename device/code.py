import asyncio
import time
import board
import keypad
import neopixel
from messaging import Messenger

messenger = Messenger()

class Controls:
    # ... rest of your Controls class here ...
    def __init__(self):
        self.Swtch = False
        self.wait = 0.001
        self.msg = {
                    'pixel_pin':None,
                    'num_pixels':256,
                    'bright':0.5,
                    'led_RGB':(0,0,0),
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

def Box( wait, pixels, num_pixels, NeoPixelWidth, BlockWidth, BlockRGB, BackGroundRGB, controls):
    pixels.fill(BackGroundRGB)
    pixels.show()
    for i in range(0, num_pixels, NeoPixelWidth):
        # Turn on the LEDs in the current group
        for j in range(i, min(i + NeoPixelWidth, num_pixels)):
            pixels[j] = BlockRGB  # Set LED color
        pixels.show()
        #time.sleep(0.1)  # Delay between lighting up each group

        # Turn off the LEDs in the group that is 'BlockWidth' LEDs before the current group
        if i >= BlockWidth:
            for j in range(i - BlockWidth, i - BlockWidth + NeoPixelWidth):
                pixels[j] = BackGroundRGB  # Turn off LEDs
            pixels.show()
            #time.sleep(0.1)  # Delay between turning off each group

        time.sleep(wait)  # Add a delay between iterations

    # Additional loop to turn off the remaining LEDs
    for i in range(num_pixels - BlockWidth, num_pixels, NeoPixelWidth):
        for j in range(i, min(i + NeoPixelWidth, num_pixels)):
            pixels[j] = BackGroundRGB  # Turn off LEDs
        pixels.show()
        time.sleep(wait)  # Delay between turning off each group




def pixels_off(pixels):
    pixels.fill((0,0,0))
    pixels.show()
    #time.sleep(wait)

def set_single_led_exc(wait,pixels,led_num_index,RGB):
    pixels.fill((0,0,0))
    pixels.show()
    pixels[led_num_index] = RGB
    #pixels.show()
    time.sleep(wait)

def set_single_led_inc(wait, pixels, led_num_index, RGB):
    pixels[led_num_index] = RGB

def set_multiple_led_inc(wait,pixels,led_num_index,RGB):
    for index in led_num_index:
        pixels[index] = RGB

async def led_func(controls):
    T = True
    pixel_pin = board.A0
    num_pixels = controls.msg['num_pixels']
    timezone = 0.001

    # Handling hardware exceptions at creation time
    try:
        pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False)
    except Exception as e:
        T = False
    while T == True:       
        try:
            msg = controls.msg
            num_pixels = msg.get("num_pixels", 256)
            bright = msg.get("bright", 0.5)
            timeset = msg.get("timeset", 0.01)
            timelimit = msg.get("timelimit", 5)
            cmd = msg.get("cmd", "off")
            led_num_index = msg.get("i", list(range(0,8)))
            RGB = tuple(msg.get("led_RGB", (0,0,0)))
            box_dict = msg.get("box_dict", {"num_pixels": 256, "NeoPixelWidth":8, "BlockWidth":4, "BlockRGB":(100,100,100), "BackGroundRGB":(0,0,0)})
            #pixels.brightness = bright 
        except Exception as e:
            print("An error occurred while processing the message:", str(e))
            continue  # Skip to next iteration if there's an error here

        # ... rest of your loop here ...
        if controls.Swtch == True and cmd == "off":
            pixels_off(pixels)
            controls.wait = timezone

        elif controls.Swtch == True and cmd == "white_box":
            Box(
                timeset,
                pixels,
                box_dict['num_pixels'],
                box_dict['NeoPixelWidth'],
                box_dict['BlockWidth'],
                box_dict['BlockRGB'],
                box_dict['BackGroundRGB'],
                controls,
                )
            controls.wait = timezone

        elif controls.Swtch == True and cmd == "xset":
            set_single_led_exc(1,pixels, led_num_index, RGB)
            controls.wait = timezone

        elif controls.Swtch == True and cmd == "iset":
            set_multiple_led_inc(1, pixels, led_num_index, RGB)
            controls.wait = timezone

        elif controls.Swtch == True and cmd == "show":
            pixels.show()
            #time.sleep(1)
            controls.wait = timezone

        elif controls.Swtch == True and cmd == "Reset_Num_LEDs":
            pixels.deinit()
            pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=bright, auto_write=False)
            controls.wait = timezone

        elif controls.Swtch == True and cmd == "num":
            controls.rsp
            controls.wait = timezone
        
        elif controls.Swtch == False:
            pixels_off(pixels)
            controls.wait = timezone
        


        await asyncio.sleep(controls.wait)

async def monitor_message(controls):
    timezone2 = 0.0001
    while True:
        try:
            msg = messenger.update()
        except Exception as e:
            print("An error occurred while receiving a message:", str(e))
            continue  # Skip to next iteration if there's an error here

        # ... rest of your loop here ...
        # Handle incoming messages 
        controls.resp['time'] = time.monotonic()

        if msg:
            # We got a new message.  
            
            # Send a response. It can by anything.  
            rsp = {
                    'time' : controls.resp['time'],
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
                    'time' : controls.resp['time'],
                    'error': messenger.error_message,
                    }
            controls.wait = timezone2
            controls.Swtch = False
            controls.resp['message'] = {}
            controls.resp['message_recieved:'] = 'error'
            controls.resp['error'] = messenger.error_message
            messenger.send(controls.resp)
            controls.resp['pixel_box_index'] = []
        else:
            rsp = {
                    'time' : controls.resp['time'],
                    'NoMessage': 'NO MESSAGE WAS RECIEVED',
                    }
            controls.wait = timezone2
            controls.Swtch = False
            controls.resp['message'] = {}
            controls.resp['message_recieved:'] = 'No'
            controls.resp['error'] = "None"
            messenger.send(controls.resp)
            controls.resp['pixel_box_index'] = []
        await asyncio.sleep(0)

async def main():
    controls = Controls()

    message_task = asyncio.create_task(monitor_message(controls))
    animation_task2 = asyncio.create_task(led_func(controls))

    # This will run forever, because no tasks ever finish.
    await asyncio.gather(message_task, animation_task2)

try:
    asyncio.run(main())
except Exception as e:
    print("An error occurred while running the program:", str(e))
