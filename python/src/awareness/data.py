from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import endpoint as i_endpoint
import protocol as i_protocol


class Item:

    @abstractproperty
    def inputs(self):
        pass

    @abstractproperty
    def outputs(self):
        pass


    @abstractmethod
    def similarity(self):
        pass


class Set:

    @abstractproperty
    def items(self):
        pass

    @abstractmethod
    def similarity(self):
        pass

class Assembly:
    pass