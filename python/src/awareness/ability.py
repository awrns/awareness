from abc import ABCMeta, abstractproperty, abstractmethod
import misc
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import operator as i_operator
import protocol as i_protocol


class Ability:
    __metaclass__ = ABCMeta

    @abstractproperty
    def operator(self):
        raise NotImplementedError()

    @abstractproperty
    def index(self):
        raise NotImplementedError()


    @abstractproperty
    def profile(self):
        raise NotImplementedError()


    @abstractmethod
    def run(self, inputSet, progressCallback=None):
        raise NotImplementedError()


class LocalAbility(Ability):

    operator = None
    index = 0

    profile = []


    def __init__(self, operator, index, profile):
        self.operator = operator
        self.index = index
        self.profile = profile


class RemoteAbility(Ability):

    operator = None
    index = 0

    profile = []


    def __init__(self, operator, index, profile):
        self.operator = operator
        self.index = index
        self.profile = profile


    def run(self, inputSet, progressCallback=None):

        output = self.operator.protocol.process(self.index, inputSet, progressCallback)

        return output

