from resources.ui_files.transfer import Ui_Form
from PyQt6.QtWidgets import QWidget

class UI_Transfer(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
    
    def clear_fields(self):
        self.ui.account_box.clear()
        self.ui.amount_box.clear()
        self.ui.first_name_box.clear()
        self.ui.last_name_box.clear()
    
    def display_balance(self, balance):
        if balance < 10:
            self.ui.balance_label.setText(f"0.0{balance}")
            return
        elif balance >= 10 and balance < 100:
            self.ui.balance_label.setText(f"0.{balance}")
            return

        str_balance = str(balance)[:-2] + '.' + str(balance)[-2:]
        self.ui.balance_label.setText(str_balance)