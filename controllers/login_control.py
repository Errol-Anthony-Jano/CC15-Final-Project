from PyQt6.QtWidgets import QMessageBox
from models.models import UserModel

class LoginAppControl:
    def __init__(self, window):
        self.main_window = window
        self.session = window.session
        self.main_window.loginPanel.btn_login.clicked.connect(self.login)
        self.main_window.loginPanel.btn_register.clicked.connect(self.showRegister)
        self.user = UserModel()


    def showDashboard(self):
        self.main_window.central_widget.setCurrentIndex(2)


    def showRegister(self):
        self.main_window.central_widget.setCurrentIndex(1)   


    def login(self):
        user_box = self.main_window.loginPanel.lineEdit
        pass_box = self.main_window.loginPanel.lineEdit_2

        username = user_box.text()
        password = pass_box.text()
        
        if(username == "" or password == ""):
            QMessageBox.warning(self.main_window, "Login Failed", "Fields must not be empty!.")
            return

        isVerified = self.user.verify_login(username, password)

        if(isVerified):
            self.session.user_id = self.user.get_user_data(username)[0][0]
            self.session.username = username
            self.showDashboard()
            user_box.clear()
            pass_box.clear()

        else:
            QMessageBox.warning(self.main_window, "Login Failed", "Incorrect username or password.")

