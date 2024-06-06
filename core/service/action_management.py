# from queue import Queue, Full
from core.base.singleton_pattern import SingletonMeta
from core.service.actions import ActionType,Action
import asyncio
import json


class ActionManager(metaclass=SingletonMeta):
    def __init__(self, max_queue_size=5000,max_workers=10):
        self.action_queue = asyncio.Queue(maxsize=max_queue_size)
        # self.executor = ThreadPoolExecutor(max_workers=max_workers)  # Example: 10 worker threads
        self.handlers = {action: [] for action in ActionType}

    def register_handler(self, action_type:ActionType, handler):
        """Register a handler for a specific action type."""
        if action_type in self.handlers:
            self.handlers[action_type].append(handler)
        else:
            print(f"Event type {action_type} is not recognized.")

    async def unregister_handler(self, action_type:ActionType, handler):
        """Unregister a handler for a specific action type."""
        if action_type in self.handlers:
            self.handlers[action_type].remove(handler)

    async def post_event(self, action:Action):
        """Post an action to the queue."""
        await self.action_queue.put(action)

    async def _dispatch_event(self):
        
        """Dispatch an action to its registered handlers."""
        while True:
            try:
                action = await self.action_queue.get()
                if action.get_type() in self.handlers:
                    for handler in self.handlers[action.get_type()]:
                        response = await handler.handle(action)
                    if response and action.client_handler:
                        message = json.dumps(response)
                        await action.client_handler.update(message)
                self.action_queue.task_done()
            except Exception as e:
                continue
            

    def run(self):
        """Run the event processing loop."""
        
        self.dispatch_task = asyncio.create_task(self._dispatch_event())



