import json
import serial

class DeviceComm(serial.Serial):
    """
    Implements basic device communications
    """


    def __init__(self, port):

        pixel_pin = 'board.A0'
        num_pixels = 256
        bright = 0.9
        WidthMulti = 4
        NeoPixelWidth = 8
        #BlockRGB = (100,100,100)
        BlockRGB = (100,0,100)
        DarkBlockRGB = (0,0,0)
        cmd = None
        i = 0
        timeset = 0.01
        timelimit = 5
        BlockWidth = WidthMulti * NeoPixelWidth


        port_param = {'port': port, 'baudrate': 115200, 'timeout': 0.2}
        super().__init__(**port_param)
        self.num_throw_away = 10
        self.throw_away_lines()
        self.cmd_dict = {'pixel_pin':pixel_pin,'num_pixels':num_pixels, 'bright':bright, 'WidthMulti':WidthMulti, 'NeoPixelWidth':NeoPixelWidth, 'BlockRGB':BlockRGB,'DarkBlockRGB':DarkBlockRGB,'timeset':timeset,"timelimit": timelimit,"i": i, "led_RGB":BlockRGB,'cmd':None, 'num_of_leds':num_pixels}

    def command_dict(self):
        return self.cmd_dict

    def throw_away_lines(self):
        """
        Throw away first few lines. Deals with case where user has updated the
        firmware which writes a bunch text to the serial port.
        """
        for i in range(self.num_throw_away):
            line = self.readline()

    def send_and_receive(self, msg_dict):
        """
        Send and receive message from the device.
        """
        msg_json = json.dumps(msg_dict) + '\n'
        self.write(msg_json.encode())
        rsp_json = self.readline()
        rsp_json = rsp_json.strip()
        rsp_dict = {}
        try:
            rsp_dict = json.loads(rsp_json.decode('utf-8'))
        except json.decoder.JSONDecodeError as e:
            print(f'Error decoding json message: {e}')
        return rsp_dict

    def set(self, led_number, rgb_value, mode='inclusive'):
        """Set the value of led and location=led_number to the specified rgb_value  
        where 

        led_number  = position of led in the array
        rgb_value   = tuple of red, green, blue values 0-255 
            
        """
        led_RGB = rgb_value
        if mode == 'exclusive' or mode == 'excl':
            self.cmd_dict['cmd'] ='xset'
            self.cmd_dict['i'] = led_number
            self.cmd_dict['led_RGB'] = led_RGB
        elif mode == 'inclusive' or mode == 'incl':
            self.cmd_dict['cmd'] ='iset'
            self.cmd_dict['i'] = led_number
            self.cmd_dict['led_RGB'] = led_RGB
        else:
            raise ValueError("mode must be 'inclusive' or 'exclusive'")
        return self.send_and_receive(self.cmd_dict)

    def set_all(self, rgb_value):
        """Sets all leds to the same r,g,b values given by rgb_value

        """
        led_RGB = rgb_value
        self.cmd_dict['cmd'] ='aset'
        self.cmd_dict['led_RGB'] = led_RGB
        return self.send_and_receive(self.cmd_dict)

    def off(self):
        """Turns all leds off

        """
        self.cmd_dict['cmd'] ='off'
        return self.send_and_receive(self.cmd_dict)


    def Reset_Num_LEDs(self):
        """Resets NeoPixel with different LED amount

        """
        self.cmd_dict["cmd"] = "Reset_Num_LEDs"
        return self.send_and_receive(self.cmd_dict)

    def number_of_leds(self):
        """Gets the number of leds controllable by the firmware. 

        """
        self.cmd_dict['cmd'] ='num'
        rsp = self.send_and_receive(self.cmd_dict)
        return rsp['num_of_leds']
# --------------------------------------------------------------------------------------

if __name__ == '__main__':

    import time
    import random
    from datetime import datetime



    

    port = '/dev/ttyACM0' # Set to match your device
    dev = DeviceComm(port)
    
    pixel_pin = 'board.A0'
    num_pixels = 256
    bright = 0.9
    WidthMulti = 4
    NeoPixelWidth = 8
    #BlockRGB = (100,100,100)
    BlockRGB = (100,0,100)
    BlockRGB = (0,100,100)
    DarkBlockRGB = (0,0,0)
    cmd = "iset"
    #cmd = "white_box"
    i = 8
    
    timeset = 0.01
    timelimit = 5
    BlockWidth = WidthMulti * NeoPixelWidth

    while True:
        msg = {'pixel_pin':pixel_pin,'num_pixels':num_pixels, 'bright':bright, 'WidthMulti':WidthMulti, 'NeoPixelWidth':NeoPixelWidth, 'BlockRGB':BlockRGB,'DarkBlockRGB':DarkBlockRGB,'timeset':timeset,"timelimit": timelimit,"i": i, "led_RGB":BlockRGB,'cmd':cmd}
        #rsp = dev.send_and_receive(msg)
        #rsp = dev.set(i,(0,100,100))
        rsp = dev.send_and_receive(msg)
        print(f'msg: {dev.command_dict()}')
        print(f'rsp: {rsp}')
        print()
        time.sleep(0.2)



