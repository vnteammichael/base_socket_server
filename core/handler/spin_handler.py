from core.handler.base_handler import BaseHandler
from core.service.actions import Action,ActionType
from core.entity.user import User
from core.service.user_management import user_manager
import json

class SpinHandler(BaseHandler):
    async def handle(self, action: Action):
        response = {}
        #handle init game 
        data = action.get_data()

        try:      
            response['cmd'] = ActionType.PLAY.value
            # token = data['token']

            # user_id = token
            # #check token valid
            bet = float(data['bet'])
            
            # data = {}
            # get user
            
            # if user_manager.is_have_user(user_id=user_id):
            #     user = user_manager.get_user_data(user_id=user_id)
            #     data = user.play_game(bet=bet)
            #     if data is not None:
            #         data['status'] = True
            #         data['total_reward'] = data['total_reward'] * (bet/3)
            #         user.call_api_update_result(bet=bet,total_rewards = data['total_reward'] )
            #         #call api plus reward
            #         data['valid_amount'] = user.amount
            #         data['msg'] = ""
            #     else:
            #         data['status'] = False
            #         data['msg'] = "Can not play game"

            # user = user_manager.get_user_data(user_id=user_id)
            user = User(user_id='1',game_code='a')
            data = user.play_game(bet=bet)
            if data is not None:
                data['status'] = True
                data['total_reward'] = data['total_reward'] * (bet/3)
                user.call_api_update_result(bet=bet,total_rewards = data['total_reward'] )
                #call api plus reward
                data['valid_amount'] = user.amount
                data['msg'] = ""
            else:
                data['status'] = False
                data['msg'] = "Can not play game"
            
            
            response['data'] = data
        except KeyError:      
            response['cmd'] = ActionType.MISS_PARAM.value
        except TypeError:      
            response['cmd'] = ActionType.TYPE_ERROR.value
        finally:
            
            return response