"""Account class."""
from datetime import datetime

DEFAULT_BALANCE = 0.0


class Account(object):

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
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

    def debit(self, amount):
        self.balance += amount

    def credit(self, amount):
        self.balance -= amount

    @classmethod
    def from_dict(cls, data):
        instance = cls(data['name'], data['balance'])
        if 'balance_history' in data:
            instance._balance_history = data['balance_history']
        return instance

    def update_history(self, balance, date):
        self._balance_history.append({
            'date': date,
            'balance': balance
        })

    def get_balance(self, date=None):
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
        print record
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
