from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import backend as i_backend
import data as i_data
import endpoint as i_endpoint
import protocol as i_protocol


class Algorithm:
    __metaclass__ = ABCMeta

    @abstractmethod
    def localSearch(self, abilities, set, time):
        pass

    @abstractmethod
    def propagatingSearch(self, abilities, set, depth, time):
        pass


class DefaultAlgorithm(Algorithm):

    def localSearch(self, abilities, callback, set, time):
        pass

    def propagatingSearch(self, abilities, set, depth, time):
        pass
