from moazna.account import Account
import csv
from moazna.transaction import Transaction

class Ledger:
    def __init__(self, datastore):
        self._datastore = datastore
    
    def record_txn(self, amount, payerName, recipientName, date):
        """Record a new txn."""
        payer = Account.getByName(self._datastore, payerName)
        if payer is None:
            payer = Account(self._datastore, payerName)
        
        recipient = Account.getByName(self._datastore, recipientName)
        if recipient is None:
            recipient = Account(self._datastore, recipientName)

        txn = Transaction(self._datastore, amount, payer.name, recipient.name, date)
        txn.save()

    def list_txns(self, accountName, startDate, endDate):
        return Transaction.list_by_name(self._datastore, accountName)

    def import_txns(self, filePath):
        """Import transactions from a text file."""

        with open(filePath) as csv_file:
            csv_reader = csv.DictReader(csv_file, fieldnames=['date', 'payer', 'recipient', 'amount'])
            for row in csv_reader:
                self.record_txn(row['amount'], row['payer'], row['recipient'], row['date'])
    
    @property
    def accounts(self):
        return self._datastore.list('accounts')
    
    @property
    def transactions(self):
        return self._datastore.list('transactions')
