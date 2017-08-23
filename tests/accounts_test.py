import unittest
from datetime import datetime
from moazna.accounts import Account, AccountRepository
from moazna.datastores import json_datastore


class TestAccount(unittest.TestCase):

    def setUp(self):
        self.sample_account = Account('sample', 0.0)

    def test_debit(self):
        self.assertEqual(self.sample_account.balance, 0.0)
        self.sample_account.debit(100.0)
        self.assertEqual(self.sample_account.balance, 100.0)

    def test_credit(self):
        self.assertEqual(self.sample_account.balance, 0.0)
        self.sample_account.credit(100.0)
        self.assertEqual(self.sample_account.balance, -100.0)

    def test_from_dict(self):
        sample_dict = {
            'name': 'mr sample',
            'balance': 123
        }
        sample_account = Account.from_dict(sample_dict)
        self.assertEqual(sample_account.name, sample_dict['name'])
        self.assertEqual(sample_account.balance, sample_dict['balance'])
        self.assertIsNotNone(sample_account.balance_history)
        self.assertEqual(sample_account.balance_history, [
                         {'balance': 123, 'date': datetime.now().strftime('%Y-%m-%d')}])

    def test_update_history(self):
        self.assertEqual(len(self.sample_account.balance_history), 1)
        self.sample_account.update_history(100.0, '2017-01-15')
        self.assertEqual(self.sample_account.get_balance('2017-01-15'), 100.0)
        self.assertEqual(len(self.sample_account.balance_history), 2)

    def test_get_balance_without_date(self):
        self.assertEqual(self.sample_account.get_balance(),
                         self.sample_account.balance)

    def test_get_balance_with_date(self):
        self.assertEqual(self.sample_account.get_balance(
            datetime.now().strftime('%Y-%m-%d')), self.sample_account.balance)


class TestAccountRepository(unittest.TestCase):

    def setUp(self):
        self.sample_datastore = json_datastore.JsonDatastore()
        self.account_repository = AccountRepository(self.sample_datastore)

    def test_create(self):
        sample_account = self.account_repository.create('mr sample')
        self.assertIsInstance(sample_account, Account)
        self.assertEqual(sample_account.name, 'mr sample')
        self.assertEqual(sample_account.balance, 0.0)
        self.assertEqual(len(sample_account.balance_history), 1)

    def test_list(self):
        result = self.account_repository.list()
        self.assertEqual(len(result), 0)
        self.account_repository.create('mr sample')
        self.account_repository.create('mr sample yo')
        result = self.account_repository.list()
        self.assertEqual(len(result), 2)

    def test_get_by_name(self):
        result = self.account_repository.get_by_name('mr sample')
        self.assertIsNone(result)
        self.account_repository.create('mr sample')
        result = self.account_repository.get_by_name('mr sample')
        self.assertIsInstance(result, Account)
        self.assertEqual(result.name, 'mr sample')
        self.assertEqual(result.balance, 0.0)
        self.assertEqual(len(result.balance_history), 1)

    def test_update(self):
        sample_account = self.account_repository.create('mr sample')
        sample_account.balance = 123
        updated_account = self.account_repository.update(sample_account)
        self.assertIsInstance(updated_account, Account)
        self.assertEqual(updated_account.balance, 123)

    def test_get_balance(self):
        sample_account = self.account_repository.create('mr sample')
        balance = self.account_repository.get_balance(
            'mr sample', datetime.now().strftime('%Y-%m-%d'))
        self.assertEqual(balance, sample_account.get_balance(
            datetime.now().strftime('%Y-%m-%d')))

    def test_update_balance_history(self):
        sample_account = self.account_repository.create('mr sample')
        self.assertEqual(len(sample_account.balance_history), 1)
        self.account_repository.update_balance_history(
            sample_account.name, 1234, '2017-04-12'
        )
        result = self.account_repository.get_by_name('mr sample')
        self.assertEqual(len(result.balance_history), 2)
        self.assertEqual(result.get_balance('2017-04-12'), 1234)
