from abc import ABCMeta, abstractproperty, abstractmethod
import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import protocol as i_protocol


class Endpoint:
    __metaclass__ = ABCMeta

    @abstractproperty
    def host(self):
        raise NotImplementedError()

    @abstractproperty
    def port(self):
        raise NotImplementedError()

    @abstractproperty
    def abilities(self):
        raise NotImplementedError()

    @abstractproperty
    def backend(self):
        raise NotImplementedError()

    @abstractproperty
    def protocol(self):
        raise NotImplementedError()


    @abstractmethod
    def localSearch(self, callback, set, time):
        raise NotImplementedError()

    @abstractmethod
    def propagatingSearch(self, callback, set, depth, time):
        raise NotImplementedError()


    @abstractmethod
    def getAcceptableData(self):
        raise NotImplementedError()

    @abstractmethod
    def processData(self, index, input):
        raise NotImplementedError()


class LocalEndpoint(Endpoint):

    host = ""
    port = -1
    abilities = []
    backend = None
    protocol = None

    algorithm = None
    assemblies = []
    remoteEndpoints = []


    def __init__(self, host="", port=1024, abilities = [], backend = None, protocol = None, algorithm = None, assemblies = [], remoteEndpoints = []):
        self.host = host
        self.port = port
        self.abilities = abilities
        self.backend = backend() if backend else i_backend.NativeBackend()
        self.protocol = protocol() if protocol else i_protocol.Protocol0()
        self.algorithm = algorithm() if algorithm else i_algorithm.DefaultAlgorithm()
        self.assemblies = assemblies
        self.remoteEndpoints = remoteEndpoints

        self.backend.async(self.protocol.provide, (self.backend.listen(host=host,port=port), self))


    def localSearch(self, set, time): self.algorithm.localSearch(self.remoteEndpoints, set, time)


    def propagatingSearch(self, set, depth, time): self.algorithm.propagatingSearch(self.remoteEndpoints, set, depth, time)


    def getAcceptableData(self):
        acceptableData = []

        for eachAbility in self.abilities:
            eachAcceptableData = (eachAbility.inputs, eachAbility.outputs)
            acceptableData.append(eachAcceptableData)

        return acceptableData


    def processData(self, index, input):
        return self.abilities[index].run(input)


class RemoteEndpoint(Endpoint):

    host = ""
    port = -1
    abilities = []
    backend = None
    protocol = None

    connection = None

    def __init__(self, host, port, abilities = [], backend = None, protocol = None):
        self.host = host
        self.port = port
        self.abilities = abilities
        self.backend = backend() if backend else i_backend.NativeBackend()
        self.protocol = protocol() if protocol else i_protocol.Protocol0()
        if self.abilities == []:
            self.connect()
            self.retrieveAbilities()
            self.disconnect()

    def connect(self):
        self.connection = self.backend.connect(self.host, port=self.port)

    def disconnect(self):
        self.connection.close()
        self.connection = None

    def retrieveAbilities(self):
        acceptableData = self.protocol.getAcceptableData(self.connection)
        for i in range(len(acceptableData)):
            eachAcceptableData = acceptableData[i]
            newAbility = i_ability.RemoteAbility(self, i, eachAcceptableData[0], eachAcceptableData[1])

            self.abilities.append(newAbility)


    def localSearch(self, callback, set, time):
        self.protocol.localSearch(self.connection, set, time)


    def propagatingSearch(self, callback, set, depth, time):
        self.protocol.propagatingSearch(self.connection, set, depth, time)


    def getAcceptableData(self):
        acceptableData = []

        for eachAbility in self.abilities:
            eachAcceptableData = (eachAbility.inputs, eachAbility.outputs)
            acceptableData.append(eachAcceptableData)

        return acceptableData


    def processData(self, index, input):
        return self.abilities[index].run(input)
