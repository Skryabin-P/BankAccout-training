from datetime import datetime, timedelta
from itertools import count
import numbers


class TimeZone:
    def __init__(self, name: str, offset_hours: int, offset_minutes: int):
        if name is None or len(name.strip()) == 0:
            raise ValueError('Timezone name cannot be empty')
        self._name = name.strip()
        if not isinstance(offset_hours, int):
            raise ValueError('Hour offset must be an integer')
        if not isinstance(offset_minutes, int):
            raise ValueError('Minute offset must be an integer')
        if offset_minutes > 59 or offset_minutes < -59:
            raise ValueError('Minutes offset must be between -59 and 59 inclusive')
        offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        if offset < timedelta(hours=-12, minutes=0) or offset > timedelta(hours=12, minutes=0):
            raise ValueError('Offset must be between -12:00 and +12:00')

        self._offset_hours = offset_hours
        self._offset_minutes = offset_minutes
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    @property
    def name(self):
        return self._name


class ConfirmationCode:
    """
    Class which contains the account number, transaction code (D, W, etc),
    datetime (UTC format), date time (in user's timezone), the transaction ID
    """
    def __init__(self, code: str, timezone: TimeZone = None):
        code_parts = code.split('-')
        if len(code_parts) != 4:
            raise ValueError('Invalid confirmation code')
        self._code_parts = code_parts
        if timezone is None:
            timezone = TimeZone('UTC', 0, 0)
        if not isinstance(timezone, TimeZone):
            raise ValueError('Time zone must be a valid TimeZone object!')
        self.timezone = timezone

    @property
    def transaction_code(self):
        return self._code_parts[0]

    @property
    def account_number(self):
        return self._code_parts[1]

    @property
    def transaction_time(self):
        transaction_time = self.transaction_time_utc + self.timezone.offset
        transaction_time_formatted = transaction_time.strftime(f'%Y-%m-%d %H:%M:%S({self.timezone.name})')
        return transaction_time_formatted

    @property
    def transaction_time_utc(self):
        parsed_transaction_time = self._code_parts[2]
        transaction_datetime = datetime.strptime(parsed_transaction_time, '%Y%m%d%H%M%S')
        return transaction_datetime

    @property
    def transaction_id(self):
        return self._code_parts[3]


class Account:
    _interest_rate = 0.5  # percent
    _transaction_id = count(1)

    def __init__(self, account_number: int, first_name: str, last_name: str,
                 timezone: TimeZone = None, balance: float = 0):
        self.account_number = account_number
        self.first_name = first_name
        self.last_name = last_name
        if timezone is None:
            timezone = TimeZone('UTC', 0, 0)
        self.timezone = timezone
        self._balance = float(balance)
        self._confirmation_code = None

    @property
    def account_number(self):
        return self._account_number

    @account_number.setter
    def account_number(self, account_number: int):
        if not isinstance(account_number, int):
            raise ValueError('Account number must be an integer!')
        self._account_number = account_number

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str):
        self.validate_set_name('_first_name', first_name, 'First name')

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str):
        self.validate_set_name('_last_name', last_name, 'Last name')

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        if not isinstance(value, TimeZone):
            raise ValueError('Time zone must be a valid TimeZone object!')
        self._timezone = value

    @classmethod
    def get_interest_rate(cls):
        return cls._interest_rate

    @classmethod
    def set_interest_rate(cls, value):
        if not isinstance(value, numbers.Real):
            raise ValueError('Interest rate must be a Real number')
        if value < 0:
            raise ValueError('Interest rate must be greater or equal 0')
        cls._interest_rate = value

    @property
    def balance(self):
        return self._balance

    @property
    def confirmation_code(self):
        return self._confirmation_code

    def validate_set_name(self, property_name: str, value: str, property_title: str):
        if not isinstance(value, str):
            raise ValueError(f'{property_title} must be a string')
        if value is None or len(value.strip()) == 0:
            raise ValueError(f'{property_title} cannot be empty')
        setattr(self, property_name, value)

    def _generate_transaction(self, transaction_type):
        self.new_transaction_id = next(Account._transaction_id)
        self._transaction_time_utc = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        self._confirmation_code = '{}-{}-{}-{}'.format(transaction_type, self.account_number,
                                                       self._transaction_time_utc, self.new_transaction_id)

    def deposit(self, amount: float):
        if not isinstance(amount, numbers.Real):
            raise ValueError('Deposit must be a Real number')
        if amount > 0:
            self._generate_transaction('D')
            self._balance += amount
            print(f'Deposit accepted, your balance {self.balance}$\n'
                  f'Confirmation code is {self.confirmation_code}')
        else:
            self._generate_transaction('X')
            print('Deposit amount must be a positive number, \n'
                  f'Transaction declined with code {self.confirmation_code}')
        return self.confirmation_code

    def withdraw(self, amount: float):
        if not isinstance(amount, numbers.Real):
            raise ValueError('Withdraw must be a Real number')
        if amount <= 0:
            raise ValueError('Withdraw must be greater than 0')
        if self.balance - amount >= 0:
            self._generate_transaction('W')
            self._balance -= amount
            print(f'Withdrawal processed, your balance now {self.balance}$ \n'
                  f'Confirmation code is {self.confirmation_code}')
        else:
            self._generate_transaction('X')
            print(f'You have insufficient funds to withdraw {amount}$,'
                  f'your current balance {self.balance}$ \n'
                  f'Transaction declined with code {self.confirmation_code}')
        return self.confirmation_code

    def pay_interest(self):
        interest = self.balance*Account.get_interest_rate()
        self._balance += interest
        self._generate_transaction('I')
        return self.confirmation_code


if __name__ == "__main__":
    mytz = TimeZone('MSK', 1, 15)
    test_account = Account(1231, 'Test', 'TEST', mytz, 100)
    test_account2 = Account(12312, 'Test2', 'TEST2', mytz, 100)
    print(test_account.balance)
    test_account.deposit(1000)
    test_account2.withdraw(50)
    test_account.withdraw(900)
    print(test_account2.pay_interest())
    code = ConfirmationCode('X-1231-20230926054249-3', mytz)
    print(code.transaction_time)
    print(code.transaction_time_utc)
