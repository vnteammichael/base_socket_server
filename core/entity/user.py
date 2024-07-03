
from core.entity.slot_machine.game import Game
from utils.database_connect import db

class User:
    user_id = None
    game:Game = None
    game_code:str = ""

    def __init__(self, user_id, game_code):
        self.user_id = user_id
        self.game_code = game_code
        self.game = Game(game_code=self.game_code)


    def check_bet_available(self,bet)->bool:
        result = db.check_user_bet_balance(bet=bet)
        return result
    
    def call_api_update_result(self,bet,total_rewards):
        self.amount += (total_rewards - bet)
    
    
    def init_game(self)->bool:
        #init game by game code =>
        self.game = Game(game_code=self.game_code)
    
    def play_game(self,bet)->dict:
        data = {}
        if self.check_bet_available(bet=bet):
            if self.game:
                data = self.game.play()
            else:
                data['msg'] = "Not have game"
        else:
            data['msg'] = "Not engough bet"
        return data