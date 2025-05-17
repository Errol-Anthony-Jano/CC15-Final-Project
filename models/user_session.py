class UserSession:
    def __init__(self):
        self.user_id = None
        self.first_name = None
        self.last_name = None
        self.username = None
        self.account_number = None
        self.balance = None # stored in cents, displayed in pesos

    def get_user_id(self):
        return self.user_id

    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name

    def get_username(self):
        return self.username

    def get_account_number(self):
        return self.account_number

    def get_password(self):
        return self.password

    def get_balance(self):
        return self.balance

    # SETTERS

    def set_user_id(self, user_id):
        self.user_id = user_id
    
    def set_first_name(self, first_name):
        self.first_name = first_name
    
    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_username(self, username):
        self.username = username

    def set_account_number(self, account_number):
        self.account_number = account_number

    def set_password(self, password):
        self.password = password

    def set_balance(self, balance):
        self.balance = balance

    def set_personal_information(self, first_name=None, last_name=None, username=None):
        if first_name is not None: 
            self.first_name = first_name

        if last_name is not None:
            self.last_name = last_name

        if username is not None:
            self.username = username