from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import backend as i_backend
import data as i_data
import endpoint as i_endpoint
import protocol as i_protocol


class Algorithm:
    __metaclass__ = ABCMeta

    @abstractmethod
    def localSearch(self, endpoint, set, time):
        raise NotImplementedError()

    @abstractmethod
    def propagatingSearch(self, endpoint, set, depth, time):
        raise NotImplementedError()


class DefaultAlgorithm(Algorithm):

    def localSearch(self, endpoint, set, time):
        pass

    def propagatingSearch(self, endpoint, set, depth, time):
        pass
