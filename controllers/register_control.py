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
        first_name = self.main_window.registerPanel.first_name
        last_name = self.main_window.registerPanel.last_name
        user_name = self.main_window.registerPanel.user_name
        password = self.main_window.registerPanel.password_field
        confirm = self.main_window.registerPanel.confirm_password_field

        user_data = {
            'first_name': first_name.text().title(),
            'last_name': last_name.text().title(),
            'username': user_name.text().strip(),
            'password': password.text()
        }

        for key, value in user_data.items():
            if(value.strip() == "" or value is None):
                QMessageBox.warning(self.main_window, "Registration Failed", f"{key.title()} must not be empty!")
                return

        if(self.user.account_actions.isUsernameExists(user_name.text())):
            QMessageBox.warning(self.main_window, "Registration Failed", "Username/Email already exists!")
            return

        if(password.text() != confirm.text()):
            QMessageBox.warning(self.main_window, "Registration Failed", "Password and Confirm Password must match!")
            return
        
        self.user.account_actions.register(user_data)
        QMessageBox.information(self.main_window, "Registration Successful", "You have registered successfully.\nPlease login to start using the app.")
        self.showLogin()

        first_name.clear()
        last_name.clear()
        user_name.clear()
        password.clear()
        confirm.clear()


