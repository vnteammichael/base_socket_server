from core.handler.base_handler import BaseHandler
from core.service.actions import Action,ActionType
from core.entity.user import User
from core.service.user_management import user_manager
from core.base.pool_objects import game_pool

class SpinHandler(BaseHandler):
    async def handle(self, action: Action):
        response = {}
        #handle init game 
        data = action.get_data()

        try:      
            response['cmd'] = ActionType.PLAY.value
            token = data['token']

            user_name = token
            #check token valid
            user_id = user_manager.is_have_user(user_name=user_name)
            if user_id != None:
                bet = float(data['bet'])
                game_code = data['game_code']
            
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
                user = user_manager.get_user_data(user_id=user_id)
                if user_manager.check_bet_available(user_id=user_id,bet=bet):
                    data = None
                    game = await game_pool.acquire(game_code)
                    try:
                        data = await game.play(1)
                    finally:
                        await game_pool.release(game)
                    if data is not None:
                        user_manager.update_user_balance(user_id=user_id,amount= - bet)
                        data['status'] = True
                        data['total_reward'] = data['total_reward'] * (bet/30)
                        data['bonus_reward'] = data['bonus_reward'] * (bet/30)
                        for k,v in data['line_win'].items():
                            if k != "scatter" :
                                v['reward'] = v['reward'] * (bet/30)
                        for i in data['bonus']:
                            i['reward'] = i['reward'] * (bet/30)
                            for k,v in i['line_win'].items():
                                if k != "scatter" :
                                    v['reward'] = v['reward'] * (bet/30)
                        #call api plus reward
                        data['valid_amount'] = user_manager.update_user_balance(user_id=user_id,amount= data['total_reward'] + data['bonus_reward'])
                        user_manager.insert_user_history(user_id=user_id,game_id=1,bet=bet,data=data)
                        data['msg'] = ""
                    else:
                        data['status'] = False
                        data['msg'] = "Can not play game"
                else:
                    data['status'] = False
                    data['msg'] = "Not engough bet"
                response['data'] = data
        except KeyError:      
            response['cmd'] = ActionType.MISS_PARAM.value
        except TypeError:      
            response['cmd'] = ActionType.TYPE_ERROR.value
        finally:
            
            return response