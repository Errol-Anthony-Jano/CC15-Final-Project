import sqlite3, hashlib

class Database:
    def __init__(self):
        self.db_path = "banking.db"
        self.conn = sqlite3.connect(self.db_path)
        self.sql = self.conn.cursor()

        self.__app_secret = "74a58c3bfe1c279c0e4e629554e9f104df253a33"
        self.__db_setup()


    def __db_setup(self):
        DEFAULT_TABLES = [
            "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, username TEXT, password TEXT)",
        ]

        for table in DEFAULT_TABLES:
            self.sql.execute(table)
            self.conn.commit()


    def hash_password(self, plaintext):
        salted_pass = self.__app_secret + plaintext
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
        password_hash = self.db.hash_password(password)


        self.db.sql.execute("INSERT INTO users(first_name, last_name, username, password) VALUES(?,?,?,?)", (first_name, last_name, username, password_hash))
        self.db.conn.commit()


    def verify_login(self, username, password):
        username = username.strip()
        password = self.db.hash_password(password)

        self.db.sql.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        results = self.db.sql.fetchall()
        return len(results) > 0

