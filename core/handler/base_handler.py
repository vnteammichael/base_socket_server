from abc import ABC, abstractmethod
from core.service.actions import Action

class BaseHandler(ABC):
    """
    An abstract base class for action handlers. All handlers should derive from this class
    and implement the handle method.
    """
    
    @abstractmethod
    async def handle(self, action: Action):
        """
        Process an action.

        Parameters:
        action (Action): The action to be processed.

        This method must be overridden by subclasses.
        """
        pass