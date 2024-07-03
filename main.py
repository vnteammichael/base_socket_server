from core.service.game_factory import GameFactory
from network.server import GameServer
import asyncio
from utils.config import config
from core.entity.slot_machine.game import Game
from core.service.action_management import ActionType
from utils.database_connect import MariaDBConnector
import time

if __name__ == "__main__":
    HOST = config.get('host')
    PORT = config.get('port')
    TIMEOUT = 180  # 60 seconds timeout
    server = GameServer(HOST, PORT, TIMEOUT)
    asyncio.run(server.start())

    