"""Database client"""
from utils.log import LOGGER
import mysql.connector
from .sql_queries import *
from typing import Dict, Any, List
import json

class MariaDBConnector:
    """MariaDB Database class"""

    
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cache = {}

    def connect(self):
        if self.conn is None:
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    charset="utf8mb3"
                )
            except Exception as e:
                LOGGER.error(e)
                raise e

    def insert_new_user(self, user_name: str) -> int:
        """
        Insert a new user into the database and return the user ID.
        
        Args:
            username (str): The name of the user.
            
        Returns:
            int: The user_id of the newly created user.
        """
        query = """
            INSERT INTO user (username)
            VALUES (%s)
        """
        self.cursor.execute(query, (user_name,))
        self.connection.commit()
        
        self.cursor.execute("SELECT LAST_INSERT_ID()")
        user_id = self.cursor.fetchone()['LAST_INSERT_ID()']
        return user_id

    def insert_new_history(self, user_id: int, game_id: int, bet_amount: float, win_amount: float, line_win_detail: Dict[str, Any], symbol_detail: Dict[str, Any]) -> int:
        """
        Insert a new game history record into the database.
        
        Args:
            user_id (int): The ID of the user.
            game_id (int): The ID of the game.
            bet_amount (float): The amount bet in the game.
            win_amount (float): The amount won in the game.
            line_win_detail (dict): The line win details as a JSON object.
            symbol_detail (dict): The symbol details as a JSON object.
            
        Returns:
            int: The id of the newly created history record.
        """
        query = """
            INSERT INTO game_histories (user_id, game_id, bet_amount, win_amount, line_win_detail, symbol_detail)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (user_id, game_id, bet_amount, win_amount, json.dumps(line_win_detail), json.dumps(symbol_detail)))
        self.connection.commit()
        
        self.cursor.execute("SELECT LAST_INSERT_ID()")
        history_id = self.cursor.fetchone()['LAST_INSERT_ID()']
        return history_id

    def update_user_balance(self, user_id: int, new_balance: float):
        query = """
            UPDATE user
            SET balance = %s
            WHERE user_id = %s
        """
        self.cursor.execute(query, (new_balance, user_id))
        self.connection.commit()

    def check_username_exists(self, user_name: str) -> int:
        query = """
            SELECT id FROM user
            WHERE username = %s
        """
        self.cursor.execute(query, (user_name,))
        result = self.cursor.fetchone()
        return result['user_id'] if result else None

    def get_symbol_config(self) -> List[Dict[str, Any]]:
        query = """
            SELECT id, symbol, rate, position, bet_id FROM symbol_config
        """
        self.cursor.execute(query)
        return [{'symbol_id': row['id'], 'symbol': row['symbol'], 'rate': row['rate'], 'position': row['position'], 'bet_id': row['bet_id']} for row in self.cursor.fetchall()]

    def get_all_games(self) -> List[Dict[str, Any]]:
        query = """
            SELECT id, code, title FROM game_type
        """
        self.cursor.execute(query)
        return [{'game_id': row['id'], 'game_code': row['code'], 'game_title': row['title']} for row in self.cursor.fetchall()]

    def get_all_bet_rates(self) -> List[Dict[str, Any]]:
        query = """
            SELECT id, bet_amount,game_id FROM bet_rates
        """
        self.cursor.execute(query)
        return [{'bet_id': row['id'], 'bet_amount': row['bet_amount'], 'game_id': row['game_id']} for row in self.cursor.fetchall()]

    def close(self):
        self.cursor.close()
        self.connection.close()
        
    



