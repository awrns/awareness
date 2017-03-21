from abc import ABCMeta, abstractproperty, abstractmethod
import misc
import affinity as i_affinity
import algorithm as i_algorithm
import backend as i_backend
import operator as i_operator
import protocol as i_protocol


class Item:
    __metaclass__ = ABCMeta

    @abstractproperty
    def input(self):
        raise NotImplementedError()

    @abstractproperty
    def output(self):
        raise NotImplementedError()


    @abstractmethod
    def datumize(self):
        raise NotImplementedError()

    @abstractmethod
    def similarity(self, other):
        raise NotImplementedError()



class Set:
    __metaclass__ = ABCMeta


    @abstractproperty
    def items(self):
        raise NotImplementedError()


    @abstractmethod
    def datumize(self):
        raise NotImplementedError()


    def similarity(self, other):
        pass



class Assembly:
    __metaclass__ = ABCMeta

    pass
