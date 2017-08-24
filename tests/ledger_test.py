import unittest
import os
from moazna import ledger
from moazna.datastores import json_datastore


class TestLedger(unittest.TestCase):

    def setUp(self):
        self.sample_datastore = json_datastore.JsonDatastore()
        self.sample_ledger = ledger.Ledger(self.sample_datastore)

    def test_get_account_balance(self):
        self.sample_ledger.record_txn(
            123, 'mr payer', 'mr recipient', '2017-09-01'
        )
        self.sample_ledger.record_txn(
            23, 'mr recipient', 'mr payer', '2017-09-02'
        )
        payer_balance = self.sample_ledger.get_account_balance(
            'mr payer', '2017-09-02')
        recipient_balance = self.sample_ledger.get_account_balance(
            'mr recipient', '2017-09-02')
        self.assertEqual(payer_balance, -100)
        self.assertEqual(recipient_balance, 100)

    def test_record_txn(self):
        txns = self.sample_ledger.transactions
        accounts = self.sample_ledger.accounts
        self.assertEqual(len(txns), 0)
        self.assertEqual(len(accounts), 0)
        self.sample_ledger.record_txn(
            123, 'mr payer', 'mr recipient', '2017-09-01'
        )
        txns = self.sample_ledger.transactions
        accounts = self.sample_ledger.accounts
        self.assertEqual(len(txns), 1)
        self.assertEqual(len(accounts), 2)
        payer_balance = self.sample_ledger.get_account_balance(
            'mr payer', '2017-09-01')
        recipient_balance = self.sample_ledger.get_account_balance(
            'mr recipient', '2017-09-01')
        self.assertEqual(payer_balance, -123)
        self.assertEqual(recipient_balance, 123)

    def test_import_txns(self):
        ledger_file_path = os.path.abspath('./sample_ledger.csv')
        txns = self.sample_ledger.transactions
        accounts = self.sample_ledger.accounts
        self.assertEqual(len(txns), 0)
        self.assertEqual(len(accounts), 0)
        txns = self.sample_ledger.import_txns(ledger_file_path)
        accounts = self.sample_ledger.accounts
        self.assertEqual(len(txns), 5)
        self.assertEqual(len(accounts), 5)
