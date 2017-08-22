"""DataStore class for general data persistance operations."""

import abc

class DataStore(object):
    """DataStore Abstract class.

    The class uses composition to make it easy
    to change the data persistance layer without disrupting
    the application logic
    """

    @abc.abstractmethod
    def create(self, instance):
        """Create an new instance.

        :param instance: The instance to be created
        """
        raise Exception('Must implelment create method')

    @abc.abstractmethod
    def retrieve(self, instance_id):
        """Retrieve an existing instance.

        :param instance_id: The id of the instance to be retrieved
        """
        raise Exception('Must implelment retrieve method')

    @abc.abstractmethod
    def update(self, instance):
        """Update and existing instance.

        :param instance: The instance to be updated
        """
        raise Exception('Must implelment update method')

    @abc.abstractmethod
    def delete(self, instance_id):
        """Delete an existing instance.

        :param instance_id: The id of the instance to be deleted
        """
        raise Exception('Must implelment delete method')
