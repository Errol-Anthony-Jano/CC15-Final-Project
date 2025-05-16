from PyQt6.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from PyQt6.QtCore import QDate
from resources.ui_files.transaction_history import Ui_Form

class UI_TransactionHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def setup_table(self):
        header = self.ui.tbl_transaction_history.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.tbl_transaction_history.setHorizontalHeaderLabels(["Initiated by", "Receiver", "Type", "Amount", "Date", "Time"])

        date = QDate.currentDate()
        self.ui.date_to.setDate(date)
        self.ui.date_from.setDate(date)
        self.ui.date_to.setCalendarPopup(True)
        self.ui.date_from.setCalendarPopup(True)

    def populate_table(self, result_set):
        self.ui.tbl_transaction_history.setRowCount(len(result_set))
        self.ui.tbl_transaction_history.setColumnCount(6)

        for row_idx, row_data in (enumerate(result_set)):
            for col_idx, value in (enumerate(row_data)):
                item = QTableWidgetItem(str(value))
                self.ui.tbl_transaction_history.setItem(row_idx, col_idx, item)

    def toggle_checkboxes(self, text):
        if text == "None":
            self.ui.option_transfer_rec.setEnabled(False)
            self.ui.option_transfer_send.setEnabled(False)
            self.ui.option_withdraw.setEnabled(False)
            self.ui.option_deposit.setEnabled(False)
            self.ui.date_from.setEnabled(False)
            self.ui.date_to.setEnabled(False)
        elif text == "Transaction Type and Date":
            self.ui.option_transfer_rec.setEnabled(True)
            self.ui.option_transfer_send.setEnabled(True)
            self.ui.option_withdraw.setEnabled(True)
            self.ui.option_deposit.setEnabled(True)
            self.ui.date_from.setEnabled(True)
            self.ui.date_to.setEnabled(True)
        elif text == "Transaction Type":
            self.ui.date_from.setEnabled(False)
            self.ui.date_to.setEnabled(False)
            self.ui.option_transfer_rec.setEnabled(True)
            self.ui.option_transfer_send.setEnabled(True)
            self.ui.option_withdraw.setEnabled(True)
            self.ui.option_deposit.setEnabled(True)
        else:
            self.ui.option_transfer_rec.setEnabled(False)
            self.ui.option_transfer_send.setEnabled(False)
            self.ui.option_withdraw.setEnabled(False)
            self.ui.option_deposit.setEnabled(False)
        
            self.ui.date_from.setEnabled(True)
            self.ui.date_to.setEnabled(True)