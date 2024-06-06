from network.server import GameServer
import asyncio
from utils.config import config
from core.entity.game import Game
from core.service.action_management import ActionType

if __name__ == "__main__":
    HOST = config.get('host')
    PORT = config.get('port')
    TIMEOUT = 60  # 60 seconds timeout
    server = GameServer(HOST, PORT, TIMEOUT)
    asyncio.run(server.start())
    # game = Game('a')
    # game.play()