from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from views.dashboard_view import DashboardUI
from controllers.dashboard_control import DepositControl
from controllers.login_control import LoginAppControl
from controllers.dashboard_control import DashboardAppControl
from controllers.register_control import RegisterAppControl
from controllers.dashboard_control import WithdrawControl
from models.user_session import UserSession
from models.models import UserModel
import sys, sqlite3, hashlib


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("CC15 Banking System")
        self.setStyleSheet("background: #ffffff")
        self.session = UserSession()
        self.user_model = UserModel()

        # initialize qstackedwidget for switching between login/register and main menu
        self.central_widget = QStackedWidget()

        # set central_widget as central widget
        self.setCentralWidget(self.central_widget)

        self.loginPanel = uic.loadUi(r"resources\ui_files\login.ui")
        self.registerPanel = uic.loadUi(r"resources\ui_files\signup_resized.ui")
        self.dashboard = DashboardUI()

        self.central_widget.addWidget(self.loginPanel) #index 0
        self.central_widget.addWidget(self.registerPanel) # index 1 
        self.central_widget.addWidget(self.dashboard) # index 2



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    
    login_control = LoginAppControl(window)
    dashboard_control = DashboardAppControl(window)
    register_control = RegisterAppControl(window)

    deposit_control = DepositControl(window, dashboard_control)
    withdraw_control = WithdrawControl(window, dashboard_control)
    window.show()
    app.exec()
