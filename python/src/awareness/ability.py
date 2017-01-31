from abc import ABCMeta, abstractproperty, abstractmethod
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import endpoint as i_endpoint
import protocol as i_protocol

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
