from enum import Enum

# Define action types as an enumeration for clarity and to avoid hard-coded strings
class ActionType(Enum):
    LOGIN = 1000
    RECONNECT = 1001
    INIT_INFO = 1002
    DISCONNECT = 1003

    PLAY = 2000
    UPDATE = 2001



    #get data
    DATA_GAME = 3000
    # Error

    MISS_PARAM = 8000
    TYPE_ERROR = 8001
    ERROR = 8002

# Basic action structure
class Action:
    def __init__(self, data, client_handler=None):
        self.data = data
        self.client_handler = client_handler

    def get_data(self):
        return self.data['data']
    
    def get_type(self):
        return self.data['cmd']
    
    def get_type(self):
        for action_type in ActionType:
            if action_type.value == self.data['cmd']:
                return action_type
        return None
    
    def send(self,msg):
        self.client_handler.update(msg)
        

