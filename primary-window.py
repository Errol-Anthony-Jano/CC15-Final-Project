from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QStackedWidget, QHBoxLayout, QSizePolicy

class MainWindow(QMainWindow):
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
        self.dashboard = uic.loadUi(r"resources\ui-files\bank-dashboard.ui")
        self.transferPanel = uic.loadUi(r"resources\ui-files\transfer-panel.ui")

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.transferPanel)

        #Set central widget
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)


        self.navbar.btn_transfer.clicked.connect(self.showTransferPanel)
        self.navbar.btn_dashboard.clicked.connect(self.showDashboard)

    def showTransferPanel(self):
        self.stack.setCurrentIndex(1)

    def showDashboard(self):
        self.stack.setCurrentIndex(0)

        


        

app = QApplication([])
window = MainWindow()
window.show()
app.exec()