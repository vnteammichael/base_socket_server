import json

class Config:
    def __init__(self):
        self._config = {}
        self.load_config()

    def load_config(self):
        with open('config.json', 'r') as config_file:
            self._config = json.load(config_file)

    def get(self, key):
        return self._config.get(key)
    
    def get_demo_symbol_rate(self) -> dict:
        #demo rate
        symbol_rate = {}
                # ô           1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
        symbol_rate['0'] = [ 40, 40, 20, 10, 10, 40, 40, 20, 10, 10, 40, 40, 20, 10, 10]
        symbol_rate['1'] = [ 40, 40, 20, 10, 10, 40, 40, 20, 10, 10, 40, 40, 20, 10, 10]
        symbol_rate['2'] = [ 30, 30, 20, 10, 10, 30, 30, 20, 10, 10, 30, 30, 20, 10, 10]
        symbol_rate['3'] = [ 30, 20, 20, 10, 10, 30, 30, 20, 10, 10, 30, 30, 20, 10, 10]
        symbol_rate['4'] = [ 20, 20, 20, 10, 10, 10, 20, 20, 20, 10, 20, 20, 20, 10, 10]
        symbol_rate['5'] = [ 20, 20, 20, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        # symbol_rate['6'] = [ 10, 10, 40, 10, 10, 10, 10, 40, 10, 10, 10, 10, 40, 10, 10]
        # symbol_rate['7'] = [ 10, 10, 40, 10, 10, 10, 10, 40, 10, 10, 10, 10, 40, 10, 10]
        symbol_rate['wild'] = [ 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5] #wild symbol
        symbol_rate['scatter'] = [ 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10] #free symbol

        return symbol_rate
    
    def get_demo_symbol_reward(self) -> dict:
        #demo rate
        symbol_reward = {}
        symbol_reward['0'] = {3:5, 4:7, 5:10}
        symbol_reward['1'] = {3:5, 4:7, 5:10}
        symbol_reward['2'] = {3:5, 4:7, 5:10}
        symbol_reward['3'] = {3:5, 4:7, 5:10}
        symbol_reward['4'] = {3:5, 4:7, 5:10}
        symbol_reward['5'] = {3:5, 4:7, 5:10}
        # symbol_reward['6'] = {3:5, 4:7, 5:10}
        # symbol_reward['7'] = {3:5, 4:7, 5:10}
        symbol_reward['wild'] = {3:5, 4:7, 5:10} #wild symbol
        # symbol_reward['9'] = {3:5, 4:7, 5:10} #free symbol

        return symbol_reward

# Global instance
config = Config()