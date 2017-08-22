from moazna.accounts import Account
from moazna.accounts import AccountRepository
import csv
# from moazna.transactions import Transaction
from moazna.transactions import TransactionRepository

class Ledger:
    def __init__(self, datastore):
        self._datastore = datastore
        self.account_repository = AccountRepository(self._datastore)
        self.txn_repository = TransactionRepository(self._datastore)

    def record_txn(self, amount, payerName, recipientName, date):
        """Record a new txn."""

        payer = self.account_repository.getByName(payerName)
        if payer is None:
            payer = self.account_repository.create(payerName)

        recipient = self.account_repository.getByName(recipientName)
        if recipient is None:
            recipient = self.account_repository.create(recipientName)

        txn = self.txn_repository.create(amount, payer.name, recipient.name, date)

        payer.balance -= amount
        self.account_repository.update(payer)

        recipient.balance -= amount
        self.account_repository.update(recipient)

        return txn

    # def list_txns(self, accountName, startDate, endDate):
    #     return self.txn_repository.list(accountName)

    def import_txns(self, filePath):
        """Import transactions from a text file."""

        with open(filePath) as csv_file:
            csv_reader = csv.DictReader(csv_file, fieldnames=['date', 'payer', 'recipient', 'amount'])
            for row in csv_reader:
                self.record_txn(row['amount'], row['payer'], row['recipient'], row['date'])
    
    def get_account_balance(self, accountName, date):
        return self.account_repository.getBalance(accountName, date)
    
    @property
    def accounts(self):
        return self.account_repository.list()
    
    @property
    def transactions(self):
        return self.txn_repository.list()
