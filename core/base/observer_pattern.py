

class Observable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

class ClientHandler:
    def __init__(self, connection):
        self.connection = connection

    async def update(self, message):
        await self.connection.send(message)

    async def close(self):
        await self.connection.close()

    def is_closed(self):
        return self.connection.closed