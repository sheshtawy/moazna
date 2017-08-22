"""Transaction Class."""

import uuid

class Transaction(object):
    def __init__(self, amount, payerName, recipientName, date):
        self.id = uuid.uuid4()
        self.amount = amount
        self.payer_name = payerName
        self.recipient_name = recipientName
        self.data = date


class TransactionRepository(object):
    
    def __init__(self, datastore):
        self._datastore = datastore

    def create(self, amount, payerName, recipientName, date):
        pass
    
    def list(self):
        pass
    
    def getById(self, id):
        pass
    
    def getByName(self, name):
        pass
    
    def getByPayer(self, payerName):
        pass

    def getByRecipient(self, recipientName):
        pass

    def update(self, instance):
        pass

    def delete(self, instance):
        pass
