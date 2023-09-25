class TimeZone:
    def __init__(self, name, offset):
        self.name = name
        self.offset = offset


class Account:
    def __init__(self, account_number: int, first_name: str, last_name: str, timezone, balance: float = 0):
        self.account_number = account_number
        self._first_name = first_name
        self._last_name = last_name
        self.timezone = timezone
        self._balance = balance

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


if __name__ == "__main__":
    test_acc = Account(123123, 'Pavel', 'TEST', -7, 100)
    test_acc.last_name = 'Skryabin'
    print(test_acc.last_name)
