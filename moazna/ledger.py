import csv

from moazna.accounts import AccountRepository
from moazna.transactions import TransactionRepository


class Ledger:
    def __init__(self, datastore):
        '''
        Repository classes used to interact with the datastore/database following
        the DAO model. Datastore connection is injected here as a dependency for 
        all repository classes. This is meant to decouple the ledger logic from 
        the data persistance logic.
        
        NOTE: I built a JSON Datastore to facilitate testing. But using this design
              Any database/datastore could be used.
        '''
        self._datastore = datastore
        self.account_repository = AccountRepository(self._datastore)
        self.txn_repository = TransactionRepository(self._datastore)

    def record_txn(self, amount, payerName, recipientName, date):
        """Record a new txn.

        Behavior:
            - This function should lookup the payer and recipient accounts in 
            the database first. If any of them is not found, new accounts will be
            created since it's a new account joining the system

            - Payer account will be debited and recipient account will be credited based
            on the assumption that the accounts are of the type 'Personal' according to
            this document https://en.wikipedia.org/wiki/Debits_and_credits

        :param amount: transaction amount
        :param payerName: payer account name
        :param recipientName: recipient account name
        :param date: date of transaction
        :returns: Transaction instance of the newly recored transaction
        """

        payer = self.account_repository.get_by_name(payerName)
        if payer is None:
            payer = self.account_repository.create(payerName)

        recipient = self.account_repository.get_by_name(recipientName)
        if recipient is None:
            recipient = self.account_repository.create(recipientName)

        txn = self.txn_repository.create(
            amount, payer.name, recipient.name, date)

        payer.credit(amount)
        self.account_repository.update(payer)
        self.account_repository.update_balance_history(
            payer.name, payer.balance, date)

        recipient.debit(amount)
        self.account_repository.update(recipient)
        self.account_repository.update_balance_history(
            recipient.name, recipient.balance, date)

        return txn

    def import_txns(self, filePath):
        """Import transactions from a text file.

        :param filePath: absolute path to a csv ledger file
        :returns: list of all transactions recored currently on the ledger
        """

        with open(filePath) as csv_file:
            csv_reader = csv.DictReader(
                csv_file, fieldnames=['date', 'payer', 'recipient', 'amount'])
            for row in csv_reader:
                self.record_txn(float(row['amount']), row['payer'],
                                row['recipient'], row['date'])

        return self.transactions

    def get_account_balance(self, accountName, date):
        """Browse account's balance history by date.
        :param accountName: name of the account
        :param date: date of the desired balance entry
        :returns: balance at the chosen date or None if no entries found
        """
        return self.account_repository.get_balance(accountName, date)

    @property
    def accounts(self):
        return self.account_repository.list()

    @property
    def transactions(self):
        return self.txn_repository.list()
