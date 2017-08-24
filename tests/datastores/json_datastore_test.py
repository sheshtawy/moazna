import unittest
import copy
from moazna.datastores import json_datastore


class JsonDatastoreTests(unittest.TestCase):

    def setUp(self):
        self.sampleDatastore = json_datastore.JsonDatastore()
        self.sampleDatastore.add_entity('test_entity')
        self.instance = {
            'id_attr': 'super_unique',
            'attr': 'value',
            'another_attr': 'yet another value',
            'a_number': 3
        }

    def test_create(self):
        self.assertEqual(self.sampleDatastore.count('test_entity'), 0)

        db_instance = self.sampleDatastore.create('test_entity', self.instance)

        self.assertEqual(self.sampleDatastore.count('test_entity'), 1)

    def test_retrieve(self):
        self.sampleDatastore.create('test_entity', self.instance)

        db_instance = self.sampleDatastore.retrieve(
            'test_entity', 'id_attr', 'super_unique')
        self.assertDictEqual(db_instance, self.instance)

    def test_update(self):
        self.sampleDatastore.create('test_entity', self.instance)

        updated_instance = copy.deepcopy(self.instance)
        updated_instance['attr'] = 'modified'
        updated_instance['new_attr'] = [1, 3, 5]
        db_instance = self.sampleDatastore.update(
            'test_entity', updated_instance, 'id_attr')
        print db_instance
        self.assertDictEqual(db_instance, updated_instance, str(db_instance))

    def test_delete(self):
        self.sampleDatastore.create('test_entity', self.instance)
        self.assertEqual(self.sampleDatastore.count('test_entity'), 1)

        self.sampleDatastore.delete(
            'test_entity', 'id_attr', self.instance['id_attr'])
        self.assertEqual(self.sampleDatastore.count('test_entity'), 0)
