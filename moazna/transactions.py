"""Transaction Class."""

import uuid


class Transaction(object):
    def __init__(self, amount, payerName, recipientName, date):
        self.id = self._generate_id()
        self.amount = amount
        self.payer_name = payerName
        self.recipient_name = recipientName
        self.date = date

    def __iter__(self):
        KEYS = ['id', 'amount', 'payer_name', 'recipient_name', 'date']

        for key in self.__dict__:
            if key in KEYS:
                yield key, self.__getattribute__(key)

    def __str__(self):
        return '{0}, {1}, {2}, {3}, {4}'.format(self.id, self.amount, self.payer_name, self.recipient_name, self.date)

    def __repr__(self):
        return '{0}(id={1}, amount={2}, payer_name={3}, recipient_name={4}, data{5})'.format(
            self.__class__.__name__, self.id, self.amount, self.payer_name, self.recipient_name, self.date
        )

    def _generate_id(self):
        return str(uuid.uuid4())

    @classmethod
    def from_dict(cls, data):
        instance = cls(data['amount'], data['payer_name'],
                       data['recipient_name'], data['date'])
        if 'id' in data:
            instance.id = data['id']
        return instance


class TransactionRepository(object):
    """A class to help persist transactions in a datastore/database."""

    def __init__(self, datastore):
        self._datastore = datastore
        self.__entity = 'transactions'
        self.__id_attr = 'id'
        self._datastore.add_entity(self.__entity)

    def create(self, amount, payerName, recipientName, date):
        """Create a new transaction and save to the datastore.
        
        :param amount: transaction amount
        :param payerName: payer account name
        :param recipientName: recipient account name
        :param date: date of transaction
        :returns: Transaction instance of the newly created transaction
        """
        instance = Transaction(amount, payerName, recipientName, date)
        return Transaction.from_dict(self._datastore.create(self.__entity, dict(instance)))

    def list(self):
        """List all saved transactions."""

        records = self._datastore.filter(self.__entity, self.__id_attr)
        txns = []
        for record in records:
            txn = Transaction.from_dict(record)
            txns.append(txn)

        return txns

    def get_by_id(self, txnId):
        """Retrieve transaction by id.
        
        :param txnId: transaction id
        :returns: Transaction instance if found or None otherwise
        """
        
        record = self._datastore.retrieve(self.__entity, self.__id_attr, txnId)
        if record is not None:
            return Transaction.from_dict(record)

    def list_by_name(self, name):
        """List all transactions containing a name as either payer or recipient.
        
        :param name: account name
        :returns: List of Transaction instances if found or empty list otherwise
        """
        txns = []
        txns.extend(self.list_by_payer(name))
        txns.extend(self.list_by_recipient(name))
        return txns

    def list_by_payer(self, payerName):
        """List all transactions by a payer.
        
        :param payerName: payer account name
        :returns: List of Transaction instances if found or empty list otherwise
        """
        
        records = self._datastore.filter(
            self.__entity, 'payer_name', payerName)
        txns = []
        for record in records:
            txn = Transaction.from_dict(record)
            txns.append(txn)

        return txns

    def list_by_recipient(self, recipientName):
        """List all transactions by a recipient.
        
        :param recipientName: payer account name
        :returns: List of Transaction instances if found or empty list otherwise
        """
        
        records = self._datastore.filter(
            self.__entity, 'recipient_name', recipientName)
        txns = []
        for record in records:
            txn = Transaction.from_dict(record)
            txns.append(txn)

        return txns

    def update(self, instance):
        """Update a transaction.

        :param instance: Transaction instance with the updated value(s)
        :returns: Transaction instance after it's saved in the datastore 
        """
        record = self._datastore.update(
            self.__entity, dict(instance), self.__id_attr)
        return Transaction.from_dict(record)

    def delete(self, instance):
        """Delete a transaction.

        :param instance: Transaction instance with the updated value(s)
        """
        
        self._datastore.delete(
            self.__entity, self.__id_attr, dict(instance)[self.__id_attr])
