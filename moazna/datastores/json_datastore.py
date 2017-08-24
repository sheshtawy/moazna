"""In-memory JSON datastore."""

import datastore


class JsonDatastore(datastore.Datastore):
    def __init__(self):
        self._data = {}

    def create(self, entity, instance):
        if not self.__has_entity(entity):
            self.add_entity(entity)

        self._data[entity].append(instance)
        return self._data[entity][-1]

    def retrieve(self, entity, key, value):
        instance = None
        if self.__has_entity(entity):
            entity_list = self._data[entity]

            for elem in entity_list:
                if elem[key] == value:
                    return elem

    def update(self, entity, instance, id_attr):
        if self.__has_entity(entity):
            entity_list = self._data[entity]
            elem = self.retrieve(entity, id_attr, instance[id_attr])

            if elem is not None:
                entity_list.remove(elem)
                for key, value in instance.iteritems():
                    try:
                        if elem[key] != value:
                            elem[key] = value
                    except KeyError:
                        elem[key] = value

            entity_list.append(elem)

            return elem

    def delete(self, entity, id_attr, value):
        if self.__has_entity(entity):
            entity_list = self._data[entity]
            elem = self.retrieve(entity, id_attr, value)

            if elem is not None:
                entity_list.remove(elem)

    def add_entity(self, entity):
        if not self.__has_entity(entity):
            self._data[entity] = []

    def count(self, entity):
        if self.__has_entity(entity):
            return len(self._data[entity])

    def __has_entity(self, entity):
        return entity in self._data

    def filter(self, entity, key, values=[]):
        if self.__has_entity(entity):
            if key is None or len(values) == 0:
                return self._data[entity]

            return [elem for elem in self._data[entity] if elem[key] in values]
