"""DataStore class for general data persistance operations."""

import abc


class Datastore:
    """DataStore Abstract class.

    The class uses composition to make it easy
    to change the data persistance layer without disrupting
    the application logic
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(self, entity, **kwargs):
        """Create an new instance.

        :param entity: entity collection name
        :param instance: The instance to be created
        :returns: python dict representing the created resource
        """
        pass

    @abc.abstractmethod
    def retrieve(self, entity, instance_id):
        """Retrieve an existing instance.

        :param entity: entity collection name
        :param instance_: The id of the instance to be retrieved
        :returns: python dict representing the retrieved resource
        """
        pass

    @abc.abstractmethod
    def update(self, entity, instance):
        """Update and existing instance.

        :param entity: entity collection name
        :param instance: The instance to be updated
        :returns: python dict representing the updated object
        """
        pass

    @abc.abstractmethod
    def delete(self, entity, instance_id):
        """Delete an existing instance.

        :param entity: entity collection name
        :param instance_id: The id of the instance to be deleted
        """
        pass

    @abc.abstractmethod
    def filter(self, entity, key, values):
        """Filter entity collection by values.

        :param entity: entity collection name
        :param key: The key to use for filtering the collection
        :param values: List of values to filter with
        """
