import sqlite3, hashlib, secrets, random

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
                "user_id INTEGER," +
                "sender_acc_num TEXT," +
                "recipient_acc_num TEXT," + # masked
                "transaction_type TEXT, " +
                "amount TEXT, " +
                "date TEXT," +
                "time TEXT," +
                "FOREIGN KEY (user_id) REFERENCES users(user_id))"
        ]

        for table in DEFAULT_TABLES:
            self.sql.execute(table)
            self.conn.commit()

class UserModel:
    def __init__(self):
        self.db = Database()
        self.account_actions = UserAccountActions(self.db)
        self.balance_actions = UserBalanceActions(self.db)
        self.transaction_actions = UserTransactionActions(self.db)

    def execute_query(self, query):
        self.db.sql.execute(query)
        return self.db.sql.fetchall()

    def execute_update_query(self, query):
        self.db.sql.execute(query)
        self.db.conn.commit()

    def execute_query_via_dict(self, query, dict):
        self.db.sql.execute(query, dict)
        self.db.conn.commit()

class UserAccountActions:
    def __init__(self, db):
        self.db = db

    def hash_password(self, plaintext, salt):
        salted_pass = salt + plaintext
        hashed_pw = hashlib.sha256(salted_pass.encode())    
        return hashed_pw.hexdigest()
    
    def get_salt(self, user_id):
        self.db.sql.execute("SELECT pass_salt FROM users WHERE user_id = ?", (user_id,))
        return self.db.sql.fetchone()[0]

    def get_hashed_password(self, user_id):
        self.db.sql.execute("SELECT hashed_password FROM users WHERE user_id = ?", (user_id,))
        return self.db.sql.fetchone()[0]

    def get_user_id_from_acc_num(self, account_number):
        self.db.sql.execute("SELECT user_id FROM users WHERE account_number = ?", (account_number,))
        return self.db.sql.fetchone()[0]
    
    def get_user_data_by_id(self, user_id):
        self.db.sql.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        results = self.db.sql.fetchone()

        return results
    
    def generate_account_number(self, last_insert_id):
        account_number = str(last_insert_id).zfill(12)
        return account_number
    
    def verify_login(self, username, password):
        username = username.strip()
        self.db.sql.execute("SELECT * FROM users WHERE username = ?", (username,))

        
        results = self.db.sql.fetchall()

        salt = ""
        if len(results) > 0:
            salt = results[0][6]
        else:
            return False
        
        password = self.hash_password(password, salt)

        if password == results[0][5]:
            return True
        
        return False
    
    def register(self, data={}):
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        password = data['password']
        salt = secrets.token_hex(16)
        account_number = "000000000000"
        password_hash = self.hash_password(password, salt)

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

    def isUsernameExists(self, username):
        self.db.sql.execute("SELECT * FROM users WHERE username = ?", (username,))
        results = self.db.sql.fetchall()
        return len(results) > 0

    def get_user_data(self, username):
        self.db.sql.execute("SELECT * FROM users WHERE username = ?", (username,))
        results = self.db.sql.fetchall()

        return results
    
class UserBalanceActions:
    def __init__(self, db):
        self.db = db

    def get_balance(self, user_id=None, account_number=None):
        result = []
        if user_id is not None:
            self.db.sql.execute("SELECT balance FROM users_balance WHERE user_id = ?", (user_id,))
            
        elif account_number is not None: 
            self.db.sql.execute("SELECT balance FROM users_balance WHERE account_number = ?", (account_number,))
        
        result = self.db.sql.fetchone()
        if result is None:
            return None
        return result[0]
    
    def update_balance(self, balance, account_number):
        self.db.sql.execute("UPDATE users_balance SET balance = ? WHERE account_number = ?", (balance, account_number))
        self.db.conn.commit()
    
    def check_existing_recipient(self, account_number, first_name, last_name):
        self.db.sql.execute("SELECT * FROM users where account_number = ? AND first_name = ? AND last_name = ?", (account_number,first_name, last_name))
        result = self.db.sql.fetchone()
        
        if result is None:
            return False
        return True

class UserTransactionActions:
    def __init__(self, db):
        self.db = db

    def record_transaction(self, user_id, sender_acc_num, recipient_acc_num, transaction_type, amount):
        self.db.sql.execute("SELECT DATE('NOW', 'localtime')")
        date = self.db.sql.fetchone()[0]

        self.db.sql.execute("SELECT TIME('NOW', 'localtime')")
        time = self.db.sql.fetchone()[0]

        self.db.sql.execute("INSERT INTO transaction_history (user_id, sender_acc_num, recipient_acc_num, transaction_type, amount, date, time) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, sender_acc_num, recipient_acc_num, transaction_type, amount, date, time))
        self.db.conn.commit()

    def load_transactions(self, user_id, account_number):
        self.db.sql.execute("SELECT sender_acc_num, recipient_acc_num, transaction_type, amount, date, time FROM transaction_history WHERE (user_id = ? AND transaction_type = 'Withdraw') OR (user_id = ? AND transaction_type = 'Deposit')  OR (recipient_acc_num = ? AND transaction_type = 'Transfer - Receiver') OR (sender_acc_num = ? AND transaction_type = 'Transfer - Sender')", (user_id, user_id, account_number, account_number))    
        return self.db.sql.fetchall()
    
    def load_recent_transactions(self, user_id, account_number):
        self.db.sql.execute("SELECT sender_acc_num, recipient_acc_num, transaction_type, amount, date, time FROM transaction_history WHERE (user_id = ? AND transaction_type = 'Withdraw') OR (user_id = ? AND transaction_type = 'Deposit') OR (recipient_acc_num = ? AND transaction_type = 'Transfer - Receiver') OR (sender_acc_num = ? AND transaction_type = 'Transfer - Sender') ORDER BY date DESC, time DESC LIMIT 5", (user_id, user_id, account_number, account_number))
        return self.db.sql.fetchall()

    def load_transactions_by_date(self, user_id, account_number, start_date, end_date):
        self.db.sql.execute("SELECT sender_acc_num, recipient_acc_num, transaction_type, amount, date, time FROM transaction_history WHERE ((user_id = ? AND transaction_type = 'Withdraw') OR (user_id = ? AND transaction_type = 'Deposit') OR (recipient_acc_num = ? AND transaction_type = 'Transfer - Receiver') OR (sender_acc_num = ? AND transaction_type = 'Transfer - Sender')) AND date BETWEEN ? AND ?", (user_id, user_id, account_number, account_number, start_date, end_date))
        return self.db.sql.fetchall()
    
    def load_transactions_by_type(self, query, dict):
        self.db.sql.execute(query, dict)
        return self.db.sql.fetchall()