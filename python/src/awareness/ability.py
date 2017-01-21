from abc import ABCMeta, abstractproperty, abstractmethod
import endpoint
import data
import backend
import protocol

class Ability:
    __metaclass__ = ABCMeta

    @abstractproperty
    def container(self): pass

    @abstractproperty
    def inputs(self): pass

    @abstractproperty
    def outputs(self): pass


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
