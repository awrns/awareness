#
# This file is part of the Awareness Operator Python implementation.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from abc import ABCMeta, abstractproperty, abstractmethod
import logging
import exception
import misc
import affinity as i_affinity
import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import operator as i_operator

class Protocol:
    __metaclass__ = ABCMeta

    @abstractmethod
    def capabilities(self, connection):
        raise NotImplementedError()

    @abstractmethod
    def search(self, connection, propagationLimit, inputSet, progressFrequency=0, progressCallback=None):
        raise NotImplementedError()

    @abstractmethod
    def process(self, connection, index, inputStream, progressFrequency=0, progressCallback=None):
        raise NotImplementedError()

    @abstractmethod
    def provide(self, listener, operator):
        raise NotImplementedError()

class Protocol0(Protocol, misc.Protocol0Constants):
    lastSearchMagic = 0
    lastProcessMagic = 0

    def capabilities(self, connection):
        self.send(connection, self.BLANK, self.CAPABILITIES, (), [])
        unitType = None
        while unitType != self.CAPABILITIES:
            res = self.receive(connection, self.validProviderToAccessor)
            if res is None:
                return None
            else:
                unitType, requestedType, pres, datums = res
        return datums

    def search(self, connection, propagationLimit, inputSet, progressFrequency=0, progressCallback=None):
        magic = self.lastSearchMagic
        self.lastSearchMagic = self.lastSearchMagic + 1 if self.lastSearchMagic < self.MAGIC_MAX_VALUE else 0
        self.send(connection, self.SEARCH_TASK_START, self.SEARCH_TASK_STATUS, (magic, inputSet.inputStream.count, inputSet.outputStream.count, inputSet.count, propagationLimit, progressFrequency), inputSet.toDatums())
        pres = (-1, -1)
        while pres[1] != 1:
            res = self.receive(connection, self.validProviderToAccessor)
            if res is None:
                return None
            else:
                _unitType, _requestedType, _pres, _datums = res

            if (_unitType == self.SEARCH_TASK_STATUS and _pres[0] == magic):
                unitType, requestedType, pres, datums = _unitType, _requestedType, _pres, _datums

                res = progressCallback(i_data.Assembly.fromDatums(datums))
                if not res:
                    self.send(connection, self.SEARCH_TASK_STOP, self.NOTHING, (), [])
                    return i_data.Assembly.fromDatums(datums)

        return i_data.Assembly(datums)

    def process(self, connection, index, inputStream, progressFrequency=0, progressCallback=None):
        magic = self.lastProcessMagic
        self.lastProcessMagic = self.lastProcessMagic + 1 if self.lastProcessMagic < self.MAGIC_MAX_VALUE else 0
        self.send(connection, self.PROCESS_TASK_START, self.PROCESS_TASK_STATUS, (magic, inputStream.count, index, progressFrequency), inputStream.toDatums())
        pres = (-1, -1, -1)
        while pres[2] != 1:
            res = self.receive(connection, self.validProviderToAccessor)
            if res is None:
                return None
            else:
                _unitType, _requestedType, _pres, _datums = res

            if (_unitType == self.PROCESS_TASK_STATUS and _pres[0] == magic):
                unitType, requestedType, pres, datums = _unitType, _requestedType, _pres, _datums

                res = progressCallback(i_data.Stream.fromCountDatums(pres[1], datums))
                if not res:
                    self.send(connection, self.PROCESS_TASK_STOP, self.NOTHING, (), [])
                    return i_data.Stream.fromCountDatums(pres[1], datums)

        return i_data.Set(datums)

    def send(self, connection, unitType, requestedType, pres, datums):
        unitPreStruct = self.unitPreStructs[unitType]
        unitDatumStruct = self.unitDatumStructs[unitType]

        tranDatums = ''
        tranPres = unitPreStruct.pack(*pres)

        for datum in datums:
            tranDatums += unitDatumStruct.pack(*datum)

        tranHeader = self.pduHeaderStruct.pack(self.VERSION_BYTE, unitType, requestedType, len(tranDatums)+len(tranPres))

        connection.sendall(tranHeader)
        connection.sendall(tranPres)
        connection.sendall(tranDatums)

    def receive(self, connection, valid):
        recvHeader = connection.recv(self.pduHeaderStruct.size)
        if len(recvHeader) < self.pduHeaderStruct.size: raise exception.ConnectionEnded("Received header was not of the required length")
        version, unitType, requestedType, dataLen = self.pduHeaderStruct.unpack(recvHeader)
        recvData = connection.recv(dataLen) if dataLen > 0 else ''

        if version != self.VERSION_BYTE:
            self.send(connection, self.UNIT_ERROR, self.NOTHING, (), [])
            raise exception.UnitError("Received version did match the known version")
        if unitType not in valid or requestedType not in valid[unitType]:
            self.send(connection, self.UNIT_ERROR, self.NOTHING, (), [])
            raise exception.UnitError("Received unit type or requested type was not valid in context")

        unitPreStruct = self.unitPreStructs[unitType]
        unitDatumStruct = self.unitDatumStructs[unitType]

        try:
            pres = unitPreStruct.unpack(recvData[:unitPreStruct.size])
            datums = []
            if unitDatumStruct.size > 0:
                for i in range(len(recvData[unitPreStruct.size:]) / unitDatumStruct.size):
                    startDataIndex = unitPreStruct.size + (i*unitDatumStruct.size)
                    dataRoi = recvData[startDataIndex:startDataIndex + unitDatumStruct.size]
                    datums.append(unitDatumStruct.unpack(dataRoi))
        except:
            self.send(connection, self.DATA_ERROR, self.NOTHING, (), [])
            raise exception.DataError("Received preambles and/or datums were unparseable in context")

        return unitType, requestedType, pres, datums

    def provide(self, listener, operator):

        def handle(connection, operator):
            logging.getLogger('awareness').info('Interacting with accesser..')
            monitor = misc.ProviderTaskMonitor()
            while True:
                try:
                    res = self.receive(connection, self.validAccessorToProvider)

                    unitType, requestedType, pres, datums = res

                    if unitType == self.SEARCH_TASK_STOP: monitor.stopSearchTask(pres[0])
                    elif unitType == self.PROCESS_TASK_STOP: monitor.stopProcessTask(pres[0])
                    elif unitType == self.SEARCH_TASK_START:
                        replyCall = lambda progress, assembly: self.send(connection, self.SEARCH_TASK_STATUS, self.NOTHING, (pres[0], progress), assembly.toDatums())
                        callback = monitor.addSearchTask(pres[0], replyCall)
                        searchArgs = (pres[4], i_data.Set.fromInputsOuputsCountDatums(pres[1], pres[2], pres[3], datums))
                        searchKwargs = {'progressFrequency':pres[5], 'progressCallback':callback}
                        i_backend.threadingAsync(operator.search, searchArgs, searchKwargs, name='Search-' + str(connection.getsockname()[0]) + '-' + str(pres[0]))
                    elif unitType == self.PROCESS_TASK_START:
                        replyCall = lambda progress, outputSet: self.send(connection, self.PROCESS_TASK_STATUS, self.NOTHING, (pres[0], outputSet.count, progress), outputSet.toDatums())
                        callback = monitor.addProcessTask(pres[0], replyCall)
                        processArgs = (pres[2], i_data.Stream.fromCountDatums(pres[1], datums))
                        processKwargs = {'progressFrequency':pres[3], 'progressCallback':callback}
                        i_backend.threadingAsync(operator.process, processArgs, processKwargs, name='Process-' + str(connection.getsockname()[0]) + '-' + str(pres[0]))

                    if requestedType == self.CAPABILITIES: self.send(connection, self.CAPABILITIES, self.NOTHING, (), operator.capabilities())
                    elif requestedType == self.BLANK: self.send(connection, self.BLANK, self.NOTHING, (), [])
                    elif requestedType == self.SEARCH_TASK_STATUS:
                        self.send(connection, self.SEARCH_TASK_STATUS, self.NOTHING, (), monitor.getSearchTaskLatestArgsKwargs(pres[0]).toDatums())
                    elif requestedType == self.PROCESS_TASK_STATUS:
                        self.send(connection, self.PROCESS_TASK_STATUS, self.NOTHING, (), monitor.getProcessTaskLatestArgsKwargs(pres[0]).toDatums())

                except exception.ProvisionException as e:
                    logging.getLogger('awareness').info('Finished interaction, exiting: ' + type(e).__name__)
                    connection.close()
                    return

        while True:
            connection, address = listener.accept()
            logging.getLogger('awareness').info('Accepted connection from ' + address[0] + ', spawning handler')
            operator.backend.threadingAsync(handle, args=(connection, operator), name='Handle-'+address[0])
