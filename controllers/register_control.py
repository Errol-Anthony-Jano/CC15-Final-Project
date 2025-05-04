from PyQt6.QtWidgets import QMessageBox
from models.models import UserModel

class RegisterAppControl:
    def __init__(self, window):
        self.main_window = window
        self.main_window.registerPanel.btn_register.clicked.connect(self.register)
        self.user = UserModel()


    def showLogin(self):
        self.main_window.central_widget.setCurrentIndex(0)
    

    def register(self):
        first_name = self.main_window.registerPanel.lineEdit
        last_name = self.main_window.registerPanel.lineEdit_2
        email = self.main_window.registerPanel.lineEdit_3
        password = self.main_window.registerPanel.lineEdit_4
        confirm = self.main_window.registerPanel.lineEdit_5

        user_data = {
            'first_name': first_name.text(),
            'last_name': last_name.text(),
            'username': email.text().strip(),
            'password': password.text()
        }

        for key, value in user_data.items():
            if(value.strip() == "" or value is None):
                QMessageBox.warning(self.main_window, "Registration Failed", f"{key.title()} must not be empty!")
                return

        if(self.user.isUsernameExists(email.text())):
            QMessageBox.warning(self.main_window, "Registration Failed", "Username/Email already exists!")
            return

        if(password.text() != confirm.text()):
            QMessageBox.warning(self.main_window, "Registration Failed", "Password and Confirm Password must match!")
            return
        
        self.user.register(user_data)
        self.showLogin()

        first_name.clear()
        last_name.clear()
        email.clear()
        password.clear()
        confirm.clear()


