from abc import ABCMeta, abstractproperty, abstractmethod

class Endpoint:
    __metaclass__ = ABCMeta

    @abstractproperty
    def address(self): pass

    @abstractproperty
    def abilities(self): pass

    @abstractmethod
    def getAcceptableData(self): pass

    @abstractmethod
    def localSearch(self): pass

    @abstractmethod
    def propagatingSearch(self): pass

    @abstractmethod
    def dataProcess(self): pass




class LocalEndpoint(Endpoint):

    address = ""
    abilities = []
    algorithms = []
    remoteEndpoints = []
    assemblies = []


class RemoteEndpoint(Endpoint):

    address = ""
    abilities = []