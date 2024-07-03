
from core.base.singleton_pattern import SingletonMeta
from utils.database_connect import db
from utils.config import config
import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler


lock = threading.Lock()

class UserManager(metaclass=SingletonMeta):

    def __init__(self):
        self.online_users = set()  # Tracks online users by user ID
        self.inactive_timeout = config.get("inactive_timeout")
        self.user_last_activity = {}  # Tracks the last activity time of users by user ID
        
        # Initialize the scheduler
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.monitor_user_activity, 'interval', seconds=180, max_instances=2)
        self.scheduler.start()

    def monitor_user_activity(self):
        if lock.acquire(blocking=False):  # Cố gắng lấy khóa mà không chờ đợi
            try:
                # Logic của công việc
                current_time = time.time()
                inactive_users = [user_id for user_id, last_activity in self.user_last_activity.items()
                                if current_time - last_activity > self.inactive_timeout]
                for user_id in inactive_users:
                    self.set_offline(user_id)
            finally:
                lock.release()  # Giải phóng khóa sau khi hoàn thành công việc
        

    def is_have_user(self, user_name):
        result = db.check_username_exists(user_name=user_name)
        return result
    
    def get_user_data(self, user_id):
        user = db.get_user_data(user_id=user_id)
        self.set_online(user_id=user_id)
        return user
    
    def create_new_user(self, user_name):
        db.insert_new_user(user_name=user_name)
        user_id = db.check_username_exists(user_name=user_name)
        self.set_online(user_id=user_id)
        return user_id
    
    def check_bet_available(self, user_id, bet)->bool:
        result = db.check_user_bet_balance(user_id=user_id, bet=bet)
        return result
    
    def update_user_balance(self,user_id,amount):
        db.update_user_balance(user_id=user_id, amount=amount)
        result = db.get_user_balance(user_id=user_id)
        return result
    
    def insert_user_history(self,user_id,bet,game_id,data):

        db.insert_new_history(user_id=user_id,bet_amount=bet,game_id=game_id,win_amount=data['total_reward'],symbol_detail=data['result'],line_win_detail=data['line_win'])
        if data['is_free_game']:
            for i in data['bonus']:
                db.insert_new_history(user_id=user_id,bet_amount=0,game_id=game_id,win_amount=i['reward'],symbol_detail=i['result'],line_win_detail=i['line_win'])
            
    
  

    def set_online(self, user_id):
        self.online_users.add(user_id)
        self.update_user_activity(user_id)

    def set_offline(self, user_id):
        if user_id in self.online_users:
            self.online_users.remove(user_id)
            self.user_last_activity.pop(user_id, None)

    def get_online_users(self):
        return self.online_users
    
    def update_user_activity(self, user_id):
        self.user_last_activity[user_id] = time.time()
    
    def user_action(self, user_id):
        self.update_user_activity(user_id)

    def shutdown_scheduler(self):
        self.scheduler.shutdown()
    

user_manager = UserManager()