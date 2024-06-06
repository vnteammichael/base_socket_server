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
        game_code = data['game_code']
        #check token valid
        user_id = token
        data = {}

        # Handle the case where the token is already in use
        if user_id in self.game_server.token_to_client:
            old_client_handler = self.game_server.token_to_client[user_id]
            if not old_client_handler.is_closed():
                await old_client_handler.update(json.dumps({"cmd": ActionType.DISCONNECT.value, "data":{"msg": "You have been disconnected due to a new login."}}))
                await old_client_handler.close()
        # Register the new client handler
        self.game_server.token_to_client[user_id] = client_handler

        #init user
        user = None
        if not user_manager.is_have_user(user_id=user_id):
            user = User(user_id=user_id,game_code=game_code)
            user_manager.add_user(user_id=user_id,user_data=user)
        else:
            user = user_manager.get_user_data(user_id=user_id)

        # if user_manager.is_have_user(user_id=user_id):
        #     user = user_manager.get
        data['status'] = True
        data['valid_amount'] = user.amount
        data['token'] = token
        data['msg'] = "" 
        response['data'] = data
        # except KeyError:      
        #     response['cmd'] = ActionType.MISS_PARAM.value
        # except TypeError:      
        #     response['cmd'] = ActionType.TYPE_ERROR.value
        # finally:
            
        return response