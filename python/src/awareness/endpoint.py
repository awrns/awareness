from abc import ABCMeta, abstractproperty, abstractmethod
import ability
import data
import backend
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


    remoteEndpoints = []


class RemoteEndpoint(Endpoint):

    address = ""
    abilities = []
