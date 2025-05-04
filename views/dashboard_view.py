from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QMainWindow, QStackedWidget, QHBoxLayout, QSizePolicy

class DashboardUI(QMainWindow):
    def __init__(self):
        # Initialize window, window name, and layout to be used.
        super().__init__()
        self.setWindowTitle("CC15 Banking System")
        self.setStyleSheet("background: #ffffff")

        #Initialize HBoxLayout
        self.layout = QHBoxLayout()

        #Initialize central widget
        self.central_widget = QWidget()

        #Initialize StackedWidget
        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        #Initialize NavBar 
        self.navbar = uic.loadUi(r"resources\ui-files\navbar.ui")
        self.navbar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        #Add elements to layout
        self.layout.addWidget(self.navbar)
        self.layout.addWidget(self.stack)

        self.layout.setStretch(0, 1)
        self.layout.setStretch(1, 4)

        #Add elements to stack
        self.dashboard = uic.loadUi(r"resources\ui-files\bank_dashboard.ui")
        self.transferPanel = uic.loadUi(r"resources\ui-files\transfer_panel.ui")
        self.depositPanel = uic.loadUi(r"resources\ui-files\deposit_panel.ui")
        self.withdrawPanel = uic.loadUi(r"resources\ui-files\withdraw_panel.ui")

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.transferPanel)
        self.stack.addWidget(self.depositPanel)
        self.stack.addWidget(self.withdrawPanel)

        #Set central widget
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)