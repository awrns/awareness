from abc import ABCMeta, abstractproperty, abstractmethod
import ability
import algorithm
import backend
import data
import endpoint

class DataUnit:
    __metaclass__ = ABCMeta

    @abstractproperty
    def struct(self): pass

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def serialize(self): pass