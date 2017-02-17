from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import endpoint as i_endpoint


class Protocol:
    __metaclass__ = ABCMeta

    @abstractmethod
    def localSearch(self, endpoint, set, time):
        raise NotImplementedError()

    @abstractmethod
    def propagatingSearch(self, endpoint, set, depth, time):
        raise NotImplementedError()

    @abstractmethod
    def getAcceptableData(self, endpoint):
        raise NotImplementedError()

    @abstractmethod
    def processData(self, endpoint, index, input):
        raise NotImplementedError()


    @abstractmethod
    def provide(self, listener, endpoint):
        raise NotImplementedError()


class Protocol0(Protocol):

    pass
