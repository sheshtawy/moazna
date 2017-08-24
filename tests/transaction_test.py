import unittest

from moazna.transactions import Transaction, TransactionRepository
from moazna.accounts import Account, AccountRepository
from moazna.datastores import json_datastore


class TestTransaction(unittest.TestCase):

    def test_from_dict(self):
        txn_dict = {
            'amount': 12,
            'payer_name': 'mr payer',
            'recipient_name': 'mr recipient',
            'date': '2017-05-12'
        }

        sample_txn = Transaction.from_dict(txn_dict)
        self.assertIsInstance(sample_txn, Transaction)
        self.assertTrue(hasattr(sample_txn, 'id'))
        txn_dict['id'] = sample_txn.id
        self.assertDictEqual(dict(sample_txn), txn_dict)


class TestTransactionRepository(unittest.TestCase):

    def setUp(self):
        self.sample_datastore = json_datastore.JsonDatastore()
        self.txn_repository = TransactionRepository(self.sample_datastore)
        self.account_repository = AccountRepository(self.sample_datastore)

        self.payer = self.account_repository.create('mr payer')
        self.recipient = self.account_repository.create('mr recipient')

    def test_create(self):
        sample_txn = self.txn_repository.create(
            123, 'mr payer', 'mr recipient', '2017-09-01'
        )

        self.assertIsInstance(sample_txn, Transaction)
        self.assertEqual(sample_txn.amount, 123)
        self.assertEqual(sample_txn.payer_name, 'mr payer')
        self.assertEqual(sample_txn.recipient_name, 'mr recipient')
        self.assertEqual(sample_txn.date, '2017-09-01')
        self.assertIsNotNone(sample_txn.id)

    def test_list(self):
        result = self.txn_repository.list()
        self.assertEqual(len(result), 0)
        self.txn_repository.create(
            123, 'mr payer', 'mr recipient', '2017-09-01')
        self.txn_repository.create(
            123, 'mr payer', 'mr recipient', '2017-09-01')
        result = self.txn_repository.list()
        self.assertEqual(len(result), 2)

    def test_get_by_id(self):
        sample_txn = Transaction(123, 'mr payer', 'mr recipient', '2017-09-01')
        result = self.txn_repository.get_by_id(sample_txn.id)
        self.assertIsNone(result)
        txn_instance = self.txn_repository.create(
            sample_txn.amount,
            sample_txn.payer_name,
            sample_txn.recipient_name,
            sample_txn.date
        )
        result = self.txn_repository.get_by_id(txn_instance.id)
        self.assertIsInstance(result, Transaction)
        self.assertEqual(result.amount, 123)
        self.assertEqual(result.payer_name, 'mr payer')
        self.assertEqual(result.recipient_name, 'mr recipient')
        self.assertEqual(result.date, '2017-09-01')
        self.assertEqual(result.id, txn_instance.id)

    def test_list_by_payer(self):
        self.txn_repository.create(
            123, 'mr payer', 'mr recipient', '2017-09-01')
        self.txn_repository.create(
            123, 'mr payer', 'mr recipient', '2017-09-01')
        self.txn_repository.create(
            123, 'another payer', 'mr recipient', '2017-09-01')
        result = self.txn_repository.list_by_payer('mr payer')
        self.assertEqual(len(result), 2)

    def test_list_by_recipient(self):
        self.txn_repository.create(
            123, 'mr payer', 'mr recipient', '2017-09-01')
        self.txn_repository.create(
            123, 'mr payer', 'mr recipient', '2017-09-01')
        self.txn_repository.create(
            123, 'another payer', 'another recipient', '2017-09-01')
        result = self.txn_repository.list_by_recipient('mr recipient')
        self.assertEqual(len(result), 2)

    def test_list_by_name(self):
        self.txn_repository.create(123, 'john', 'mr recipient', '2017-09-01')
        self.txn_repository.create(123, 'mr payer', 'john', '2017-09-01')
        self.txn_repository.create(123, 'new payer', 'john', '2017-09-01')
        self.txn_repository.create(
            123, 'another payer', 'another recipient', '2017-09-01')
        result = self.txn_repository.list_by_name('john')
        self.assertEqual(len(result), 3)

    def test_update(self):
        sample_txn = self.txn_repository.create(
            123, 'mr payer', 'mr recipient', '2017-09-01')
        sample_txn.recipient_name = 'new recipient'
        updated_txn = self.txn_repository.update(sample_txn)
        self.assertEqual(updated_txn.recipient_name, 'new recipient')

    def test_delete(self):
        sample_txn = self.txn_repository.create(
            123, 'mr payer', 'mr recipient', '2017-09-01')
        self.txn_repository.create(
            123, 'mr payer', 'mr recipient', '2017-09-01')
        result = self.txn_repository.list()
        self.assertEqual(len(result), 2)
        self.txn_repository.delete(sample_txn)
        result = self.txn_repository.list()
        self.assertEqual(len(result), 1)
