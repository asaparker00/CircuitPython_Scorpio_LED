import sys
import json
import usb_cdc
import supervisor

class Messenger:

    def __init__(self):
        self.buffer = []
        self.err_str = '' 
        self.err_cnt = 0
        self.msg_cnt = 0

    @property
    def error(self):
        return bool(self.err_str)

    @property
    def error_message(self):
        return self.err_str

    @property
    def message_count(self):
        return self.msg_cnt

    def update(self):
        msg = False
        while supervisor.runtime.serial_bytes_available:
            byte = sys.stdin.read(1)
            if byte != '\n':
                self.buffer.append(byte)
            else:
                msg_str = ''.join(self.buffer)
                self.buffer = []
                msg = True
                break
        msg_dict = {}
        self.err_str = '' 
        if msg:
            try:
                msg_dict = json.loads(msg_str)
                self.msg_cnt += 1
            except ValueError as e:
                self.err_str = str(e)
                self.err_cnt += 1
        return msg_dict

    def send(self,msg):
        print(json.dumps(msg))

