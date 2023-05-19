import time
from messaging import Messenger
import board
import neopixel
import asyncio


messenger = Messenger()

class IO:
    def __init__(self):
        self.Swtch = False
        self.wait = 0.0
        self.delay = 0.5
        self.mesg = {'pixel_pin':"A0",'num_pixels':256, 'bright':0.5, 'WidthMulti':4, 'NeoPixelWidth':8, 'BlockRGB':(100,100,100),'DarkBlockRGB':(0,0,0),'timeset':0.01,'func':"white_box"}

def white_box(
    wait, pixels, num_pixels, NeoPixelWidth, BlockWidth, BlockRGB, DarkBlockRGB
):
    for i in range(0, num_pixels - (BlockWidth - NeoPixelWidth), NeoPixelWidth):
        for j in range(i, i + BlockWidth):
            pixels[j] = (100, 100, 100)
        for k in range(i - BlockWidth, i):
            pixels[k] = (0, 0, 0)
        pixels.show()
        time.sleep(wait)
    # time.sleep(wait)


async def msgcode(IO):
    while True:
        # Handle incoming messages
        msg = messenger.update()
        if msg:
            # We got a new message.

            # Send a response. It can by anything.
            rsp = {
                "time": time.monotonic(),
                "message": msg,
                "message_count": messenger.message_count,
            }
            IO.mesg = msg
            IO.Swtch = True
            IO.delay = 0.1
            messenger.send(rsp)

        elif messenger.error:
            # We have a message error - we couldn't parse the json.

            # Send error response. Again it can be anything you want
            rsp = {
                "time": time.monotonic(),
                "error": messenger.error_message,
            }
            IO.Swtch = False
            IO.delay = 0.5
            messenger.send(rsp)

        await asyncio.sleep(0)

async def ledcode(IO):
    msg = IO.mesg
    while True:
        pixel_pin = board.A0  # msg['pixel_pin']
        num_pixels = msg["num_pixels"]
        bright = msg["bright"]

        ORDER = neopixel.GRB
        pixels = neopixel.NeoPixel(
            pixel_pin,
            num_pixels,
            brightness=bright,
            auto_write=False,
            pixel_order=ORDER,
        )
        pixels.fill((0, 0, 0))
        pixels.show()
        WidthMulti = msg["WidthMulti"]
        NeoPixelWidth = msg["NeoPixelWidth"]
        BlockWidth = WidthMulti * NeoPixelWidth
        BlockRGB = msg["BlockRGB"]
        DarkBlockRGB = msg["DarkBlockRGB"]
        timeset = msg["timeset"]
        func = msg["func"]

        while IO.Swtch:
            white_box(
                timeset,
                pixels,
                num_pixels,
                NeoPixelWidth,
                BlockWidth,
                BlockRGB,
                DarkBlockRGB,
                )
                #await asyncio.sleep(0.5)
            await asyncio.sleep(IO.delay)

        while IO.Swtch == False:
            pixels.fill((5, 5, 5))
            pixels.show()
            await asyncio.sleep(IO.delay)
        await asyncio.sleep(wait)
        await asyncio.sleep(wait)

async def main():

    InputOutput = IO()
    msg_task = asyncio.create_task(
        msgcode(InputOutput)
    )
    led_task = asyncio.create_task(
        ledcode(InputOutput)
    )

    await asyncio.gather(msg_task, led_task)
        # Do other stuff here.
        # --------------------------------------------------------------------
        # No long running tasks or you will miss messages.
        # Restructure code, including messaging, to use async if necessary.
        # ---------------------------------------------------------------------

asyncio.run(main())
