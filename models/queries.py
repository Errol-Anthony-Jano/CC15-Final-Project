import textwrap
class Queries:

    @staticmethod
    def insert_new_user_query():
        return textwrap.dedent("""
            INSERT INTO users (
                account_number,
                first_name,
                last_name,
                username,
                hashed_password,
                pass_salt
            ) VALUES (?, ?, ?, ?, ?, ?)
            """).strip()
    
    @staticmethod
    def insert_new_transaction_query():
        return textwrap.dedent(
            """
            INSERT INTO transaction_history (
                user_id,
                sender_acc_num,
                recipient_acc_num,
                transaction_type,
                amount,
                date,
                time
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        ).strip()

    @staticmethod
    def check_existing_recipient_query():
        return textwrap.dedent(
            """
            SELECT *
            FROM users
            WHERE account_number = ?
            AND first_name = ?
            AND last_name = ?
            """
        ).strip()

    @staticmethod
    def select_transactions_query():
        return textwrap.dedent(
            """
            SELECT 
                sender_acc_num,
                recipient_acc_num,
                transaction_type,
                amount,
                date,
                time
            FROM transaction_history
            WHERE
            (
                (
                    user_id = ? AND transaction_type IN ('Withdraw', 'Deposit')
                ) OR (
                    recipient_acc_num = ? AND transaction_type = 'Transfer - Receiver'
                ) OR (
                    sender_acc_num = ? AND transaction_type = 'Transfer - Sender'
                )
            )
            """
        ).strip()
    
    @staticmethod
    def order_and_limit_constraint():
        return textwrap.dedent(
            """
            ORDER BY 
                date DESC,
                time DESC
            LIMIT 5
            """
        ).strip()