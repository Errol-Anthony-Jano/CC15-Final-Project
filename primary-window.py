from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login = uic.loadUi(r"resources\ui-files\login.ui")
        self.dashboard = uic.loadUi(r"resources\ui-files\bank-dashboard.ui")

        self.stack.addWidget(self.login)
        self.stack.addWidget(self.dashboard)

        self.login.pushButton.clicked.connect(self.showDashboard)
        self.dashboard.btn_logout.clicked.connect(self.showLogin)

    
    def showDashboard(self):
        self.stack.setCurrentIndex(1)

    def showLogin(self):
        self.stack.setCurrentIndex(0)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()