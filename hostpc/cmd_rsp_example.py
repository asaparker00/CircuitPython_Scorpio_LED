import json
import serial

class DeviceComm(serial.Serial):
    """
    Implements basic device communications
    """

    def __init__(self, port):
        port_param = {'port': port, 'baudrate': 115200, 'timeout': 0.2}
        super().__init__(**port_param)
        self.num_throw_away = 10
        self.throw_away_lines()

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
    BlockRGB = (100,100,100)
    BlockRGB = (100,0,100)
    DarkBlockRGB = (0,0,0)
    func = "white_box"
    timeset = 0.01
    timelimit = 5

    count = 0

    while True:
        #count += 1
        #value = random.random()
        #date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        #msg = {'count': count, 'value': value, 'date': date}
        msg = {'pixel_pin':pixel_pin,'num_pixels':num_pixels, 'bright':bright, 'WidthMulti':WidthMulti, 'NeoPixelWidth':NeoPixelWidth, 'BlockRGB':BlockRGB,'DarkBlockRGB':DarkBlockRGB,'timeset':timeset,'func':func,"timelimit": timelimit}
        rsp = dev.send_and_receive(msg)
        print(f'msg: {msg}')
        print(f'rsp: {rsp}')
        #print(f'rsp: {rsp["timeset"]}')
        print()
        time.sleep(0.2)
        count = 1



