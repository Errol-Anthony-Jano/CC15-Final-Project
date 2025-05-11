from PyQt6.QtWidgets import QMessageBox
class DashboardAppControl:
    def __init__(self, main_window):
        self.main_window = main_window
        self.session = main_window.session
        self.user = self.main_window.user_model

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
        self.main_window.dashboard.dashboard.set_balance_display(self.user.get_balance(self.session.get_user_id()))
        self.main_window.dashboard.stack.setCurrentIndex(0)

    def showWithdraw(self):
        self.main_window.dashboard.withdrawPanel.display_balance(self.user.get_balance(self.session.get_user_id()))
        self.main_window.dashboard.stack.setCurrentIndex(3)

    def showDeposit(self):
        self.main_window.dashboard.depositPanel.display_balance(self.user.get_balance(self.session.get_user_id()))
        self.main_window.dashboard.stack.setCurrentIndex(2)

    def showTransfer(self):
        self.main_window.dashboard.stack.setCurrentIndex(1)

    def showLogin(self):
        self.main_window.central_widget.setCurrentIndex(0)

    def showTransactionHistory(self):
        self.main_window.dashboard.stack.setCurrentIndex(4)

    def showAccount(self):
        self.main_window.dashboard.stack.setCurrentIndex(5)

class DepositControl:
    def __init__(self, window, dashboard_control):
        self.main_window = window
        self.deposit_menu = self.main_window.dashboard.depositPanel
        self.dashboard_control = dashboard_control
        self.session = window.session
        self.user = self.main_window.user_model
        self.deposit_menu.ui.btn_confirm.clicked.connect(self.deposit)

    def deposit(self):
        recipient = self.main_window.dashboard.depositPanel.ui.account_box.text()
        recipient_first_name = self.main_window.dashboard.depositPanel.ui.first_name_box.text()
        recipient_last_name = self.main_window.dashboard.depositPanel.ui.last_name_box.text()

        amount = self.main_window.dashboard.depositPanel.ui.amount_box.text().replace(".", '')
        recepient_amount = self.user.get_balance_by_account_number(recipient)

        if (self.user.check_existing_recipient(recipient, recipient_first_name, recipient_last_name) == False):
            QMessageBox.warning(self.main_window, "Transfer Failed", "Invalid account name/number.\nPlease make sure that you entered the correct details.")
            return
    
        new_amount = int(amount) + recepient_amount
        self.user.update_balance(new_amount, recipient)
        self.main_window.dashboard.depositPanel.clear_fields()
        QMessageBox.information(self.main_window, "Transaction Successful", "Transaction successful.")
        
        self.dashboard_control.showDashboard()

class WithdrawControl:
    def __init__(self, window, dashboard_control):
        self.main_window = window
        self.session = self.main_window.session
        self.dashboard_control = dashboard_control
        self.withdraw_menu = self.main_window.dashboard.withdrawPanel
        self.user = self.main_window.user_model

        self.withdraw_menu.ui.btn_confirm.clicked.connect(self.withdraw)

    def withdraw(self):
        user_id = self.session.get_user_id()
        account_number = self.session.get_account_number()

        amount = self.withdraw_menu.ui.amount_box.text().replace(".", "")

        new_amount = self.user.get_balance(user_id) - int(amount)
        
        self.user.update_balance(new_amount, account_number)
        QMessageBox.information(self.main_window, "Transaction Successful", "Transaction successful.")
        self.main_window.dashboard.withdrawPanel.clear_fields()
        self.dashboard_control.showDashboard()

