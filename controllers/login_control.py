from PyQt6.QtWidgets import QMessageBox
from models.models import UserModel

class LoginAppControl:
    def __init__(self, window):
        self.main_window = window
        self.session = window.session
        self.main_window.loginPanel.btn_login.clicked.connect(self.login)
        self.main_window.loginPanel.btn_register.clicked.connect(self.showRegister)
        self.user = self.main_window.user_model


    def showDashboard(self):
        self.main_window.central_widget.setCurrentIndex(2)
        self.main_window.dashboard.stack.setCurrentIndex(0)


    def showRegister(self):
        self.main_window.central_widget.setCurrentIndex(1)   


    def login(self):
        user_box = self.main_window.loginPanel.lineEdit
        pass_box = self.main_window.loginPanel.lineEdit_2

        username = user_box.text().strip()
        password = pass_box.text()
        
        if(username == "" or password == ""):
            QMessageBox.warning(self.main_window, "Login Failed", "Fields must not be empty!.")
            return

        isVerified = self.user.account_actions.verify_login(username, password)

        if(isVerified):
            
            user_data = self.user.account_actions.get_user_data(username=username)
            

            self.session.set_user_id(user_data[0])
            self.session.set_account_number(user_data[1])
            self.session.set_first_name(user_data[2])
            self.session.set_last_name(user_data[3])
            self.session.set_username(username)
            self.session.set_password(user_data[5]) # modify later
            
            balance = self.user.balance_actions.get_balance(self.session.get_user_id())
            self.session.set_balance(balance)

            self.main_window.dashboard.dashboard.set_balance_display(balance)
            self.main_window.dashboard.accountPanel.set_display_information(user_data[1], user_data[2], user_data[3], username)
            self.main_window.dashboard.dashboard.set_acc_number_display(self.session.get_account_number())
            self.main_window.dashboard.dashboard.setup_table()
            
            result_set = self.user.transaction_actions.load_transactions(self.session.get_user_id(), self.session.get_account_number(), recent_flag=True)
            self.main_window.dashboard.dashboard.populate_table(result_set)
            self.showDashboard()
            user_box.clear()
            pass_box.clear()

        else:
            QMessageBox.warning(self.main_window, "Login Failed", "Incorrect username or password.")
    
    
        

