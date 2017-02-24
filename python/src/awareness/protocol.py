from abc import ABCMeta, abstractproperty, abstractmethod

import struct

import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import endpoint as i_endpoint


class Protocol:
    __metaclass__ = ABCMeta

    @abstractmethod
    def localSearch(self, endpoint, set, time):
        raise NotImplementedError()

    @abstractmethod
    def propagatingSearch(self, endpoint, set, depth, time):
        raise NotImplementedError()

    @abstractmethod
    def getAcceptableData(self, endpoint):
        raise NotImplementedError()

    @abstractmethod
    def processData(self, endpoint, index, input):
        raise NotImplementedError()


    @abstractmethod
    def provide(self, listener, endpoint):
        raise NotImplementedError()


class Protocol0(Protocol):


    pduStruct = lambda datalen: struct.Struct("!5cQ" + datalen + "s")


    VERSION_BYTE =          0xA0

    LOCAL_SEARCH =          0x00
    PROPAGATING_SEARCH =    0x01

    GET_ACCEPTABLE_DATA =   0x10
    PROCESS_DATA =          0x11

    ITEM_RESPONSE =         0x20
    SET_RESPONSE =          0x21
    ASSEMBLY_RESPONSE =     0x22

    INCOMPATIBLE_ERROR =    0x30
    UNIT_ERROR =            0x31
    DATA_ERROR =            0x32


    localSearchStruct =         struct.Struct("!")
    propagatingSearchStruct =   struct.Struct("!")

    getAcceptableDataStruct =   struct.Struct("!")
    processDataStruct =         lambda paramnum: struct.Struct("!B" + paramnum + "B")

    itemResponseStruct =        lambda paramnum: struct.Struct("!" + paramnum + "B")
    setResponseStruct =         lambda itemnum, paramnum: struct.Struct("!Q" + itemnum*paramnum + "B")
    assemblyResponseStruct =    struct.Struct("!")


    def localSearch(self, endpoint, set, time):
        pass

    def propagatingSearch(self, endpoint, set, depth, time):
        pass

    def getAcceptableData(self, endpoint):
        pass

    def processData(self, endpoint, index, input):
        
        connection = endpoint.backend.connect(endpoint.host, endpoint.port)



        connection.close()

    def provide(self, listener, endpoint):
        pass


