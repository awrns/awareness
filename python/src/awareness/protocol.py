from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import endpoint as i_endpoint


class Protocol:
    __metaclass__ = ABCMeta

    @abstractmethod
    def localSearch(self, connection, callback, set, time):
        pass

    @abstractmethod
    def propagatingSearch(self, connection, callback, set, time):
        pass

    @abstractmethod
    def getAcceptableData(self, connection):
        pass

    @abstractmethod
    def processData(self, connection, index, input):
        pass

class Protocol0(Protocol):

    pass