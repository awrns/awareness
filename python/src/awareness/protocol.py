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
import socket
import logging
import exception
import misc
import component as i_component
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
    def search(self, connection, recursion_limit, input_set, progress_frequency=0, progress_callback=None):
        raise NotImplementedError()

    @abstractmethod
    def process(self, connection, index, input_stream, progress_frequency=0, progress_callback=None):
        raise NotImplementedError()

    @abstractmethod
    def provide(self, listener, operator):
        raise NotImplementedError()

class Protocol0(Protocol, misc.Protocol0Constants):
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

    def search(self, connection, recursion_limit, input_set, progress_frequency=0, progress_callback=None):
        magic = self.last_search_magic
        self.last_search_magic = self.last_search_magic + 1 if self.last_search_magic < self.MAGIC_MAX_VALUE else 0
        self.send(connection, self.SEARCH_TASK_START, self.NOTHING, (magic, input_set.n_inputs, input_set.n_outputs, input_set.count, recursion_limit, progress_frequency), input_set.to_datums())
        pres = (-1, -1)
        while pres[1] != 1:
            res = self.receive(connection, self.valid_provider_to_accessor)
            if res is None:
                return None
            else:
                _unit_type, _requested_type, _pres, _datums = res

            if (_unit_type == self.SEARCH_TASK_STATUS and _pres[0] == magic):
                unit_type, requested_type, pres, datums = _unit_type, _requested_type, _pres, _datums

                res = progress_callback(i_data.Assembly.from_datums(datums)) if progress_callback else True
                if not res:
                    self.send(connection, self.SEARCH_TASK_STOP, self.NOTHING, (), [])
                    return i_data.Assembly.from_datums(datums)

        return i_data.Assembly.from_datums(datums)

    def process(self, connection, index, input_stream, progress_frequency=0, progress_callback=None):
        magic = self.last_process_magic
        self.last_process_magic = self.last_process_magic + 1 if self.last_process_magic < self.MAGIC_MAX_VALUE else 0
        self.send(connection, self.PROCESS_TASK_START, self.NOTHING, (magic, input_stream.count, index, progress_frequency), input_stream.to_datums())
        pres = (-1, -1, -1)
        while pres[2] != 1:
            res = self.receive(connection, self.valid_provider_to_accessor)
            if res is None:
                return None
            else:
                _unit_type, _requested_type, _pres, _datums = res

            if (_unit_type == self.PROCESS_TASK_STATUS and _pres[0] == magic):
                unit_type, requested_type, pres, datums = _unit_type, _requested_type, _pres, _datums

                res = progress_callback(i_data.Stream.from_count_datums(pres[1], datums)) if progress_callback else True
                if not res:
                    self.send(connection, self.PROCESS_TASK_STOP, self.NOTHING, (), [])
                    return i_data.Stream.from_count_datums(pres[1], datums)

        return i_data.Stream.from_count_datums(pres[1], datums)

    def send(self, connection, unit_type, requested_type, pres, datums):
        logging.getLogger('awareness').info('Sending type '+str(unit_type)+' requesting '+str(requested_type)+' to '+str(connection.getpeername()[0]))

        unit_pre_struct = self.unit_pre_structs[unit_type]
        unit_datum_struct = self.unit_datum_structs[unit_type]

        tran_datums = ''
        tran_pres = unit_pre_struct.pack(*pres)

        for datum in datums:
            tran_datums += unit_datum_struct.pack(*datum)

        tran_header = self.pdu_header_struct.pack(self.VERSION_BYTE, unit_type, requested_type, len(tran_datums)+len(tran_pres))

        connection.sendall(tran_header + tran_pres + tran_datums)


    def receive(self, connection, valid):
        recv_header = ''
        while len(recv_header) < self.pdu_header_struct.size: recv_header += connection.recv(self.pdu_header_struct.size - len(recv_header))  # This subtraction precents overfilling
        version, unit_type, requested_type, data_len = self.pdu_header_struct.unpack(recv_header)
        recv_data = ''
        while len(recv_data) < data_len: recv_data += connection.recv(data_len - len(recv_data))  # Same 'goal-subtraction' routine

        if version != self.VERSION_BYTE:
            self.send(connection, self.UNIT_ERROR, self.NOTHING, (), [])
            raise exception.UnitError("Received version did not match the known version")
        if unit_type not in valid or requested_type not in valid[unit_type]:
            self.send(connection, self.UNIT_ERROR, self.NOTHING, (), [])
            raise exception.UnitError("Received unit type or requested type was not valid in context")

        unit_pre_struct = self.unit_pre_structs[unit_type]
        unit_datum_struct = self.unit_datum_structs[unit_type]

        try:
            pres = unit_pre_struct.unpack(recv_data[:unit_pre_struct.size])
            datums = []
            if unit_datum_struct.size > 0:
                for i in range(len(recv_data[unit_pre_struct.size:]) / unit_datum_struct.size):
                    start_data_index = unit_pre_struct.size + (i*unit_datum_struct.size)
                    data_roi = recv_data[start_data_index:start_data_index + unit_datum_struct.size]
                    datums.append(unit_datum_struct.unpack(data_roi))
        except:
            self.send(connection, self.DATA_ERROR, self.NOTHING, (), [])
            raise exception.DataError("Received preambles and/or datums were unparseable in context")

        logging.getLogger('awareness').info('Received type '+str(unit_type)+' requesting '+str(requested_type)+' from '+str(connection.getpeername()[0]))
        return unit_type, requested_type, pres, datums

    def provide(self, listener, operator):

        def handle(connection, operator):
            monitor = misc.ProviderTaskMonitor()
            while True:
                try:
                    res = self.receive(connection, self.valid_accessor_to_provider)

                    unit_type, requested_type, pres, datums = res

                    if unit_type == self.SEARCH_TASK_STOP: monitor.stop_search_task(pres[0])

                    elif unit_type == self.PROCESS_TASK_STOP: monitor.stop_process_task(pres[0])

                    elif unit_type == self.SEARCH_TASK_START:
                        reply_call = lambda progress, assembly: self.send(connection, self.SEARCH_TASK_STATUS, self.NOTHING, (pres[0], assembly), assembly.to_datums())
                        callback = monitor.add_search_task(pres[0], reply_call)
                        search_args = (pres[4], i_data.Set.from_inputs_outputs_count_datums(pres[1], pres[2], pres[3], datums))
                        search_kwargs = {'progress_frequency':pres[5], 'progress_callback':callback}
                        term_callback = lambda assembly: self.send(connection, self.SEARCH_TASK_STATUS, self.NOTHING, (pres[0], 1.0), assembly.to_datums())
                        operator.backend.threading_async(operator.search, search_args, search_kwargs, name='Search-' + str(connection.getpeername()[0]) + '-' + str(pres[0]), callback=term_callback)
                    
                    elif unit_type == self.PROCESS_TASK_START:
                        reply_call = lambda progress, stream: self.send(connection, self.PROCESS_TASK_STATUS, self.NOTHING, (pres[0], stream.count, progress), stream.to_datums())
                        callback = monitor.add_process_task(pres[0], reply_call)
                        process_args = (pres[2], i_data.Stream.from_count_datums(pres[1], datums))
                        process_kwargs = {'progress_frequency':pres[3], 'progress_callback':callback}
                        term_callback = lambda stream: self.send(connection, self.PROCESS_TASK_STATUS, self.NOTHING, (pres[0], stream.count, 1.0), stream.to_datums())
                        operator.backend.threading_async(operator.process, process_args, process_kwargs, name='Process-' + str(connection.getpeername()[0]) + '-' + str(pres[0]), callback=term_callback)

                    if requested_type == self.CAPABILITIES: self.send(connection, self.CAPABILITIES, self.NOTHING, (), operator.capabilities())
                    elif requested_type == self.BLANK: self.send(connection, self.BLANK, self.NOTHING, (), [])

                    elif requested_type == self.SEARCH_TASK_STATUS:
                        res = monitor.get_search_task_latest_args(pres[0])
                        datums = res[1].toDatums() if res else []
                        progress = res[0] if res else 0
                        self.send(connection, self.SEARCH_TASK_STATUS, self.NOTHING, (pres[0], progress), datums)

                    elif requested_type == self.PROCESS_TASK_STATUS:                     
                        res = monitor.get_process_task_latest_args(pres[0])
                        count = res[1].count if res else 0
                        datums = res[1].to_datums() if res else []
                        progress = res[0] if res else 0
                        self.send(connection, self.PROCESS_TASK_STATUS, self.NOTHING, (pres[0], count, progress), datums)

                except (exception.ProvisionException, exception.ConnectionException, socket.error) as e:  # Use of ConnectionException for custom backends
                    connection.close()
                    return

        while True:
            connection, address = listener.accept()
            logging.getLogger('awareness').info('Accepted connection from ' + address[0])
            operator.backend.threading_async(handle, args=(connection, operator), name='Handle-'+address[0])
