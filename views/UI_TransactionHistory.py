from PyQt6.QtWidgets import QWidget
from resources.ui_files.transaction_history import Ui_Form

class UI_TransactionHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
