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

    @abstractproperty
    def backend(self):
        pass

    @abstractproperty
    def protocol(self):
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

    address = ""
    abilities = []

    backend = None
    protocol = None


    algorithm = None
    assemblies = []
    remoteEndpoints = []


    def __init__(
        self,
        address,
        abilities = [],
        backend = None,
        protocol = None,
        algorithm = None,
        assemblies = [],
        remoteEndpoints = []
    ):

        self.address = address
        self.abilities = abilities
        self.backend = backend() if backend else i_backend.NativeBackend()
        self.protocol = protocol() if protocol else i_protocol.Protocol0()
        self.algorithm = algorithm() if algorithm else i_algorithm.DefaultAlgorithm()
        self.assemblies = assemblies
        self.remoteEndpoints = remoteEndpoints


    def localSearch(self, callback, set, time):
        self.backend.async(self.algorithm.localSearch(self, callback, set, time))


    def propagatingSearch(self, callback, set, depth, time):
        self.backend.async(self.algorithm.propagatingSearch(self, callback, set, depth, time))


    def getAcceptableData(self):
        acceptableData = []

        for eachAbility in self.abilities:
            eachAcceptableData = (eachAbility.inputs, eachAbility.outputs)
            acceptableData.append(eachAcceptableData)

        return acceptableData


    def processData(self, index, input):
        return self.abilities[index].run(input)


class RemoteEndpoint(Endpoint):

    address = ""
    abilities = []

    backend = None
    protocol = None

    def __init__(
        self,
        address,
        abilities = [],
        backend = None,
        protocol = None,
    ):
        self.address = address
        self.abilities = abilities
        self.backend = backend() if backend else i_backend.NativeBackend()
        self.protocol = protocol() if protocol else i_protocol.Protocol0()

        if self.abilities == []:
            self.retrieveAbilities()


    def retrieveAbilities(self):
        connection = self.backend.connect(self.address)
        acceptableData = self.protocol.getAcceptableData(connection)
        for i in range(len(acceptableData)):
            eachAcceptableData = acceptableData[i]
            newAbility = i_ability.RemoteAbility(self, i, eachAcceptableData[0], eachAcceptableData[1])

            self.abilities.append(newAbility)


    def localSearch(self, callback, set, time):
        connection = self.backend.connect(self.address)
        self.protocol.localSearch(connection, callback, set, time)


    def propagatingSearch(self, callback, set, depth, time):
        connection = self.backend.connect(self.address)
        self.protocol.propagatingSearch(connection, callback, set, depth, time)


    def getAcceptableData(self):
        acceptableData = []

        for eachAbility in self.abilities:
            eachAcceptableData = (eachAbility.inputs, eachAbility.outputs)
            acceptableData.append(eachAcceptableData)

        return acceptableData


    def processData(self, index, input):
        return self.abilities[index].run(input)
