from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import endpoint as i_endpoint
import protocol as i_protocol


class Item:
    __metaclass__ = ABCMeta

    @abstractproperty
    def input(self):
        raise NotImplementedError()

    @abstractproperty
    def output(self):
        raise NotImplementedError()


    def similarity(self, other):
        pass


class Set:
    __metaclass__ = ABCMeta

    @abstractproperty
    def items(self):
        raise NotImplementedError()


    def similarity(self):
        pass

class Assembly:
    __metaclass__ = ABCMeta

    pass
