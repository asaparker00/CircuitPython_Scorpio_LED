import json
import serial

class DeviceComm(serial.Serial):
    """
    Implements basic device communications
    """

    def __init__(self, port, baudrate=115200, timeout=0.2, num_throw_away=10):
        self.num_pixels = 256
        self.bright = 0.9
        self.timeset = 0.01
        self.timelimit = 1
        self.i = 0
        self.BlockRGB = (100,0,100)
        self.cmd_dict = {'num_pixels':self.num_pixels, 'bright':self.bright, 
                         'timeset':self.timeset, "timelimit": self.timelimit,
                         "i": self.i, "led_RGB":self.BlockRGB, "box_dict":{"num_pixels": 256, 
                         "NeoPixelWidth":8, "BlockWidth":4, "BlockRGB":(100,100,100), 
                         "BackGroundRGB":(0,0,0)},'cmd':None}

        super().__init__(port=port, baudrate=baudrate, timeout=timeout)
        self.num_throw_away = num_throw_away
        self.throw_away_lines()

    def command_dict(self):
        return self.cmd_dict

    def throw_away_lines(self):
        """
        Throw away first few lines. Deals with case where user has updated the
        firmware which writes a bunch text to the serial port.
        """
        for _ in range(self.num_throw_away):
            self.readline()

    def send_and_receive(self, msg_dict):
        """
        Send and receive message from the device.
        """
        msg_json = json.dumps(msg_dict) + '\n'
        self.write(msg_json.encode())
        rsp_json = self.readline().strip()

        try:
            rsp_dict = json.loads(rsp_json.decode('utf-8'))
        except json.decoder.JSONDecodeError as e:
            print(f'Error decoding json message: {e}')
            rsp_dict = {}
        except serial.SerialException as e:
            print(f'Error in serial communication: {e}')
            rsp_dict = {}
        
        return rsp_dict

    #... rest of your methods here...

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

    def Host_Box(self, num_pixels,NeoPixelWidth,BlockWidth,BlockRGB,BackGroundRGB):
        for i in range(0, num_pixels, NeoPixelWidth):
                # Turn on the LEDs in the current group
                msg = {'num_pixels': num_pixels, "i": list(range(i, min(i + NeoPixelWidth, num_pixels))), "led_RGB":BlockRGB, 'cmd':"iset"}
                rsp = dev.send_and_receive(msg)
                print(f'rspbox: {rsp}')
                print()
                msg = {'num_pixels': num_pixels, "i": i, "led_RGB":BlockRGB, 'cmd':"show"}
                rsp = dev.send_and_receive(msg)
                print(f'rspshow: {rsp}')
                print()
                #time.sleep(0.1)  # Delay between lighting up each group

                # Turn off the LEDs in the group that is 'BlockWidth' LEDs before the current group
                if i >= BlockWidth:
                    msg = {'num_pixels': num_pixels, "i": list(range(i - BlockWidth, i - BlockWidth + NeoPixelWidth)), "led_RGB":BackGroundRGB, 'cmd':"iset"}
                    rsp = dev.send_and_receive(msg)
                    print(f'rspdelete: {rsp}')
                    print()
                    msg = {'num_pixels': dev.num_pixels, "i": i, "led_RGB":BlockRGB, 'cmd':"show"}
                    rsp = dev.send_and_receive(msg)
                    print(f'rspshow: {rsp}')
                    print()
                    #time.sleep(0.1)  # Delay between turning off each group
            # Additional loop to turn off the remaining LEDs
        for i in range(num_pixels - BlockWidth, num_pixels, NeoPixelWidth):
            msg = {'num_pixels': num_pixels, "i": list(range(i, min(i + NeoPixelWidth, num_pixels))), "led_RGB":BackGroundRGB, 'cmd':"iset"}
            rsp = dev.send_and_receive(msg)
            print(f'rspdeletelast: {rsp}')
            print()
            msg = {'num_pixels': dev.num_pixels, "i": i, "led_RGB":BlockRGB, 'cmd':"show"}
            rsp = dev.send_and_receive(msg)
            print(f'rspshow: {rsp}')
            print()
            #time.sleep(timelimit)  # Delay between turning off each group
        time.sleep(timelimit)

    def Firm_Box(self,num_pixels,NeoPixelWidth,BlockWidth,BlockRGB,BackGroundRGB):
        bd = {"num_pixels": num_pixels, "NeoPixelWidth":NeoPixelWidth, "BlockWidth":BlockWidth, "BlockRGB":BlockRGB, "BackGroundRGB":BackGroundRGB}
        msg = {'num_pixels': num_pixels, "i": 0, "box_dict":bd,"led_RGB":BlockRGB, 'cmd':"Box"}
        rsp = dev.send_and_receive(msg)
        print(f'rspbox: {rsp}')
        print()

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
        return rsp.get('num_of_leds', None)  # return None if 'num_of_leds' key doesn't exist
    
    def brightness(self,bright):
        msg = {'num_pixels': num_pixels, "bright": bright,"i": 0, "led_RGB":BlockRGB, 'cmd':"bright"}
        rsp = dev.send_and_receive(msg)
        print(f'rspbright: {rsp}')
        print()

# --------------------------------------------------------------------------------------

'''
if __name__ == '__main__':

    import time

    port = '/dev/ttyACM0' # Set to match your device
    dev = DeviceComm(port)
    i = 9
    #BlockRGB = (100,0,100)

    num_pixels = 256
    bright = 0.1
    WidthMulti = 4
    NeoPixelWidth = 8
    BlockRGB = (100,0,100)
    BlockRGB = (0,0,0)
    BackGroundRGB = (100,100,100)
    cmd = "off"
    p = 0
    
    #bd = {"num_pixels": num_pixels, "NeoPixelWidth":NeoPixelWidth, "BlockWidth":BlockWidth, "BlockRGB":BlockRGB, "BackGroundRGB":BackGroundRGB}

    timeset = 0.0001
    timelimit = 0.0001
    BlockWidth = WidthMulti * NeoPixelWidth

    #msg = {'pixel_pin':pixel_pin,'num_pixels':num_pixels, 'bright':bright, 'WidthMulti':WidthMulti, 'NeoPixelWidth':NeoPixelWidth, 'BlockRGB':BlockRGB,'DarkBlockRGB':DarkBlockRGB,'timeset':timeset,"timelimit": timelimit,"i": i, "led_RGB":BlockRGB,'cmd':cmd}

    while True:
        try:
            #dev.Host_Box(num_pixels,NeoPixelWidth,BlockRGB,BackGroundRGB)
            dev.brightness(bright)
            dev.Firm_Box(num_pixels,NeoPixelWidth,BlockWidth,BlockRGB,BackGroundRGB)

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    dev.close()  # ensure to close the device communication
'''