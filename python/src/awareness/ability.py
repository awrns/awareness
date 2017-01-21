from abc import ABCMeta, abstractproperty, abstractmethod

class Ability:
    __metaclass__ = ABCMeta

    @abstractproperty
    def endpoint(self): pass

    @abstractproperty
    def inputs(self): pass

    @abstractproperty
    def outputs(self): pass


    @abstractmethod
    def process(self): pass


class LocalAbility(Ability):

    endpoint = None

    inputs = 0
    outputs = 0

class RemoteAbility(Ability):

    endpoint = None

    inputs = 0
    outputs = 0
