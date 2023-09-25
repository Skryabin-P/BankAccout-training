from datetime import datetime


class TimeZone:
    def __init__(self, name, offset):
        self.name = name
        self.offset = offset


class ConfirmationCode:
    """
    Class which contains the account number, transaction code (D, W, etc),
    datetime (UTC format), date time (in user's timezone), the transaction ID
    """


class Account:
    _interest_rate = 0.5
    _transaction_id = 0

    def __init__(self, account_number: int, first_name: str, last_name: str, timezone, balance: float = 0):
        self._account_number = account_number
        self._first_name = first_name
        self._last_name = last_name
        self.timezone = timezone
        self._balance = balance
        self._confirmation_code = None

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if isinstance(first_name, str):
            self._first_name = first_name
        else:
            raise ValueError('First name must be a string')

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if isinstance(last_name, str):
            self._last_name = last_name
        else:

            raise ValueError('Last name must be a string')

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def balance(self):
        return self._balance

    def _generate_transaction(self, transaction_type):
        self._transaction_id += 1
        self._transaction_time_utc = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        self._confirmation_code = '{}-{}-{}-{}'.format(transaction_type, self._account_number,
                                                       self._transaction_time_utc, self._transaction_id)

    def deposit(self, amount: float):
        if amount > 0:
            self._generate_transaction('D')
            self._balance += amount
            print(f'Deposit accepted, your balance {self.balance} '
                  f'\nconfirmation code is {self.confirmation_code}')
        else:
            self._generate_transaction('X')
            print('Deposit amount must be a positive number,'
                  f' transaction declined with code {self.confirmation_code}')

    @property
    def confirmation_code(self):
        return self._confirmation_code


if __name__ == "__main__":
    test_account = Account(1231, 'test', 'TEST', +3, 100)
    print(test_account.balance)
    test_account.deposit(1000)
    test_account.deposit(-10)
