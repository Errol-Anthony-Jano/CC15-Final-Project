class DashboardAppControl:
    def __init__(self, main_window):
        self.main_window = main_window
        self.session = main_window.session
        self.main_window.dashboard.navbar.btn_dashboard.clicked.connect(self.showDashboard)
        self.main_window.dashboard.navbar.btn_withdraw.clicked.connect(self.showWithdraw)
        self.main_window.dashboard.navbar.btn_deposit.clicked.connect(self.showDeposit)
        self.main_window.dashboard.navbar.btn_transfer.clicked.connect(self.showTransfer)
        self.main_window.dashboard.navbar.btn_logout.clicked.connect(self.showLogin)
        self.main_window.dashboard.navbar.btn_history.clicked.connect(self.showTransactionHistory)
        self.main_window.dashboard.navbar.btn_account.clicked.connect(self.showAccount)


    # index:
    # 0 - dashboard
    # 1 - transfer
    # 2 - deposit
    # 3 - withdraw
    # 4 - transaction history
    # 5 - show account menu

    def showDashboard(self):
        self.main_window.dashboard.stack.setCurrentIndex(0)

    def showWithdraw(self):
        self.main_window.dashboard.stack.setCurrentIndex(3)

    def showDeposit(self):
        self.main_window.dashboard.stack.setCurrentIndex(2)

    def showTransfer(self):
        self.main_window.dashboard.stack.setCurrentIndex(1)

    def showLogin(self):
        self.main_window.central_widget.setCurrentIndex(0)

    def showTransactionHistory(self):
        self.main_window.dashboard.stack.setCurrentIndex(4)

    def showAccount(self):
        self.main_window.dashboard.stack.setCurrentIndex(5)