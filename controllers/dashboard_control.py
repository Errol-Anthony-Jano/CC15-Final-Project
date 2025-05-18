from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate
from models.utilities import Utilities
import re 

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
        result_set = self.user.transaction_actions.load_transactions(self.session.get_user_id(), self.session.get_account_number(), recent_flag=True)
        self.main_window.dashboard.dashboard.populate_table(result_set)
        self.main_window.dashboard.dashboard.set_balance_display(self.user.balance_actions.get_balance(user_id=self.session.get_user_id()))
        self.main_window.dashboard.stack.setCurrentIndex(0)

    def showWithdraw(self):
        self.main_window.dashboard.withdrawPanel.display_balance(self.user.balance_actions.get_balance(user_id=self.session.get_user_id()))
        self.main_window.dashboard.stack.setCurrentIndex(3)

    def showDeposit(self):
        self.main_window.dashboard.depositPanel.display_balance(self.user.balance_actions.get_balance(user_id=self.session.get_user_id()))
        self.main_window.dashboard.stack.setCurrentIndex(2)

    def showTransfer(self):
        self.main_window.dashboard.transferPanel.display_balance(self.user.balance_actions.get_balance(user_id=self.session.get_user_id()))
        self.main_window.dashboard.stack.setCurrentIndex(1)

    def showLogin(self):
        self.main_window.central_widget.setCurrentIndex(0)

    def showTransactionHistory(self):
        self.main_window.dashboard.transactionHistoryPanel.setup_table()

        result_set = self.user.transaction_actions.load_transactions(self.session.get_user_id(), self.session.get_account_number())
        self.main_window.dashboard.transactionHistoryPanel.populate_table(result_set)
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
        user_id = self.session.get_user_id()
        account_number = self.session.get_account_number()

        recipient = self.main_window.dashboard.depositPanel.ui.account_box.text()
        recipient_first_name = self.main_window.dashboard.depositPanel.ui.first_name_box.text().title()
        recipient_last_name = self.main_window.dashboard.depositPanel.ui.last_name_box.text().title()

        amount_text = self.main_window.dashboard.depositPanel.ui.amount_box.text()

        if Utilities.validate_amount(amount_text) == False:
            QMessageBox.warning(self.main_window, "Invalid amount format", "Please enter the amount using the format XXXX.XX, with no leading zeros on the amount.")
            return
        
        if (self.user.balance_actions.check_existing_recipient(recipient, recipient_first_name, recipient_last_name) == False):
            QMessageBox.warning(self.main_window, "Transfer Failed", "Invalid account name/number.\nPlease make sure that you entered the correct details.")
            return

        amount = amount_text.replace(".", '')
        recepient_amount = self.user.balance_actions.get_balance(recipient)

        if int(amount) ==  0:
            QMessageBox.critical(self.main_window, "Invalid amount", "Please enter a valid amount.")
            return

        new_amount = int(amount) + recepient_amount
        self.user.balance_actions.update_balance(new_amount, recipient)
        self.main_window.dashboard.depositPanel.clear_fields()

        self.user.transaction_actions.record_transaction(user_id, account_number, recipient, "Deposit", Utilities.parse_amount(int(amount)))
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

        amount_text = self.withdraw_menu.ui.amount_box.text()

        if Utilities.validate_amount(amount_text) == False:
            QMessageBox.warning(self.main_window, "Invalid amount format", "Please enter the amount using the format XXXX.XX, with no leading zeros on the amount.")
            return

        amount = amount_text.replace(".", "")
        
        existing_amount = self.user.balance_actions.get_balance(user_id)

        if int(amount) > existing_amount or int(amount) == 0:
            QMessageBox.critical(self.main_window, "Invalid amount", "Please enter a valid amount.")
            return
        
        new_amount = self.user.balance_actions.get_balance(user_id) - int(amount)
        
        self.user.balance_actions.update_balance(new_amount, account_number)
        self.user.transaction_actions.record_transaction(user_id, account_number, "N/A", "Withdraw", Utilities.parse_amount(int(amount)))
        QMessageBox.information(self.main_window, "Transaction Successful", "Transaction successful.")
        self.main_window.dashboard.withdrawPanel.clear_fields()
        self.dashboard_control.showDashboard()

class TransferControl:
    def __init__(self, window, dashboard_control):
        self.main_window = window
        self.session = self.main_window.session
        self.dashboard_control = dashboard_control
        self.transfer_menu = self.main_window.dashboard.transferPanel
        self.user = self.main_window.user_model
        self.transfer_menu.ui.btn_confirm.clicked.connect(self.transfer)
    
    def transfer(self):
        user_id = self.session.get_user_id()
        account_number = self.session.get_account_number()
        amount_text = self.transfer_menu.ui.amount_box.text()

        if Utilities.validate_amount(amount_text) == False:
            QMessageBox.critical(self.main_window, "Invalid amount format", "Please enter the amount using the format XXXX.XX, with no leading zeros on the amount.")
            return
        
        amount = amount_text.replace(".", "")
        sender_existing_balance = self.user.balance_actions.get_balance(user_id)

        if int(amount) > sender_existing_balance or int(amount) == 0:
            QMessageBox.critical(self.main_window, "Invalid amount", "Please enter a valid amount.")
            return
        
        recipient_acc_num = self.transfer_menu.ui.account_box.text()
        recipient_first_name = self.transfer_menu.ui.first_name_box.text()
        recipient_last_name = self.transfer_menu.ui.last_name_box.text()

        if (self.user.balance_actions.check_existing_recipient(recipient_acc_num, recipient_first_name, recipient_last_name) == False):
            QMessageBox.warning(self.main_window, "Transfer Failed", "Invalid account name/number.\nPlease make sure that you entered the correct details.")
            return

        if recipient_acc_num == self.session.get_account_number():
            QMessageBox.warning(self.main_window, "Invalid account number", "Please enter an account number that is not yours.")
            return
        
        recipient_amount = int(amount) + self.user.balance_actions.get_balance(recipient_acc_num)
        sender_amount = sender_existing_balance - int(amount)

        self.user.balance_actions.update_balance(recipient_amount, recipient_acc_num)
        self.user.balance_actions.update_balance(sender_amount, self.session.get_account_number())

        self.user.transaction_actions.record_transaction(user_id, account_number, recipient_acc_num, "Transfer - Sender", Utilities.parse_amount(int(amount)))
        self.user.transaction_actions.record_transaction(user_id, account_number, recipient_acc_num, "Transfer - Receiver", Utilities.parse_amount(int(amount)))

        QMessageBox.information(self.main_window, "Transaction Successful", "Transaction successful.")
        self.transfer_menu.clear_fields()
        self.dashboard_control.showDashboard()

class TransactionHistoryControl:
    def __init__(self, window, dashboard_control):
        self.main_window = window
        self.transaction_history = self.main_window.dashboard.transactionHistoryPanel
        self.dashboard_control = dashboard_control
        self.session = window.session
        self.user = self.main_window.user_model
        self.transaction_history.ui.filter_select.currentTextChanged.connect(self.transaction_history.toggle_checkboxes)
        self.transaction_history.ui.btn_filter.clicked.connect(self.filter_transactions)

    def filter_transactions(self):
        
        if self.transaction_history.ui.filter_select.currentText() == "None":
            result_set = self.user.transaction_actions.load_transactions(self.session.get_user_id(), self.session.get_account_number())
            self.transaction_history.populate_table(result_set)

        elif self.transaction_history.ui.filter_select.currentText() == "Transaction Type":
            if self.are_checkboxes_checked() == False:
                QMessageBox.warning(self.main_window, "Operation Failed", "Please check at least one of the boxes.")
                return

            query_string, params = self.generate_filter_by_type([])
            main_query = f"SELECT sender_acc_num, recipient_acc_num, transaction_type, amount, date, time FROM transaction_history WHERE {query_string}"
            result_set = self.user.transaction_actions.load_transactions_by_type(main_query, params)

            self.transaction_history.populate_table(result_set)

        elif self.transaction_history.ui.filter_select.currentText() == "Transaction Date":
            # get date from qlineedit obejects
            start_date = self.transaction_history.ui.date_from.date().toString("yyyy-MM-dd")
            end_date = self.transaction_history.ui.date_to.date().toString("yyyy-MM-dd")

            if self.is_range_valid(start_date, end_date) == False:
                QMessageBox.warning(self.main_window, "Operation Failed", "Please make sure that the date range is valid.")
                return

            
            result_set = self.user.transaction_actions.load_transactions(self.session.get_user_id(), self.session.get_account_number(), date_flag=True, start_date=start_date, end_date=end_date)
            self.transaction_history.populate_table(result_set)

        elif self.transaction_history.ui.filter_select.currentText() == "Transaction Type and Date":

            if self.are_checkboxes_checked() == False:
                QMessageBox.warning(self.main_window, "Operation Failed", "Please check at least one of the boxes.")
                return
            
            start_date = self.transaction_history.ui.date_from.date().toString("yyyy-MM-dd")
            end_date = self.transaction_history.ui.date_to.date().toString("yyyy-MM-dd")

            if self.is_range_valid(start_date, end_date) == False:
                QMessageBox.warning(self.main_window, "Operation Failed", "Please make sure that the date range is valid.")
                return

            query_string, params = self.generate_filter_by_type([])
            #print(query_string)
            main_query = f"SELECT sender_acc_num, recipient_acc_num, transaction_type, amount, date, time FROM transaction_history WHERE ({query_string}) AND (date BETWEEN '{start_date}' AND '{end_date}')"
            #print(main_query)
            result_set = self.user.transaction_actions.load_transactions_by_type(main_query, params)
            self.transaction_history.populate_table(result_set)

    def generate_filter_by_type(self, query_list):
        params = {}

        if self.transaction_history.ui.option_transfer_rec.isChecked():
            query_list.append(f"(transaction_type = 'Transfer - Receiver' AND recipient_acc_num = :recipient)")
            params["recipient"] = self.session.get_account_number()

        if self.transaction_history.ui.option_transfer_send.isChecked():
            query_list.append(f"(transaction_type = 'Transfer - Sender' AND sender_acc_num = :sender)")
            params["sender"] = self.session.get_account_number()

        if self.transaction_history.ui.option_deposit.isChecked():
            query_list.append(f"(transaction_type = 'Deposit' AND user_id = :dep_user_id)")
            params["dep_user_id"] = self.session.get_user_id()

        if self.transaction_history.ui.option_withdraw.isChecked():
            query_list.append(f"(transaction_type = 'Withdraw' AND user_id = :wd_user_id)")
            params["wd_user_id"] = self.session.get_user_id()
        
        query_string = " OR ".join(query_list)

        query_list.clear()
        print(query_string)

        return query_string, params
    

    def are_checkboxes_checked(self):
        checkbox_list = [
            self.transaction_history.ui.option_transfer_rec, 
            self.transaction_history.ui.option_transfer_send, 
            self.transaction_history.ui.option_withdraw,
            self.transaction_history.ui.option_deposit
        ]

        for item in checkbox_list:
            if item.isChecked():
                return True
            
        return False

    def is_range_valid(self, start_date, end_date):
        if start_date > end_date:
            return False
        return True

class AccountControl:
    def __init__(self, window, dashboard_control):
        self.main_window = window
        self.session = self.main_window.session
        self.dashboard_control = dashboard_control
        self.account_menu = self.main_window.dashboard.accountPanel
        self.user = self.main_window.user_model
        self.account_menu.ui.btn_cancel.clicked.connect(self.show_prompt)
        self.account_menu.ui.btn_save.clicked.connect(self.save_changes)

    def show_prompt(self):
        if self.check_unsaved_changes() == False:
            self.dashboard_control.showDashboard()
            return
        
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setText("There are unsaved changes. Proceed?")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)

        response = msg_box.exec()
        if response == QMessageBox.StandardButton.Yes:
            self.dashboard_control.showDashboard()

    def save_changes(self):
        if self.check_unsaved_changes() == False:
            return

        first_name = self.account_menu.ui.first_name_box.text().strip().title()
        last_name = self.account_menu.ui.last_name_box.text().title()
        username = self.account_menu.ui.username_box.text().strip()
        password = self.account_menu.ui.password_box.text().strip()
        confirm_password = self.account_menu.ui.confirm_password_box.text().strip()

        if self.validate_inputs(first_name, last_name, username, password, confirm_password) == False:
            return


        query_string = "UPDATE users SET "
        query_list = []
        params = {}

        if first_name != "" and first_name != self.session.get_first_name():
            #check via regex later
            query_list.append(f"first_name = :first_name")
            params["first_name"] = first_name

        if last_name != "" and last_name != self.session.get_last_name():
            query_list.append(f"last_name = :last_name")
            params["last_name"] = last_name

        if username != "" and username != self.session.get_username():
            query_list.append(f"username = :username")
            params["username"] = username
        
        if password != "" and password == confirm_password:
            query_list.append(f"hashed_password = :password")
            params["password"] = self.user.account_actions.hash_password(password, self.user.account_actions.get_salt(self.session.get_user_id()))

        i = 0
        for query in query_list:   
            query_string += query 
            if i < len(query_list) - 1:
                query_string +=  ", "
            i += 1
        
        query_string += f" WHERE user_id = {self.session.get_user_id()}"
        self.user.execute_query_via_dict(query_string, params)
        print(query_string)
        
        user_data = self.user.account_actions.get_user_data(user_id=self.session.get_user_id())

        QMessageBox.information(self.main_window, "Operation Successful", "Account details successfully updated.")

        self.account_menu.set_display_information(user_data[1], user_data[2], user_data[3], user_data[4])
        self.session.set_personal_information(first_name=user_data[2], last_name=user_data[3], username=user_data[4])
        self.account_menu.clear_fields()
    
    def check_unsaved_changes(self):
        box_list = [
            self.account_menu.ui.first_name_box,
            self.account_menu.ui.last_name_box,
            self.account_menu.ui.username_box,
            self.account_menu.ui.password_box,
            self.account_menu.ui.confirm_password_box,
        ]

        if box_list[0].text() != "" and box_list[0].text().title() != self.session.get_first_name():
            return True

        if box_list[1].text() != "" and box_list[1].text().title() != self.session.get_last_name():
            return True
        
        if box_list[2].text() != "" and box_list[2].text().title() != self.session.get_username():
            return True

        if box_list[3].text() != "" and box_list[3].text().title() != self.session.get_password():
            return True

        return False
    
    def validate_inputs(self, first_name, last_name, username, password, confirm_password):
        if first_name != "" and Utilities.validate_name(first_name) == False:
            QMessageBox.critical(self.main_window, "Invalid input", "Invalid first name. Please make sure you entered your name correctly.\nOnly letters, a single apostrophe, and hyphens are allowed.")
            return False
        
        if last_name != "" and Utilities.validate_name(last_name) == False:
            QMessageBox.critical(self.main_window, "Invalid input", "Invalid last name. Please make sure you entered your name correctly.\nOnly letters, a single apostrophe, and hyphens are allowed.")
            return False

        if username != "" and Utilities.validate_username(username) == False:
            QMessageBox.critical(self.main_window, "Invalid input", "Invalid username.\nPlease make sure that your username is 3-20 characters long, and must contain only letters, numbers, and apostrophes or periods.")
            return False

        if password != "" and Utilities.validate_password(password) == False:
            QMessageBox.critical(self.main_window, "Invalid input", "Invalid password. Please make sure that your password is at least 8 characters long,\n and must contain at least 1 digit, 1 uppercase and lowercase letter,\n and at least 1 non-alphanumeric character.")
            return False
        elif Utilities.validate_password(password) == True and password != confirm_password:
            QMessageBox.critical(self.main_window, "Invalid input", "Invalid password. Please make sure that your passwords match.")
            return False

        return True