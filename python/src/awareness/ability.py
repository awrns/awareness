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
    def inputNum(self):
        raise NotImplementedError()

    @abstractproperty
    def outputNum(self):
        raise NotImplementedError()


    @abstractmethod
    def run(self, inputSet):
        raise NotImplementedError()


class LocalAbility(Ability):

    endpoint = None
    index = 0

    inputNum = 0
    outputNum = 0

    def __init__(self, endpoint, index, inputNum, outputNum):
        self.endpoint = endpoint
        self.index = index
        self.inputNum = inputNum
        self.outputNum = outputNum


class RemoteAbility(Ability):

    endpoint = None
    index = 0

    inputNum = 0
    outputNum = 0

    def __init__(self, endpoint, index, inputNum, outputNum):
        self.endpoint = endpoint
        self.index = index
        self.inputNum = inputNum
        self.outputNum = outputNum

    def run(self, inputSet):

        output = self.endpoint.protocol.processData(self.endpoint, self.index, inputSet)

        return output

