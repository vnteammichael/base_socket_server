import random
from utils.config import config

class Game:
    game_code = None
    def __init__(self,game_code):
        self.game_code = game_code
        self.symbols_rewards = config.get_demo_symbol_reward() #read from database
        self.symbols_rate = config.get_demo_symbol_rate() #read from database
        self.grid = None
        self.is_free_spin = False
        self.free_spin_nums = 0


    def play(self):
        #check free game
        if self.is_free_spin:
            self.free_game_play()

        #
        #gen grid
        self.grid = self.gen_grid()
        # self.grid = [['3', '5', 'wild'], ['5', '0', '7'], ['7', 'wild', '3'], ['3', 'wild', '0'], ['5', '4', '1']]
        # self.grid =  [['4', '5', 'wild'],['0', 'wild', '0'],['wild', '6', '5'],['4', '4', '0'],['6', '5', '5']]
        # print(self.grid)
        self.print_grid()

        total_reward, reward_description, is_free_spin = self.calculate_rewards()
        self.is_free_spin = is_free_spin
        # print(f"Total reward: {total_reward}")
        # print(f"Reward description: {reward_description}")
        data = {}
        data['result'] = self.grid
        data['line_win'] = reward_description
        data['total_reward'] = total_reward
        data['is_free_game'] = is_free_spin
        return data
    
    def print_grid(self):

        for i in range(3):
            for j in range(5):
                print(f"{self.grid[j][i]:4} ",end="")
            print()

    
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


    def gen_grid(self):
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
    
    def free_game_play(self,data):
        
        self.free_spin_nums = data['num_spin']
        self.free_spin_multi = data['multi']

        rewards = 0
        reward_descriptions = {}
        count = 0
        while count<self.free_spin_nums:
            self.grid = self.gen_grid()
            reward, reward_description = self.calculate_rewards()
            rewards += reward
            reward_descriptions[count] = reward_description
            count += 1
        

        return rewards, reward_descriptions

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

            if is_wild_valid:
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
                    break
                else:
                    consecutive += 1
                    reward_multi *= match
            if consecutive == 5 and symbol == "scatter":
                is_free_spin = True
            elif consecutive == 5:
                reward_description[symbol] = {}
                reward_description[symbol]['symbol'] = symbol
                reward_description[symbol]['reward_multi'] = reward_multi
                reward_description[symbol]['reward'] = reward_multi * rewards.get(consecutive, 0)
                reward_description[symbol]['consecutive'] = consecutive
                total_reward += reward_description[symbol]['reward']

                
        return total_reward, reward_description, is_free_spin
    

