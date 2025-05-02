from PyQt6.QtWidgets import QWidget
from signup import Ui_SignupWindow

class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SignupWindow()
        self.ui.setupUi(self)