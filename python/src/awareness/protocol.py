from abc import ABCMeta, abstractproperty, abstractmethod
import misc
import ability as i_ability
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import operator as i_operator


class Protocol:
    __metaclass__ = ABCMeta

    @abstractmethod
    def searchCapabilities(self, connection):
        raise NotImplementedError()

    @abstractmethod
    def processCapabilities(self, connection):
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



class Protocol0(Protocol, misc.Protocol0Constants):


    def searchCapabilities(self, connection):
        
        pass


    def processCapabilities(self, connection):
        
        self.send(connection, self.BLANK, self.PROCESS_CAPABILITIES, (), ())

        unitType, requestedType, params, datums = self.receive(connection)

        



    def search(self, connection, propagationLimit, trainingSet, testSet, progressCallback=None):
        
        pass

    def process(self, connection, index, inputSet, progressCallback=None):

        pass


    def send(self, connection, unitType, requestedType, params, datums):

        unitPreStruct = self.unitPreStructs[unitType]
        unitDatumStruct = self.unitDatumStructs[unitType]

        tranDatums = ''
        tranPre = unitPreStruct.pack(params)

        for datum in datums:
            tranDatums.append(unitDatumStruct.pack(datum))


        tranHeader = self.pduHeaderStruct.pack(self.VERSION_BYTE, unitType, requestedType, len(tranDatums)+len(tranPre))

        connection.sendall(tranHeader)
        connection.sendall(tranPre)
        connection.sendall(tranDatums)


    def receive(self, connection):

        recvHeader =  connection.recv(self.pduHeaderStruct.size)
        version, unitType, requestedType, dataLen = self.pduHeaderStruct.unpack(recvHeader)
        recvData = connection.recv(dataLen)

        if version != self.VERSION_BYTE:
            self.send(connection, self.UNIT_ERROR, self.NOTHING, (), ())
            return None

        try:
            unitPreStruct = self.unitPreStructs[unitType]
            unitDatumStruct = self.unitDatumStructs[unitType]
        except:
            self.send(connection, self.UNIT_ERROR, self.NOTHING, (), ())
            return None


        try:
            params = unitPreStruct.unpack(recvData[:unitPreStruct.size])
            datums = []
            for i in range(len(recvData[unitPreStruct.size:])):
                startDataIndex = unitPreStruct.size + (i*unitDatumStruct.size)
                dataRoi = recvData[startDataIndex:startDataIndex + unitDatumStruct.size]
                datums.append(unitDatumStruct.unpack(dataRoi))
        except:
            self.send(connection, self.DATA_ERROR, self.NOTHING, (), ())
            return None


        return unitType, requestedType, params, datums



    def provide(self, listener, operator):

        def handle(connection):
            
            unitType, datums = self.receive(connection)

            if unitType == self.INFO:
                self.send(connection, self.INFO_RESPONSE, )

        
        connection, address = listener.accept()

        operator.backend.threadingAsync(handle, connection)


