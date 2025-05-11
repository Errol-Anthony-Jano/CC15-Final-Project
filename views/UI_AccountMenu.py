from PyQt6.QtWidgets import QWidget
from resources.ui_files.account_menu import Ui_Form

class UI_AccountMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def set_display_information(self, account_number, first_name, last_name, username):
        self.ui.dsp_account_number_box.setText(account_number)
        self.ui.dsp_first_name.setText(first_name)
        self.ui.dsp_last_name.setText(last_name)
        self.ui.dsp_username.setText(username)