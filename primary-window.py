from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login = uic.loadUi(r"resources\ui-files\login.ui")
        self.signup = uic.loadUi(r"resources\ui-files\sign-up.ui")
        self.dashboard = uic.loadUi(r"resources\ui-files\bank-dashboard.ui")

        self.stack.addWidget(self.login)
        self.stack.addWidget(self.signup)
        self.stack.addWidget(self.dashboard)

        self.login.btn_login.clicked.connect(self.showDashboard)
        self.dashboard.btn_logout.clicked.connect(self.showLogin)
        self.login.register_button.clicked.connect(self.showRegistration)

    
    def showDashboard(self):
        self.stack.setCurrentIndex(2)

    def showLogin(self):
        self.stack.setCurrentIndex(0)

    def showRegistration(self):
        self.stack.setCurrentIndex(1)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()