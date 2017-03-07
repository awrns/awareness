from abc import ABCMeta, abstractproperty, abstractmethod
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import endpoint as i_endpoint
import protocol as i_protocol


class Ability:
    __metaclass__ = ABCMeta

    @abstractproperty
    def endpoint(self):
        raise NotImplementedError()

    @abstractproperty
    def index(self):
        raise NotImplementedError()


    @abstractproperty
    def profile(self):
        raise NotImplementedError()


    @abstractmethod
    def run(self, inputSet):
        raise NotImplementedError()


class LocalAbility(Ability):

    endpoint = None
    index = 0

    profile = []


    def __init__(self, endpoint, index, profile):
        self.endpoint = endpoint
        self.index = index
        self.profile = profile


class RemoteAbility(Ability):

    endpoint = None
    index = 0

    profile = []


    def __init__(self, endpoint, index, profile):
        self.endpoint = endpoint
        self.index = index
        self.profile = profile


    def run(self, inputSet):

        output = self.endpoint.protocol.process(self.endpoint, self.index, inputSet)

        return output

