from abc import ABCMeta, abstractproperty, abstractmethod
import struct
import misc
import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import operator as i_operator


class Protocol:
    __metaclass__ = ABCMeta

    @abstractmethod
    def info(self, connection):
        raise NotImplementedError()

    @abstractmethod
    def search(self, connection, propagationLimit, trainingSet, testSet, progressCallback=None):
        raise NotImplementedError()

    @abstractmethod
    def process(self, index, inputSet, progressCallback=None):
        raise NotImplementedError()


    @abstractmethod
    def provide(self, listener, operator):
        raise NotImplementedError()



class Protocol0(Protocol):

    pduHeaderStruct = struct.Struct("!3cQ")

    VERSION_BYTE =          0xA0

    NOTHING =               0x00
    INFO =                  0x01

    SET_SEARCH =            0x10
    GET_SEARCH =            0x11

    SET_DATA =              0x20
    GET_DATA =              0x21

    UNIT_ERROR =            0x30
    DATA_ERROR =            0x31

    nothingStruct =         lambda dataLen: struct.Struct("!")
    infoStruct =            lambda dataLen: struct.Struct("!")

    setSearchStruct =       lambda dataLen: struct.Struct("!")
    getSearchStruct =       lambda dataLen: struct.Struct("!")

    setDataStruct =         lambda dataLen: struct.Struct("!")
    getDataStruct =         lambda dataLen: struct.Struct("!")

    unitErrorStruct =       lambda dataLen: struct.Struct("!")
    dataErrorStruct =       lambda dataLen: struct.Struct("!")

    units = {NOTHING: nothingStruct,
             INFO: infoStruct,
             SET_SEARCH: setSearchStruct,
             GET_SEARCH: getSearchStruct,
             SET_DATA: setDataStruct,
             GET_DATA: getDataStruct,
             UNIT_ERROR: unitErrorStruct,
             DATA_ERROR: dataErrorStruct}


    def info(self, connection):
        raise NotImplementedError()

    def search(self, connection, propagationLimit, trainingSet, testSet, progressCallback=None):
        raise NotImplementedError()

    def process(self, connection, index, inputSet, progressCallback=None):

        dataStruct = self.processDataStruct(len(input))
        data = dataStruct.pack(index, *input)

        header = self.pduHeaderStruct.pack(self.VERSION_BYTE, self.PROCESS_DATA, self.ITEM_RESPONSE, len(data))

        connection.sendall(header)
        connection.sendall(data)

        recvHeader = connection.recv(self.pduHeaderStruct.size)
        version, unitType, requestedType, dataLen = self.pduHeaderStruct.unpack(recvHeader)
        recvData = connection.recv(dataLen)

        itemStruct = self.itemResponseStruct(dataLen)
        output = itemStruct.unpack(recvData)

        return output


    def provide(self, listener, operator):

        def handle(connection):
            
            recvHeader = connection.recv(self.pduHeaderStruct.size)
            version, unitType, requestedType, dataLen = self.pduHeaderStruct.unpack(recvHeader)
            recvData = connection.recv(dataLen)

            if unitType == self.PROCESS_DATA:
                dataStruct = self.processDataStruct(dataLen - 1)
                index, input = dataStruct.unpack(recvData)
                input = list(input)

                output = operator.processData(index, input)

                itemStruct = self.itemResponseStruct(len(output))
                data = itemStruct.pack(*output)

                header = self.pduHeaderStruct.pack(self.VERSION_BYTE, self.ITEM_RESPONSE, self.NOTHING, len(data))
                
                connection.sendall(header)
                connection.sendall(data)

        
        connection, address = listener.accept()

        operator.backend.threadingAsync(handle, connection)


