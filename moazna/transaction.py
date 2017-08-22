"""Transaction Class."""

import uuid

class Transaction(object):
    def __init__(self, datastore, amount, payerName, recipientName, date):
        self._datastore = datastore
        self.id = uuid.uuid4()
        self.amount = amount
        self.payerName = payerName
        self.recipientName = recipientName
        self.data = date

    def save(self):
        if self.id in self._datastore:
            self._datastore.update(dict(self))
        else:
            self._datastore.create(dict(self))

    @classmethod
    def list_by_name(cls, datastore, name):
        return datastore.filter(name)
