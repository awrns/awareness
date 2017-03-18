from abc import ABCMeta, abstractproperty, abstractmethod
import misc
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import operator as i_operator
import protocol as i_protocol


class Affinity:
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
    def run(self, inputSet, progressFrequency=0, progressCallback=None):
        raise NotImplementedError()


class LocalAffinity(Affinity):

    operator = None
    index = 0

    profile = []


    def __init__(self,
                 operator,
                 index,
                 profile):

        self.operator = operator
        self.index = index
        self.profile = profile


class RemoteAffinity(Affinity):

    operator = None
    index = 0

    profile = []


    def __init__(self,
                 operator,
                 index,
                 profile):

        self.operator = operator
        self.index = index
        self.profile = profile


    def run(self, connection, inputSet, progressFrequency=0, progressCallback=None):

        output = self.operator.protocol.process(connection, self.index, inputSet, progressFrequency, progressCallback)

        return output

