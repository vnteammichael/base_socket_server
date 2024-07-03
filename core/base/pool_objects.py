from collections import deque
import asyncio
from core.service.game_factory import GameFactory

class ObjectPool:
    def __init__(self, create_instance_func, max_size=10):
        self.pool = deque(maxlen=max_size)
        self.create_instance_func = create_instance_func
        self.max_size = max_size
        self.lock = asyncio.Lock()
        self.condition = asyncio.Condition(self.lock)
        self.current_size = 0

    async def acquire(self, game_code):
        async with self.condition:
            for instance in self.pool:
                if instance.game_code.startswith(game_code[0]):
                    self.pool.remove(instance)
                    return instance

            if self.current_size < self.max_size:
                instance = self.create_instance_func(game_code)
                self.current_size += 1
                return instance
            else:
                await self.condition.wait()
                for instance in self.pool:
                    if instance.game_code.startswith(game_code[0]):
                        self.pool.remove(instance)
                        return instance

    async def release(self, instance):
        async with self.condition:
            if len(self.pool) < self.max_size:
                self.pool.append(instance)
            else:
                self.current_size -= 1
            self.condition.notify()

# Singleton instance of ObjectPool for games
game_pool = ObjectPool(create_instance_func=GameFactory.create_game, max_size=10)
