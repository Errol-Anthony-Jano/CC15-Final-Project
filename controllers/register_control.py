from PyQt6.QtWidgets import QMessageBox
from models.models import UserModel
from models.utilities import Utilities
import re

class RegisterAppControl:
    def __init__(self, window):
        self.main_window = window
        self.main_window.registerPanel.btn_register.clicked.connect(self.register)
        self.main_window.registerPanel.btn_login.clicked.connect(self.showLogin)
        self.user = UserModel()


    def showLogin(self):
        self.main_window.central_widget.setCurrentIndex(0)
    

    def register(self):
        first_name = self.main_window.registerPanel.first_name
        last_name = self.main_window.registerPanel.last_name
        user_name = self.main_window.registerPanel.user_name
        password = self.main_window.registerPanel.password_field
        confirm = self.main_window.registerPanel.confirm_password_field

        text_first_name = first_name.text().title().strip()
        text_last_name = last_name.text().title().strip()
        text_username = user_name.text().strip()
        text_password = password.text()

        if Utilities.validate_name(text_first_name) == False:
            QMessageBox.critical(self.main_window, "Invalid input", "Invalid first name. Please make sure you entered your name correctly.\nOnly letters, a single apostrophe, and hyphens are allowed.")
            return 
        
        if Utilities.validate_name(text_last_name) == False:
            QMessageBox.critical(self.main_window, "Invalid input", "Invalid last name. Please make sure you entered your name correctly.\nOnly letters, a single apostrophe, and hyphens are allowed.")
            return

        if Utilities.validate_username(text_username) == False:
            QMessageBox.critical(self.main_window, "Invalid input", "Invalid username.\nPlease make sure that your username is 3-20 characters long, and must contain only letters, numbers, and apostrophes or periods.")
            return

        if Utilities.validate_password(text_password) == False:
            QMessageBox.critical(self.main_window, "Invalid input", "Invalid password. Please make sure that your password is at least 8 characters long,\n and must contain at least 1 digit, 1 uppercase and lowercase letter,\n and at least 1 non-alphanumeric character.")
            return
        
        user_data = {
            'first_name': text_first_name,
            'last_name': text_last_name,
            'username': text_username,
            'password': text_password
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


