
from core.base.singleton_pattern import SingletonMeta

class UserManager(metaclass=SingletonMeta):

    def __init__(self):
        self.users = {}  # Stores user data, keyed by user ID
        self.online_users = set()  # Tracks online users by user ID

    def add_user(self, user_id, user_data):
        if user_id not in self.users:
            self.users[user_id] = user_data

    def is_have_user(self, user_id):
        if user_id not in self.users:
            return False
        return True
    
    def get_user_data(self, user_id):
        if user_id not in self.users:
            return None
        return self.users[user_id]

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            self.online_users.discard(user_id)

    def set_online(self, user_id):
        if user_id in self.users:
            self.online_users.add(user_id)

    def set_offline(self, user_id):
        if user_id in self.online_users:
            self.online_users.remove(user_id)

    def get_online_users(self):
        return {user_id: self.users[user_id] for user_id in self.online_users}
    

user_manager = UserManager()