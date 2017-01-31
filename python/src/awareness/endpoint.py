from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import protocol as i_protocol


class Endpoint:
    __metaclass__ = ABCMeta

    @abstractproperty
    def address(self):
        pass

    @abstractproperty
    def abilities(self):
        pass
    

    @abstractmethod
    def localSearch(self):
        pass

    @abstractmethod
    def propagatingSearch(self):
        pass


    @abstractmethod
    def getAcceptableData(self):
        pass

    @abstractmethod
    def processData(self):
        pass


class LocalEndpoint(Endpoint):

    algorithm = None
    backend = None
    protocol = None

    address = ""
    abilities = []
    assemblies = []


    remoteEndpoints = []


    def __init__(
        self,
        address,
        algorithm = i_algorithm.DefaultAlgorithm,
        backend = i_backend.NativeBackend,
        protocol = i_protocol.Protocol0,
        abilities = [],
        assemblies = [],
        remoteEndpoints = []
    ):

        self.address = address
        self.algorithm = algorithm()
        self.backend = backend()
        self.protocol = protocol()
        self.abilities = abilities
        self.assemblies = assemblies
        self.remoteEndpoints = remoteEndpoints


    def localSearch(self, callback, set, time):
        self.backend.async(self.algorithm.localSearch(callback, set, time))


    def propagatingSearch(self, callback, set, depth, time):
        self.backend.async(self.algorithm.localSearch(callback, set, depth, time))


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


