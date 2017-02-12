from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import endpoint as i_endpoint


class Protocol:
    __metaclass__ = ABCMeta

    @abstractmethod
    def enactLocalSearch(self, connection, callback, set, time):
        pass

    @abstractmethod
    def enactPropagatingSearch(self, connection, callback, set, time):
        pass

    @abstractmethod
    def enactGetAcceptableData(self, connection):
        pass

    @abstractmethod
    def enactProcessData(self, connection, index, input):
        pass


    @abstractmethod
    def provide(self, endpoint, connection):
        pass


class Protocol0(Protocol):

    pass