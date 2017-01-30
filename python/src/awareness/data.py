from abc import ABCMeta, abstractproperty, abstractmethod
import ability
import algorithm
import backend
import endpoint
import protocol

class Item:

    @abstractproperty
    def inputs(self): pass

    @abstractproperty
    def outputs(self): pass


    @abstractmethod
    def similarity(self): pass

class Set:

    @abstractproperty
    def items(self): pass

    @abstractmethod
    def similarity(self): pass

class Assembly: pass