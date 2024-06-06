from core.handler.base_handler import BaseHandler
from core.service.actions import Action,ActionType
from core.service.user_management import user_manager

class InitInfoHandler(BaseHandler):
    async def handle(self, action: Action):
        response = {}
        #handle init game 
        data = action.get_data()

        try:      
            response['cmd'] = ActionType.INIT_INFO.value
            token = data['token']
            #check token valid
            user_id = token
            data = {}
            #init user
            user = None
            if user_manager.is_have_user(user_id=user_id):
                user = user_manager.get_user_data(user_id=user_id)

            # if user_manager.is_have_user(user_id=user_id):
            #     user = user_manager.get
                data['status'] = True
                data['valid_amount'] = user.amount
                data['token'] = token
                data['msg'] = ""
            else:
                data['status'] = False
                data['msg'] = "Do not have user"

            response['data'] = data
        except KeyError:      
            response['cmd'] = ActionType.MISS_PARAM.value
        except TypeError:      
            response['cmd'] = ActionType.TYPE_ERROR.value
        finally:
            
            return response