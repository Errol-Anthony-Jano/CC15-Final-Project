class LoginAppControl:
    def __init__(self, window):
        self.main_window = window

        self.main_window.loginPanel.btn_login.clicked.connect(self.showDashboard)
        self.main_window.loginPanel.btn_register.clicked.connect(self.showRegister)
        
    def showDashboard(self):
        self.main_window.central_widget.setCurrentIndex(2)

    def showRegister(self):
        self.main_window.central_widget.setCurrentIndex(1)