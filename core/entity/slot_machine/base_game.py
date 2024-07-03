
from utils.database_connect import db
import random


class BaseGame:
    def __init__(self, code):
        self.game_code = code
        
        self.symbols_rewards = {} #read from database
        self.symbols_rate = {} #read from database
        self.grid = None
        self.free_spin_nums = 0
        self.free_spin_multi = 1
        self.id_symbol_config_free_game = 5
        self.id_symbol_config = 1
        self.get_symbol_reward_from_db()

    async def play(self,id_symbol_config):
        self.id_symbol_config = id_symbol_config
        self.get_symbol_config_from_db(self.id_symbol_config)

        self.grid = self.gen_grid()
        # self.grid =  [['4', '5', 'scatter'],['0', 'scatter', '0'],['scatter', '3', '5'],['4', '4', '0'],['3', '5', '5']]
        # self.grid =  [['wild', '4', '0'],['4', '4', '1'],['0', '1', '4'],['3', '4', '5'],['5', '1', '0']]

        
         
        
        total_reward, reward_description, is_free_spin = self.calculate_rewards()
        data = {
            'result': self.grid,
            'line_win': reward_description,
            'total_reward': total_reward,
            'is_free_game': is_free_spin,
            'bonus_reward': 0,
            'bonus': []
        }
        if is_free_spin:
            data['bonus_reward'], data['bonus'] = await self.free_game_play()
        return data
    
    async def free_game_play(self):
        self.get_symbol_config_from_db(self.id_symbol_config_free_game)
        bonus_data = []
        rewards = 0
        while self.free_spin_nums > 0:
            data = {}
            self.grid = self.gen_grid()
            reward, reward_description, is_free_game = self.calculate_rewards()
            data['result'] = self.grid
            data['reward'] = reward
            data['line_win'] = reward_description
            bonus_data.append(data)
            rewards += reward
            self.free_spin_nums -= 1
        self.get_symbol_config_from_db(self.id_symbol_config)
        return rewards, bonus_data
    
    def get_symbol_by_cell(self,cell,with_free_symbol = True) -> int:
        result = 0

        total = sum([rate[cell] for rate in self.symbols_rate.values()])
        cumulative_score = 0

        rand_num = random.randint(0,total)

        for symbol,values in self.symbols_rate.items():
            cumulative_score += values[cell]
            if rand_num <= cumulative_score:
                result = symbol
                break
            
        return result
    
    def gen_grid(self, is_free_spin = False):
        # có thể thêm điều kiện để chọn ra bộ rate phù hợp
        grid = []
        for i in range(5):
            col = []
            have_free_symbol = False
            for j in range(3):
                if have_free_symbol :
                    symbol = self.get_symbol_by_cell(i+j*5,False)
                else:
                    symbol = self.get_symbol_by_cell(i+j*5)
                if symbol == 'scatter':
                    have_free_symbol = True
                col.append(symbol)
            grid.append(col)
        return grid

    def count_symbol_in_col(self,symbol,col):
        count = 0
        is_wild = True
        for s in col:
            if s == symbol and s!="wild":
                count += 1
                is_wild = False
            if  s=="wild":
                count +=1
        return count, is_wild
    
    def calculate_rewards(self):
        total_reward = 0
        reward_description = {}
        is_free_spin = False
        # Iterate over each symbol to find its matches across the columns
        for symbol, rewards in self.symbols_rewards.items():
            # Initialize a list to keep track of matches for each symbol
            matches = [0] * 5
            is_wild_valid = True
            for col_index, col in enumerate(self.grid):
                matches[col_index],is_wild = self.count_symbol_in_col(symbol=symbol,col=col)
                is_wild_valid = is_wild_valid & is_wild

            if is_wild_valid and symbol != "wild":
                continue
            consecutive = 0
            reward_multi = 1
            for match in matches:
                if match == 0:
                    if consecutive>=3 and symbol != "scatter":
                        reward_description[symbol] = {}
                        reward_description[symbol]['symbol'] = symbol
                        reward_description[symbol]['reward_multi'] = reward_multi
                        reward_description[symbol]['reward'] = reward_multi * rewards.get(consecutive, 0)
                        reward_description[symbol]['consecutive'] = consecutive
                        total_reward += reward_description[symbol]['reward']
                    elif consecutive>=3 and symbol == "scatter":
                        is_free_spin = True
                        self.free_spin_nums += rewards.get(consecutive, 0)
                        reward_description[symbol] = {}
                        reward_description[symbol]['symbol'] = symbol
                        reward_description[symbol]['reward_multi'] = reward_multi
                        reward_description[symbol]['reward'] = rewards.get(consecutive, 0)
                        reward_description[symbol]['consecutive'] = consecutive
                    break
                else:
                    consecutive += 1
                    reward_multi *= match
            if consecutive == 5 and symbol == "scatter":
                is_free_spin = True
                self.free_spin_nums += rewards.get(consecutive, 0)
                reward_description[symbol] = {}
                reward_description[symbol]['symbol'] = symbol
                reward_description[symbol]['reward_multi'] = reward_multi
                reward_description[symbol]['reward'] = rewards.get(consecutive, 0)
                reward_description[symbol]['consecutive'] = consecutive
            elif consecutive == 5:
                reward_description[symbol] = {}
                reward_description[symbol]['symbol'] = symbol
                reward_description[symbol]['reward_multi'] = reward_multi
                reward_description[symbol]['reward'] = reward_multi * rewards.get(consecutive, 0)
                reward_description[symbol]['consecutive'] = consecutive
                total_reward += reward_description[symbol]['reward']

                
        return total_reward, reward_description, is_free_spin
    
    def get_symbol_config_from_db(self, id:int):
        temp = db.get_symbol_config(id)
        self.symbols_rate = {}
        for i in temp:
            if i['symbol'] not in self.symbols_rate:
                self.symbols_rate[i["symbol"]] = list(range(15))
            self.symbols_rate[i["symbol"]][i['position']-1] = i['rate']

    def get_symbol_reward_from_db(self):
        temp = db.get_symbol_reward()
        self.symbols_rewards = {}
        for i in temp:
            if i['symbol'] not in self.symbols_rewards:
                self.symbols_rewards[i["symbol"]] = {}
            self.symbols_rewards[i["symbol"]][i['symbols_per_line']] = i['reward_multiplier']

    
