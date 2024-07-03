import asyncio
import json
import websockets
from core.service.action_management import ActionManager
from core.service.actions import Action, ActionType
from utils.config import config
from core.base.observer_pattern import ClientHandler
from core.handler.login_handler import LoginHandler
from core.handler.spin_handler import SpinHandler

class GameServer:
    def __init__(self, host, port, timeout=600):
        self.host = host
        self.port = port
        self.timeout = timeout  # Timeout for client connections in seconds
        self.clients = set()  # Track client websockets
        self.token_to_client = {}  # Track JWT token to client handler
        self.action_manager = ActionManager()

        self.action_manager.register_handler(action_type=ActionType.LOGIN,handler=LoginHandler(self))
        self.action_manager.register_handler(action_type=ActionType.PLAY,handler=SpinHandler())


    async def serve(self):
        async with websockets.serve(self.handle_client, self.host, self.port):
            print(f"Server listening on {self.host}:{self.port}")
            await asyncio.Future()  # Run forever

    async def handle_client(self, websocket, path):
        addr = websocket.remote_address
        print(f"New connection from {addr}")
        client_handler = ClientHandler(websocket)
        self.clients.add(client_handler)


        try:
            # Main loop to receive messages with timeout
            while True:
                try:
                    # Wait for a message from the client, with timeout
                    message = await asyncio.wait_for(websocket.recv(), timeout=self.timeout)

                    # Process the message
                    data = json.loads(message)

                    action = Action(data=data, client_handler=client_handler)  # Adapt as necessary
                    await self.action_manager.post_event(action)
                except asyncio.TimeoutError:
                    print("Timeout: No messages received, closing connection.")
                    await client_handler.update(json.dumps({"cmd": ActionType.DISCONNECT.value, "data":{"msg": "Timeout: No messages received, closing connection."}}))
                
                    break  # Exit the loop to close the connection

        except websockets.ConnectionClosed:
            print("Connection closed by the client.")
        finally:
            print("Closing connection.")
            await websocket.close()
            self.clients.remove(client_handler)
            for k,v in list(self.token_to_client.items()):
                if v.is_closed():
                    del self.token_to_client[k]

    async def start(self):
        # Start the server
        # threading.Thread(target=self.action_manager.run).start()
        self.action_manager.run()
        await self.serve()

