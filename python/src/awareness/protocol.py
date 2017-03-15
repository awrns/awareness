from abc import ABCMeta, abstractproperty, abstractmethod
import socket
import misc
import affinity as i_affinity
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
    def serve(self, listener, operator):
        raise NotImplementedError()


    @abstractmethod
    def provideReceiveMonitor(self, connection, operator):
        raise NotImplementedError()


    @abstractmethod
    def accessReceiveMonitor(self, connection):
        raise NotImplementedError()



class Protocol0(Protocol, misc.Protocol0Constants):


    def searchCapabilities(self, connection):
        
        pass

    def processCapabilities(self, connection):
        
        pass

    def search(self, connection, propagationLimit, trainingSet, testSet, progressCallback=None):
        
        pass

    def process(self, connection, index, inputSet, progressCallback=None):

        pass


    def send(self, connection, unitType, requestedType, pres, datums):

        unitPreStruct = self.unitPreStructs[unitType]
        unitDatumStruct = self.unitDatumStructs[unitType]

        tranDatums = ''
        tranPres = unitPreStruct.pack(pres)

        for datum in datums:
            tranDatums.append(unitDatumStruct.pack(datum))


        tranHeader = self.pduHeaderStruct.pack(self.VERSION_BYTE, unitType, requestedType, len(tranDatums)+len(tranPres))

        connection.sendall(tranHeader)
        connection.sendall(tranPres)
        connection.sendall(tranDatums)


    def receive(self, connection, valid):

        recvHeader =  connection.recv(self.pduHeaderStruct.size)
        version, unitType, requestedType, dataLen = self.pduHeaderStruct.unpack(recvHeader)
        recvData = connection.recv(dataLen)

        if version != self.VERSION_BYTE:
            self.send(connection, self.UNIT_ERROR, self.NOTHING, (), ())
            return None

        if unitType not in valid or requestedType not in valid[unitType]:
            self.send(connection, self.UNIT_ERROR, self.NOTHING, (), ())
            return None


        try:
            unitPreStruct = self.unitPreStructs[unitType]
            unitDatumStruct = self.unitDatumStructs[unitType]
        except:
            self.send(connection, self.UNIT_ERROR, self.NOTHING, (), ())
            return None


        try:
            pres = unitPreStruct.unpack(recvData[:unitPreStruct.size])
            datums = []
            for i in range(len(recvData[unitPreStruct.size:])):
                startDataIndex = unitPreStruct.size + (i*unitDatumStruct.size)
                dataRoi = recvData[startDataIndex:startDataIndex + unitDatumStruct.size]
                datums.append(unitDatumStruct.unpack(dataRoi))
        except:
            self.send(connection, self.DATA_ERROR, self.NOTHING, (), ())
            return None


        return unitType, requestedType, pres, datums



    def serve(self, listener, operator):
        
        connection, address = listener.accept()

        operator.backend.threadingAsync(self.provideReceiveMonitor, (connection, operator))



    def provideReceiveMonitor(self, connection, operator):

        while True:
            try:

                res = self.receive(connection, self.validAccessorToProvider)

                if res is not None:

                    unitType, requestedType, pres, datums = res

                    if unitType == self.BLANK:
                        if requestedType == self.BLANK: self.send(connection, self.BLANK, self.NOTHING, (), ())
                        elif requestedType == self.SEARCH_CAPABILITIES: pass  # TODO stuff.

            except socket.error:
                break


    def accessReceiveMonitor(self, connection):

        while True:
            try:

                res = self.receive(connection, self.validProviderToAccessor)

                if res is not None:

                    unitType, requestedType, pres, datums = res

                    if unitType == self.BLANK:
                        pass
# TODO stuff...
                    elif unitType == self.SEARCH_CAPABILITIES:
                        pass

                    elif unitType == self.SEARCH_PARAMS:
                        pass

                    elif unitType == self.SEARCH_STATUS:
                        pass

                    elif unitType == self.PROCESS_CAPABILITIES:
                        pass

                    elif unitType == self.PROCESS_PARAMS:
                        pass

                    elif unitType == self.PROCESS_STATUS:
                        pass


            except socket.error:
                break



