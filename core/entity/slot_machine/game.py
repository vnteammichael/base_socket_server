from core.entity.slot_machine.base_game import BaseGame
from utils.config import config
import asyncio

class Game(BaseGame):
    def __init__(self, game_code):
        super().__init__(game_code)

    

