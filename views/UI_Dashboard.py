from PyQt6.QtWidgets import QWidget, QMainWindow, QStackedWidget, QHBoxLayout, QSizePolicy
from resources.ui_files.dashboard import Ui_Form

class UI_Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def set_balance_display(self, balance):
        if balance < 10:
            self.ui.bal_label.setText(f"0.0{balance}")
            return
        elif balance >= 10 and balance < 100:
            self.ui.bal_label.setText(f"0.{balance}")
            return

        str_balance = str(balance)[:-2] + '.' + str(balance)[-2:]
        self.ui.bal_label.setText(str_balance)
        

    def set_acc_number_display(self, account_number):
        self.ui.acct_num_label.setText(account_number)
