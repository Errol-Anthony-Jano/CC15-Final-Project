import sqlite3, hashlib, secrets, random
from decimal import *

class Database:
    def __init__(self):
        self.db_path = "banking.db"
        self.conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.sql = self.conn.cursor()

        # self.__app_secret = "74a58c3bfe1c279c0e4e629554e9f104df253a33"
        self.__db_setup()


    def __db_setup(self):
        DEFAULT_TABLES = [
            "CREATE TABLE IF NOT EXISTS users(" +
                "user_id INTEGER PRIMARY KEY AUTOINCREMENT," + 
                "account_number VARCHAR(12) UNIQUE," + 
                "first_name TEXT," +
                "last_name TEXT," +
                "username TEXT," +  
                "hashed_password TEXT," +
                "pass_salt TEXT)",
            
            "CREATE TABLE IF NOT EXISTS users_balance(" + 
                "user_id INTEGER," + 
                "account_number VARCHAR(12)," +
                "balance INTEGER," + 
                
                "FOREIGN KEY (user_id) REFERENCES users(user_id))",

            "CREATE TABLE IF NOT EXISTS transaction_history(" +
                "transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, " + 
                "user_id INTEGER, " +
                "transaction_type_id INTEGER, " +
                "transaction_amount DECIMAL(15,2), " +
                "transaction_date DATE," +
                "transaction_time TIME)",

            "CREATE TABLE IF NOT EXISTS transaction_type_table(" + 
            "transaction_type_id INTEGER PRIMARY KEY," +
            "transaction_type VARCHAR(255))"
        ]

        for table in DEFAULT_TABLES:
            self.sql.execute(table)
            self.conn.commit()


    def hash_password(self, plaintext, salt):
        salted_pass = salt + plaintext
        hashed_pw = hashlib.sha256(salted_pass.encode())    
        return hashed_pw.hexdigest()


class UserModel:
    def __init__(self):
        self.db = Database()


    def isUsernameExists(self, username):
        self.db.sql.execute("SELECT * FROM users WHERE username = ?", (username,))
        results = self.db.sql.fetchall()
        return len(results) > 0


    def get_user_data(self, username):
        self.db.sql.execute("SELECT * FROM users WHERE username = ?", (username,))
        results = self.db.sql.fetchall()

        return results

    
    def register(self, data={}):
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        password = data['password']
        salt = secrets.token_hex(16)
        account_number = "000000000000"
        password_hash = self.db.hash_password(password, salt)

        self.db.sql.execute("INSERT INTO users(account_number, first_name, last_name, username, hashed_password, pass_salt) VALUES(?,?,?,?,?,?)", (account_number, first_name, last_name, username, password_hash, salt))
        self.db.conn.commit()

        self.db.sql.execute("SELECT LAST_INSERT_ROWID()")
        last_insert_id = self.db.sql.fetchone()[0]
        account_number = self.generate_account_number(last_insert_id)

        self.db.sql.execute("UPDATE users SET account_number = ? WHERE user_id = ?", (account_number, last_insert_id))
        self.db.conn.commit()

        balance = 0
        
        self.db.sql.execute("INSERT INTO users_balance(user_id, account_number, balance) VALUES(?, ?, ?)", (last_insert_id, account_number, balance))
        self.db.conn.commit()


    def verify_login(self, username, password):
        username = username.strip()
        self.db.sql.execute("SELECT * FROM users WHERE username = ?", (username,))

        
        results = self.db.sql.fetchall()

        salt = ""
        if len(results) > 0:
            salt = results[0][6]
        else:
            return False
        
        password = self.db.hash_password(password, salt)

        if password == results[0][5]:
            return True
        
        return False
    
    def generate_account_number(self, last_insert_id):
        account_number = str(last_insert_id).zfill(12)
        return account_number

    def get_balance(self, user_id):
        self.db.sql.execute("SELECT balance FROM users_balance WHERE user_id = ?", (user_id,))
        result = self.db.sql.fetchone()
        return result[0]

    def get_balance_by_account_number(self, account_number):
        self.db.sql.execute("SELECT balance FROM users_balance WHERE account_number = ?", (account_number,))
        result = self.db.sql.fetchone()
        return result[0]
    
    def update_balance(self, balance, account_number):
        self.db.sql.execute("UPDATE users_balance SET balance = ? WHERE account_number = ?", (balance, account_number))
        self.db.conn.commit()


    def check_existing_recipient(self, account_number, first_name, last_name):
        self.db.sql.execute("SELECT * FROM users where account_number = ? AND first_name = ? AND last_name = ?", (account_number,first_name, last_name))
        result = self.db.sql.fetchone()
        return len(result) > 0


    