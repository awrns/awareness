from abc import ABCMeta, abstractproperty, abstractmethod
import misc
import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import protocol as i_protocol


class Operator:
    __metaclass__ = ABCMeta

    @abstractproperty
    def host(self):
        raise NotImplementedError()

    @abstractproperty
    def port(self):
        raise NotImplementedError()

    @abstractproperty
    def abilities(self):  # List of LocalAbility.
        raise NotImplementedError()

    @abstractproperty
    def backend(self):  # Any derivation from i_backend.Backend.
        raise NotImplementedError()

    @abstractproperty
    def protocol(self):  # Any derivation from i_protocol.Protocol.
        raise NotImplementedError()


    @abstractmethod
    def capabilities(self):
        raise NotImplementedError()

    @abstractmethod
    def search(self, propagationLimit, trainingSet, testSet, progressCallback=None):
        raise NotImplementedError()

    @abstractmethod
    def process(self, index, inputSet, progressCallback=None):
        raise NotImplementedError()


class LocalOperator(Operator):

    host = ""
    port = -1
    abilities = []
    backend = None
    protocol = None

    algorithm = None
    assemblies = []  # List of i_assembly.Assembly.
    remoteOperators = []  # List of RemoteOperator.


    def __init__(self,
                 host="",
                 port=1600,
                 abilities = [],
                 backend = None,
                 protocol = None,
                 algorithm = None,
                 assemblies = [],
                 remoteOperators = []):

        self.host = host
        self.port = port
        self.abilities = abilities
        self.backend = backend() if backend else i_backend.NativeBackend()  # If not passed in, use default
        self.protocol = protocol() if protocol else i_protocol.Protocol0()
        self.algorithm = algorithm() if algorithm else i_algorithm.DefaultAlgorithm()
        self.assemblies = assemblies
        self.remoteOperators = remoteOperators

        # Kickoff the server process. Get a listener from self.backend, and give it to self.protocol to use.
        self.backend.processingAsync(self.protocol.provide, (self.backend.listen(host=host,port=port), self))


    def search(self, propagationLimit, trainingSet, testSet, progressCallback=None):
        # Search both the LocalAbilities here and the RemoteAbilities that the RemoteOperators make available.
        self.algorithm.search(self.abilities, self.remoteOperators, trainingSet, testSet, progressCallback)

    def process(self, index, inputSet, progressCallback=None):
        # Hand inputSet to our indexed LocalAbility.
        return self.abilities[index].run(inputSet, progressCallback)

    def capabilities(self):
        # Building a list of tuples.
        capabilities = []

        for eachAbility in self.abilities:
            capabilities.append(eachAbility.profile)  # eachAbility.profile is a 2-tuple

        return capabilities


class RemoteOperator(Operator):

    host = ""
    port = -1
    abilities = []
    backend = None
    protocol = None

    connection = None

    def __init__(self,
                 host,
                 port,
                 abilities = [],
                 backend = None,
                 protocol = None):

        self.host = host
        self.port = port
        self.abilities = abilities
        self.backend = backend() if backend else i_backend.NativeBackend()  # Set to default if None.
        self.protocol = protocol() if protocol else i_protocol.Protocol0()

        # Do a quick routine to get the Ability details.
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


    def search(self, propagationLimit, trainingSet, testSet, progressCallback=None):
        self.algorithm.search(self.connection, trainingSet, testSet, progressCallback)

    def process(self, index, inputSet, progressCallback=None):
        return self.abilities[index].run(self.connection, inputSet, progressCallback)


    def capabilities(self):
        capabilities = []

        for eachAbility in self.abilities:
            capabilities.append(eachAbility.profile)

        return capabilities
