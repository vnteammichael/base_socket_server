"""Database client"""
from core.base.singleton_pattern import SingletonMeta
from utils.log import LOGGER
import mysql.connector
from .sql_queries import *
from typing import Dict, Any, List
import json
from .config import config 

class MariaDBConnector(metaclass=SingletonMeta):
    """MariaDB Database class"""

    def __init__(self):
        None

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cache = {}
        self.connect()

    def connect(self):
        if self.conn is None or  not self.conn.is_connected():
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            except Exception as e:
                LOGGER.error(e)
                raise e

    def insert_new_user(self, user_name: str):
        """
        Insert a new user into the database and return the user ID.

        Args:
            username (str): The name of the user.

        Returns:
            int: The user_id of the newly created user.
        """
        self.connect()
        query = """
            INSERT INTO user (username)
            VALUES (%s)
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (user_name,))
            self.conn.commit()

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
        self.connect()
        query = """
            INSERT INTO game_histories (user_id, game_id, bet_amount, win_amount, line_win_detail, symbol_detail)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (user_id, game_id, bet_amount, win_amount, json.dumps(line_win_detail), json.dumps(symbol_detail)))
            self.conn.commit()

    def check_user_bet_balance(self, user_id: int, bet: float):
        query = """
            SELECT balance
            FROM user
            WHERE id = %s
        """
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, (user_id, ))
            result = cursor.fetchone()
        return result[0]>bet

    def update_user_balance(self, user_id: int, amount: float):
        query = """
            UPDATE user
            SET balance = balance +  %s
            WHERE id = %s
        """
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, (amount, user_id))
            self.conn.commit()

    def get_user_balance(self, user_id: int):
        query = """
            SELECT balance
            FROM user
            WHERE id = %s
        """
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, (user_id, ))
            result = cursor.fetchone()

        return result[0]
    
    def get_user_data(self, user_id: int):
        query = """
            SELECT username, balance
            FROM user
            WHERE id = %s
        """
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, (user_id, ))
            result = cursor.fetchone()
        return {"username":result[0], "balance":result[1]}

    def check_username_exists(self, user_name: str) -> int:
        query = """
            SELECT id FROM user
            WHERE username = %s
        """
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, (user_name,))
            result = cursor.fetchone()
        return result[0] if result else None

    def get_symbol_config(self, id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT id, symbol, rate, position FROM symbol_config WHERE bet_id = %s
        """
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, (id,))
            return [{'symbol': row[1], 'rate': row[2], 'position': row[3]} for row in cursor.fetchall()]

    def get_symbol_reward(self) -> List[Dict[str, Any]]:
        query = """
            SELECT id, symbol, symbols_per_line, reward_multiplier FROM symbol_reward
        """
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return [{'symbol': row[1], 'symbols_per_line': row[2], 'reward_multiplier': row[3]} for row in cursor.fetchall()]

    def get_all_games(self) -> List[Dict[str, Any]]:
        query = """
            SELECT id, code, title FROM game_type
        """
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return [{'game_id': row[0], 'game_code': row[1], 'game_title': row[2]} for row in cursor.fetchall()]

    def get_all_bet_rates(self) -> List[Dict[str, Any]]:
        query = """
            SELECT id, bet_amount, game_id FROM bet_config
        """
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return [{'bet_id': row[0], 'bet_amount': row[1], 'game_id': row[2]} for row in cursor.fetchall()]

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None



db = MariaDBConnector(host=config.get("db_host"),port=config.get("db_port"),user=config.get("db_user"),password=config.get("db_password"),database=config.get("db_database"))