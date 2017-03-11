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

    pduHeaderStruct = struct.Struct("!2cQ")

    searchIds = []
    processIds = []

    VERSION_BYTE =          0xA0

    NOTHING =               0x00
    INFO =                  0x01

    SET_SEARCH =            0x10
    GET_SEARCH =            0x11

    SET_DATA =              0x20
    GET_DATA =              0x21

    UNIT_ERROR =            0x30
    DATA_ERROR =            0x31

    INFO_RESPONSE =         0x40
    SEARCH_RESPONSE =       0x41
    DATA_RESPONSE =         0x42


    nothingPreStruct =              struct.Struct("!")
    infoPreStruct =                 struct.Struct("!")

    setSearchPreStruct =            struct.Struct("!")
    getSearchPreStruct =            struct.Struct("!")

    setDataPreStruct =              struct.Struct("!")
    getDataPreStruct =              struct.Struct("!")

    unitErrorPreStruct =            struct.Struct("!")
    dataErrorPreStruct =            struct.Struct("!")

    infoResponsePreStruct =         struct.Struct("!")
    searchResponsePreStruct =       struct.Struct("!")
    dataResponsePreStruct =         struct.Struct("!")


    nothingDatumStruct =            struct.Struct("!")
    infoDatumStruct =               struct.Struct("!")

    setSearchDatumStruct =          struct.Struct("!")
    getSearchDatumStruct =          struct.Struct("!")

    setDataDatumStruct =            struct.Struct("!")
    getDataDatumStruct =            struct.Struct("!")

    unitErrorDatumStruct =          struct.Struct("!")
    dataErrorDatumStruct =          struct.Struct("!")

    infoResponseDatumStruct =       struct.Struct("!")
    searchResponseDatumStruct =     struct.Struct("!")
    dataResponseDatumStruct =       struct.Struct("!")


    unitsPreStruct = {NOTHING: nothingPreStruct,
                      INFO: infoPreStruct,
                      SET_SEARCH: setSearchPreStruct,
                      GET_SEARCH: getSearchPreStruct,
                      SET_DATA: setDataPreStruct,
                      GET_DATA: getDataPreStruct,
                      UNIT_ERROR: unitErrorPreStruct,
                      DATA_ERROR: dataErrorPreStruct,
                      INFO_RESPONSE: infoResponsePreStruct,
                      DATA_RESPONSE: dataResponsePreStruct}


    unitsDatumStruct = {NOTHING: nothingDatumStruct,
                        INFO: infoDatumStruct,
                        SET_SEARCH: setSearchDatumStruct,
                        GET_SEARCH: getSearchDatumStruct,
                        SET_DATA: setDataDatumStruct,
                        GET_DATA: getDataDatumStruct,
                        UNIT_ERROR: unitErrorDatumStruct,
                        DATA_ERROR: dataErrorDatumStruct,
                        INFO_RESPONSE: infoResponseDatumStruct,
                        DATA_RESPONSE: dataResponseDatumStruct}


    def info(self, connection):
        
        pass

    def search(self, connection, propagationLimit, trainingSet, testSet, progressCallback=None):
        
        pass

    def process(self, connection, index, inputSet, progressCallback=None):

        pass


    def send(self, connection, unitType, params):

        tranData = self.units[unitType].pack(params)
        tranHeader = self.pduHeaderStruct.pack(self.VERSION_BYTE, unitType, len(tranData))

        connection.sendall(tranHeader)
        connection.sendall(tranData)


    def receive(self, connection):

        recvHeader =  connection.recv(self.pduHeaderStruct.size)
        version, unitType, dataLen = self.pduHeaderStruct.unpack(recvHeader)
        recvData = connection.recv(dataLen)

        if version != self.VERSION_BYTE:
            self.send(connection, self.UNIT_ERROR, ())
            return None

        try:
            unitPreStruct = self.unitsPreStruct[unitType]
            unitDatumStruct = self.unitsDatumStruct[unitType]
        except:
            self.send(connection, self.UNIT_ERROR, ())
            return None


        try:
            paramsPre = unitPreStruct.unpack(recvData[:unitPreStruct.size])
            paramsDatum = []
            for i in range(len(recvData[unitPreStruct.size:])):
                startDataIndex = unitPreStruct.size + (i*unitDatumStruct.size)
                dataRoi = recvData[startDataIndex:startDataIndex + unitDatumStruct.size]
                paramsDatum.append(unitDatumStruct.unpack(dataRoi))
        except:
            self.send(connection, self.DATA_ERROR, ())
            return None


        return unitType, paramsPre, paramsDatum



    def provide(self, listener, operator):

        def handle(connection):
            
            unitType, datums = self.receive(connection)

            if unitType == self.INFO:
                self.send(connection, self.INFO_RESPONSE, )

        
        connection, address = listener.accept()

        operator.backend.threadingAsync(handle, connection)


