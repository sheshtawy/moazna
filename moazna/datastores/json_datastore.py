"""In-memory JSON datastore."""

import datastore


class JsonDatastore(datastore.Datastore):
    def __init__(self):
        self._data = {}

    def create(self, entity, instance):
        if not self.__has_entity(entity):
            self.add_entity(entity)
        
        self._data[entity].append(instance)
        return len(self._data[entity])

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
            elem = None

            elem = self.retrieve(entity, id_attr, instance[id_attr])

            if elem is not None:
                for key, value in instance:
                    if elem[key] != value:
                        elem[key] = value
            
            entity_list.append(elem)
            return elem

    def delete(self):
        pass

    def add_entity(self, entity):
        if not self.__has_entity(entity):
            self._data[entity] = []


    def __has_entity(self, entity):
        return entity in self._data
