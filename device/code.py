import time
from messaging import Messenger

messenger = Messenger()

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
        messenger.send(rsp)

    elif messenger.error:
        # We have a message error - we couldn't parse the json. 
        
        # Send error response. Again it can be anything you want  
        rsp = {
                'time' : time.monotonic(),
                'error': messenger.error_message,
                }
        messenger.send(rsp)

    
    # Do other stuff here. 
    # --------------------------------------------------------------------
    # No long running tasks or you will miss messages. 
    # Restructure code, including messaging, to use async if necessary. 
    # ---------------------------------------------------------------------
    






        







