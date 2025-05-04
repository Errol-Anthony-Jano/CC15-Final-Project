class RegisterAppControl:
    def __init__(self, window):
        self.main_window = window

        self.main_window.registerPanel.btn_register.clicked.connect(self.showLogin)

    
    def showLogin(self):
        self.main_window.central_widget.setCurrentIndex(0)