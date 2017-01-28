from abc import ABCMeta, abstractproperty, abstractmethod
import algorithm
import backend
import data
import endpoint
import protocol

class Ability:
    __metaclass__ = ABCMeta

    @abstractproperty
    def container(self): pass

    @abstractproperty
    def inputs(self): pass

    @abstractproperty
    def outputs(self): pass

    @abstractproperty
    def state(self): pass

    @abstractmethod
    def process(self): pass


class LocalAbility(Ability):

    container = None

    inputs = 0
    outputs = 0

class RemoteAbility(Ability):

    container = None

    inputs = 0
    outputs = 0
