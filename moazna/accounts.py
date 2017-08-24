"""Account classes."""
from datetime import datetime

DEFAULT_BALANCE = 0.0


class Account(object):
    """A class to perform the account's different logical operations."""

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        # balance history is private to be only modified by the internal functions
        self._balance_history = []
        self.update_history(self.balance, datetime.now().strftime('%Y-%m-%d'))

    def __iter__(self):
        KEYS = ['name', 'balance', '_balance_history']

        for key in self.__dict__:
            if key in KEYS:
                new_key = key
                if(key.startswith('_')):
                    new_key = key[1:]
                yield new_key, self.__getattribute__(key)

    def __str__(self):
        return 'name: {0}, balance: {1}, balance_history: {2}'.format(self.name, self.balance, self.balance_history)

    def __repr__(self):
        return '{0}(name={1}, balance={2})'.format(self.__class__.__name__, self.name, self.balance)

    def debit(self, amount):
        """Increase the account's balance.
        
        The account is assumed to be of type 'Personal' according to 
        this document https://en.wikipedia.org/wiki/Debits_and_credits
        """
        self.balance += amount

    def credit(self, amount):
        """Decrease the account's balance.
        
        The account is assumed to be of type 'Personal' according to 
        this document https://en.wikipedia.org/wiki/Debits_and_credits
        """

        self.balance -= amount

    @classmethod
    def from_dict(cls, data):
        """Create an Account instance from dict.
        
        :param data: Dict containing name, balance and possibly balance_history attrs
        :returns: Account instance
        """

        instance = cls(data['name'], data['balance'])
        if 'balance_history' in data:
            instance._balance_history = data['balance_history']
        return instance

    def update_history(self, balance, date):
        """Update account's balance history.
        
        NOTE: Date granuality is by day

        :param balance: balance amount
        :param date: date of recording the balance amount
        """
        try: 
            self._balance_history.remove({
                'date': date,
                'balance': balance
            })
        except ValueError:
            self._balance_history.append({
                'date': date,
                'balance': balance
            })
        else:
            self._balance_history.append({
                'date': date,
                'balance': balance
            })

    def get_balance(self, date=None):
        """Retrieve account's balance in a specific date.
        
        :param date: date of the desired balance entry
        :returns: balance amount if the entry exists, defaults to the current balance
        """
        if date is not None:
            for entry in self._balance_history:
                if entry['date'] == date:
                    return entry['balance']
        else:
            return self.balance

    @property
    def balance_history(self):
        return self._balance_history


class AccountRepository(object):
    """A class to help persist accounts in a datastore/database."""

    def __init__(self, datastore):
        self._datastore = datastore
        self.__entity = 'accounts'
        self.__id_attr = 'name'
        self._datastore.add_entity(self.__entity)

    def create(self, name, balance=DEFAULT_BALANCE):
        instance = Account(name, balance)

        return Account.from_dict(self._datastore.create(self.__entity, dict(instance)))

    def list(self):
        records = self._datastore.filter(self.__entity, self.__id_attr)
        accounts = []
        for record in records:
            account = Account.from_dict(record)
            accounts.append(account)
        return accounts

    def get_by_name(self, name):
        record = self._datastore.retrieve(self.__entity, 'name', name)
        if record is not None:
            return Account.from_dict(record)

    def update(self, instance):
        record = self._datastore.update(
            self.__entity, dict(instance), self.__id_attr)
        return Account.from_dict(record)

    def delete(self, instance):
        self._datastore.delete(
            self.__entity, self.__id_attr, instance[self.__id_attr])

    def get_balance(self, name, date):
        record = self.get_by_name(name)
        if record is not None:
            instance = Account.from_dict(dict(record))
            return instance.get_balance(date)

    def update_balance_history(self, accountName, balance, date):
        instance = self.get_by_name(accountName)
        instance.update_history(balance, date)
        self._datastore.update(self.__entity, dict(instance), self.__id_attr)
