from core.entity.slot_machine.game import Game


class GameFactory:
    @staticmethod
    def create_game(game_code):
        if game_code == "SL001":
            return Game(game_code)
        else:
            raise ValueError(f"Unknown game code: {game_code}")
