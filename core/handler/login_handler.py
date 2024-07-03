from core.handler.base_handler import BaseHandler
from core.service.actions import Action,ActionType
from core.entity.user import User
from core.service.user_management import user_manager
import json

class LoginHandler(BaseHandler):
    def __init__(self, game_server):
        self.game_server = game_server

    async def handle(self, action: Action):
        response = {}
        #handle init game 
        data = action.get_data()
        client_handler = action.client_handler

    # try:      
        response['cmd'] = ActionType.LOGIN.value
        token = data['token']
        #check token valid
        user_name = token
        data = {}

        # Handle the case where the token is already in use
        if user_name in self.game_server.token_to_client:
            old_client_handler = self.game_server.token_to_client[user_name]
            if not old_client_handler.is_closed():
                await old_client_handler.update(json.dumps({"cmd": ActionType.DISCONNECT.value, "data":{"msg": "You have been disconnected due to a new login."}}))
                await old_client_handler.close()
        # Register the new client handler
        self.game_server.token_to_client[user_name] = client_handler

        #init user
        user_id = user_manager.is_have_user(user_name=user_name)
        if user_id == None:
            user_id = user_manager.create_new_user(user_name=user_name)

        user_data = user_manager.get_user_data(user_id=user_id)


        data['status'] = True
        data['valid_amount'] = user_data['balance']
        data['token'] = user_data['username']
        data['msg'] = "" 
        response['data'] = data
    # except KeyError as e:      
    #     response['cmd'] = ActionType.MISS_PARAM.value
    #     data['msg'] = e 
    # except TypeError as e:      
    #     response['cmd'] = ActionType.TYPE_ERROR.value
    #     data['msg'] = e 
    # finally:
        
        return response