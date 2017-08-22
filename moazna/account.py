"""Account class."""

import collections
import datetime


class Account(object):
    def __init__(self, datastore, name, balance=0.0):
        self._datastore = datastore
        self.name = name
        self._balance = balance
        self._balance_history = collections.OrderedDict()

    def debit(self, amount):
        self._balance += amount

    def credit(self, amount):
        self._balance -= amount

    def get_balance(self, date):
        if date in self._balance_history:
            return self._balance_history[date]

    def save(self):
        if self._datastore.retrieve(self.name) is None:
            self._datastore.create(dict(self))
        else:
            self._datastore.update(dict(self))

    @property
    def balance(self):
        return self._balance

    @classmethod
    def getByName(cls, datastore, name):
        record = datastore.retrieve(name)
        if record is not None:
            instance = cls(datastore, record['name'], record['balance'])
            return instance
        
        return None
    