#
# Copyright (c) 2016-2017 Aedan S. Cullen.
#
# This file is part of the Awareness Python implementation.
#
# Awareness is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Awareness is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Awareness.  If not, see <http://www.gnu.org/licenses/>.
#


from abc import ABCMeta, abstractmethod
import socket
import logging
import awareness.exception
import awareness.misc
import awareness.data

class Protocol(metaclass=ABCMeta):
    @abstractmethod
    def capabilities(self, connection):
        raise NotImplementedError()

    @abstractmethod
    def search(self, connection, recursion_limit, input_set, split_idx, progress_callback=None):
        raise NotImplementedError()

    @abstractmethod
    def process(self, connection, index, input_stream, progress_callback=None):
        raise NotImplementedError()

    @abstractmethod
    def provide(self, listener, operator):
        raise NotImplementedError()

class Protocol0(Protocol, awareness.misc.Protocol0Constants):
    last_search_magic = 0
    last_process_magic = 0

    def capabilities(self, connection):
        self.send(connection, self.BLANK, self.CAPABILITIES, (), [])
        unit_type = None
        while unit_type != self.CAPABILITIES:
            res = self.receive(connection, self.valid_provider_to_accessor)
            if res is None:
                return None
            else:
                unit_type, requested_type, pres, datums = res
        return datums

    def search(self, connection, recursion_limit, input_set, split_idx, progress_callback=None):
        magic = self.last_search_magic
        self.last_search_magic = self.last_search_magic + 1 if self.last_search_magic < self.MAGIC_MAX_VALUE else 0
        self.send(connection, self.SEARCH_TASK_START, self.NOTHING, (magic, input_set.inputs, input_set.outputs, input_set.count, split_idx, recursion_limit), input_set.to_datums())
        pres = (-1, -1)
        while pres[1] is not True:
            res = self.receive(connection, self.valid_provider_to_accessor)
            if res is None:
                return None
            else:
                _unit_type, _requested_type, _pres, _datums = res

            if (_unit_type == self.SEARCH_TASK_STATUS and _pres[0] == magic):
                unit_type, requested_type, pres, datums = _unit_type, _requested_type, _pres, _datums

                if pres[1] is True: continue # Check again now that we've verified we're recieving updates intended for us

                res = progress_callback(awareness.data.Assembly.from_datums(datums)) if progress_callback else True
                if not res:
                    self.send(connection, self.SEARCH_TASK_STOP, self.NOTHING, (), [])
                    return awareness.data.Assembly.from_datums(datums)

        return awareness.data.Assembly.from_datums(datums)

    def process(self, connection, index, input_stream, progress_callback=None):
        magic = self.last_process_magic
        self.last_process_magic = self.last_process_magic + 1 if self.last_process_magic < self.MAGIC_MAX_VALUE else 0
        self.send(connection, self.PROCESS_TASK_START, self.NOTHING, (magic, input_stream.count, index), input_stream.to_datums())
        pres = (-1, -1, -1)

        while pres[2] is not True:
            res = self.receive(connection, self.valid_provider_to_accessor)
            if res is None:
                return None
            else:
                _unit_type, _requested_type, _pres, _datums = res

            if (_unit_type == self.PROCESS_TASK_STATUS and _pres[0] == magic):
                unit_type, requested_type, pres, datums = _unit_type, _requested_type, _pres, _datums

                if pres[2] is True: continue # Check again now that we've verified we're recieving updates intended for us

                res = progress_callback(awareness.data.Stream.from_count_datums(pres[1], datums)) if progress_callback else True
                if not res:
                    self.send(connection, self.PROCESS_TASK_STOP, self.NOTHING, (), [])
                    return awareness.data.Stream.from_count_datums(pres[1], datums)

        return awareness.data.Stream.from_count_datums(pres[1], datums)

    def send(self, connection, unit_type, requested_type, pres, datums):
        logging.getLogger('awareness').debug('Sending type '+str(unit_type)+' requesting '+str(requested_type)+' to '+str(connection.getpeername()[0]))

        try:

            unit_pre_struct = self.unit_pre_structs[unit_type]
            unit_datum_struct = self.unit_datum_structs[unit_type]

            tran_datums = b''
            tran_pres = unit_pre_struct.pack(*pres)

            for datum in datums:
                tran_datums += unit_datum_struct.pack(*datum)

            tran_header = self.pdu_header_struct.pack(self.VERSION_BYTE, unit_type, requested_type, len(tran_datums)+len(tran_pres))

            connection.sendall(tran_header + tran_pres + tran_datums)

        except Exception as e:
            raise awareness.exception.ConnectionException(e)


    def receive(self, connection, valid):
        try:
            recv_header = b''
            while len(recv_header) < self.pdu_header_struct.size:
                res = connection.recv(self.pdu_header_struct.size - len(recv_header))  # This subtraction prevents overfilling
                if len(res) != 0:
                    recv_header += res
                else:
                    raise Exception("Connection closed by peer")
            
            try: 
                version, unit_type, requested_type, data_len = self.pdu_header_struct.unpack(recv_header)
            except:
                self.send(connection, self.UNIT_ERROR, self.NOTHING, (), [])
                raise awareness.exception.UnitError("Received PDU header was unparseable")

            recv_data = b''
            while len(recv_data) < data_len: 
                res = connection.recv(data_len - len(recv_data))  # Same 'goal-subtraction' routine
                if len(res) != 0:
                    recv_data += res
                else:
                    raise Exception("Connection closed by peer")

        except Exception as e:
            raise awareness.exception.ConnectionException(e)

        if version != self.VERSION_BYTE:
            self.send(connection, self.UNIT_ERROR, self.NOTHING, (), [])
            raise awareness.exception.UnitError("Received version did not match the known version")
        if unit_type == self.UNIT_ERROR:
            raise awareness.exception.UnitError("Got UnitError")
        if unit_type == self.DATA_ERROR:
            raise awareness.exception.DataError("Got DataError")
        if unit_type not in valid or requested_type not in valid[unit_type]:
            self.send(connection, self.UNIT_ERROR, self.NOTHING, (), [])
            raise awareness.exception.UnitError("Received unit type or requested type was not valid in context")

        unit_pre_struct = self.unit_pre_structs[unit_type]
        unit_datum_struct = self.unit_datum_structs[unit_type]

        try:
            pres = unit_pre_struct.unpack(recv_data[:unit_pre_struct.size])
            datums = []
            if unit_datum_struct.size > 0:
                for i in range(len(recv_data[unit_pre_struct.size:]) // unit_datum_struct.size):
                    start_data_index = unit_pre_struct.size + (i*unit_datum_struct.size)
                    data_roi = recv_data[start_data_index:start_data_index + unit_datum_struct.size]
                    datums.append(unit_datum_struct.unpack(data_roi))
        except:
            self.send(connection, self.DATA_ERROR, self.NOTHING, (), [])
            raise awareness.exception.DataError("Received preambles and/or datums were unparseable in context")

        logging.getLogger('awareness').debug('Received type '+str(unit_type)+' requesting '+str(requested_type)+' from '+str(connection.getpeername()[0]))
        return unit_type, requested_type, pres, datums

    def provide(self, listener, operator):

        def handle(connection, operator):
            monitor = awareness.misc.ProviderTaskMonitor()
            while True:
                try:
                    res = self.receive(connection, self.valid_accessor_to_provider)

                    unit_type, requested_type, pres, datums = res

                    if unit_type == self.SEARCH_TASK_STOP: monitor.stop_search_task(pres[0])

                    elif unit_type == self.PROCESS_TASK_STOP: monitor.stop_process_task(pres[0])

                    elif unit_type == self.SEARCH_TASK_START:
                        reply_call = lambda assembly: self.send(connection, self.SEARCH_TASK_STATUS, self.NOTHING, (pres[0], False), assembly.to_datums())
                        callback = monitor.add_search_task(pres[0], reply_call)
                        search_args = (pres[5], awareness.data.Set.from_inputs_outputs_count_datums(pres[1], pres[2], pres[3], datums), pres[4])
                        search_kwargs = {'progress_callback':callback}
                        term_callback = lambda assembly: self.send(connection, self.SEARCH_TASK_STATUS, self.NOTHING, (pres[0], True), assembly.to_datums())
                        operator.backend.threading_async(operator.search, search_args, search_kwargs, name='search-' + str(connection.getpeername()[0]) + '-' + str(pres[0]), callback=term_callback)
                    
                    elif unit_type == self.PROCESS_TASK_START:
                        reply_call = lambda stream: self.send(connection, self.PROCESS_TASK_STATUS, self.NOTHING, (pres[0], stream.count, False), stream.to_datums())
                        callback = monitor.add_process_task(pres[0], reply_call)
                        process_args = (pres[2], awareness.data.Stream.from_count_datums(pres[1], datums))
                        process_kwargs = {'progress_callback':callback}
                        term_callback = lambda stream: self.send(connection, self.PROCESS_TASK_STATUS, self.NOTHING, (pres[0], stream.count, True), stream.to_datums())
                        operator.backend.threading_async(operator.process, process_args, process_kwargs, name='process-' + str(connection.getpeername()[0]) + '-' + str(pres[0]), callback=term_callback)

                    if requested_type == self.CAPABILITIES: self.send(connection, self.CAPABILITIES, self.NOTHING, (), operator.capabilities())
                    elif requested_type == self.BLANK: self.send(connection, self.BLANK, self.NOTHING, (), [])

                    elif requested_type == self.SEARCH_TASK_STATUS:
                        res = monitor.get_search_task_latest_args(pres[0])
                        datums = res[1].toDatums() if res else []
                        finished = res[0] if res else False
                        self.send(connection, self.SEARCH_TASK_STATUS, self.NOTHING, (pres[0], finished), datums)

                    elif requested_type == self.PROCESS_TASK_STATUS:                     
                        res = monitor.get_process_task_latest_args(pres[0])
                        count = res[1].count if res else 0
                        datums = res[1].to_datums() if res else []
                        finished = res[0] if res else False
                        self.send(connection, self.PROCESS_TASK_STATUS, self.NOTHING, (pres[0], count, finished), datums)

                except (awareness.exception.ProtocolException, awareness.exception.ConnectionException) as e:
                    logging.getLogger('awareness').info('Closing connection with' + str(connection.getpeername()[0]))
                    connection.shutdown(2) # socket.SHUT_RDWR
                    connection.close()
                    return

        while True:
            connection, address = listener.accept()
            logging.getLogger('awareness').info('Accepted connection from ' + address[0])
            operator.backend.threading_async(handle, args=(connection, operator), name='handle-'+address[0])
