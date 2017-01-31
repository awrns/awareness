from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import endpoint as i_endpoint


class DataUnit:
    __metaclass__ = ABCMeta

    @abstractproperty
    def struct(self):
        pass

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def deserialize(self):
        pass

    @abstractmethod
    def serialize(self):
        pass

