from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QMainWindow, QStackedWidget, QHBoxLayout, QSizePolicy
from views.UI_Dashboard import UI_Dashboard
from views.UI_Transfer import UI_Transfer
from views.UI_Deposit import UI_Deposit
from views.UI_Withdraw import UI_Withdraw
from views.UI_TransactionHistory import UI_TransactionHistory
from views.UI_AccountMenu import UI_AccountMenu

class DashboardUI(QWidget):
    def __init__(self):
        # Initialize window, window name, and layout to be used.
        super().__init__()
        self.setWindowTitle("CC15 Banking System")
        self.setStyleSheet("background: #ffffff")

        #Initialize HBoxLayout
        self.layout = QHBoxLayout(self)

        #Initialize StackedWidget
        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        #Initialize NavBar 
        self.navbar = uic.loadUi(r"resources\ui_files\navbar.ui")
        self.navbar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        #Add elements to layout
        self.layout.addWidget(self.navbar)
        self.layout.addWidget(self.stack)

        self.layout.setStretch(0, 1)
        self.layout.setStretch(1, 4)

        #Add elements to stack
        self.dashboard = UI_Dashboard()
        self.transferPanel = UI_Transfer()
        self.depositPanel = UI_Deposit()
        self.withdrawPanel = UI_Withdraw()
        self.transactionHistoryPanel = UI_TransactionHistory()

        self.accountPanel = UI_AccountMenu()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.transferPanel)
        self.stack.addWidget(self.depositPanel)
        self.stack.addWidget(self.withdrawPanel)
        self.stack.addWidget(self.transactionHistoryPanel)
        self.stack.addWidget(self.accountPanel)

        # Set displayed balance on screen