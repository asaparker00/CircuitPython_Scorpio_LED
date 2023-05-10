import sys
import json
import usb_cdc
import supervisor

class Messenger:

    def __init__(self):
        self.buffer = []
        self.error_str = '' 
        self.error_cnt = 0
        self.message_count = 0

    @property
    def error(self):
        return bool(self.error_str)

    @property
    def error_message(self):
        return self.error_str

    def update(self):
        msg = False
        while supervisor.runtime.serial_bytes_available:
            byte = sys.stdin.read(1)
            if byte != '\n':
                self.buffer.append(byte)
            else:
                message_str = ''.join(self.buffer)
                self.buffer = []
                msg = True
                break
        msg_dict = {}
        self.error_str = '' 
        if msg:
            try:
                msg_dict = json.loads(message_str)
                self.message_count += 1
            except ValueError as e:
                self.error_str = str(e)
                self.error_cnt += 1
        return msg_dict

    def send(self,msg):
        print(json.dumps(msg))

