"""Account class."""

import collections
import datetime


class Account(object):

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def debit(self, amount):
        self.balance += amount

    def credit(self, amount):
        self.balance -= amount

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['balance'])


class AccountRepository(object):
    
    def __init__(self, datastore):
        self._datastore = datastore
    
    def create(self, name, balance=0.0):
        pass
    
    def list(self):
        pass
    
    def getByName(self, name):
        pass

    def update(self, instance):
        pass

    def delete(self, instance):
        pass

    def getBalance(self, name, date):
        pass

    def _updateBalanceHistory(self, accountName, balance):
        pass
