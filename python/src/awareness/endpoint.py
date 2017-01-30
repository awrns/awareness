from abc import ABCMeta, abstractproperty, abstractmethod
import ability
import algorithm
import backend
import data
import protocol


class Endpoint:
    __metaclass__ = ABCMeta

    @abstractproperty
    def address(self): pass

    @abstractproperty
    def abilities(self): pass
    

    @abstractmethod
    def localSearch(self): pass

    @abstractmethod
    def propagatingSearch(self): pass


    @abstractmethod
    def getAcceptableData(self): pass

    @abstractmethod
    def processData(self): pass


class LocalEndpoint(Endpoint):

    address = ""
    abilities = []
    assemblies = []

    algorithms = []


    remoteEndpoints = []


    def __init__(self, address, abilities = [], assemblies = [], algorithms = [], remoteEndpoints = []):
        self.address = address
        self.abilities = abilities
        self.assemblies = assemblies
        self.algorithms = algorithms
        self.remoteEndpoints = remoteEndpoints


    def localSearch(self, callback, set, time):
        search = algorithm.LocalSearch(callback, self.abilities, set, time)
        self.algorithms.append(search)


    def propagatingSearch(self, callback, set, depth, time):
        search = algorithm.PropagatingSearch(callback, self.abilities, set, depth, time)
        self.algorithms.append(search)


    def getAcceptableData(self):
        acceptableData = []

        for eachAbility in self.abilities:
            acceptableData.append(eachAbility.getAcceptableData())

        return acceptableData


    def processData(self, index, input):
        return self.abilities[index].processData(input)


class RemoteEndpoint(Endpoint):

    address = ""
    abilities = []

    def __init__(self, address, abilities = []):
        self.address = address
        self.abilities = abilities


