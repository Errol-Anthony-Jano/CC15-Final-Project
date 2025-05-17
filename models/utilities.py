import re

class Utilities:
    @staticmethod
    def validate_name(name):
        if re.fullmatch("^[a-zA-Z]+(?:[ \-'][a-zA-Z]+)*$", name) is None:
            return False
        return True
    
    @staticmethod
    def validate_username(username):
        if re.fullmatch("^[a-zA-Z0-9._-]{3,20}$", username) is None:
            return False
        return True

    @staticmethod
    def validate_password(password):
        if re.fullmatch("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,}$", password) is None:
            return False
        return True

    @staticmethod
    def validate_amount(amount):
        if re.fullmatch(r'^[0-9]+\.[0-9]{2}$', amount) is None:
            return False
        return True

    @staticmethod 
    def parse_amount(amount):
        if amount < 10:
            return (f"0.0{amount}")
        if amount >= 10 and amount < 100:
            return (f"0.{amount}")
        return str(amount)[:-2] + '.' + str(amount)[-2:]