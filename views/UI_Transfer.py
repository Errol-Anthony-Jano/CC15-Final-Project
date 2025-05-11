from resources.ui_files.transfer import Ui_Form
from PyQt6.QtWidgets import QWidget

class UI_Transfer(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)