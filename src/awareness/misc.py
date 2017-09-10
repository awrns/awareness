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



import struct

class Protocol0Constants:

    MAGIC_MAX_VALUE = 2**63 - 1

    pdu_header_struct = struct.Struct("!3BQ")

    VERSION_BYTE =          0xA0

    NOTHING =               0x00
    BLANK =                 0x01
    CAPABILITIES =          0x02

    SEARCH_TASK_START =     0x20
    SEARCH_TASK_STATUS =    0x21
    SEARCH_TASK_STOP =      0x22

    PROCESS_TASK_START =    0x30
    PROCESS_TASK_STATUS =   0x31
    PROCESS_TASK_STOP =     0x32

    UNIT_ERROR =            0x40
    DATA_ERROR =            0x41

    blank_pre_struct =                      struct.Struct("!")	    		# intentional
    capabilities_pre_struct =               struct.Struct("!")	    		# intentional

    search_task_start_pre_struct =          struct.Struct("!6Q")    		# magic, inputs, outputs, count, split_idx, recursion_limit
    search_task_status_pre_struct =         struct.Struct("!Q ?")    		# magic, finished
    search_task_stop_pre_struct =           struct.Struct("!Q")	    		# magic

    process_task_start_pre_struct =         struct.Struct("!3Q")    		# magic, count, index
    process_task_status_pre_struct =        struct.Struct("!2Q ?")   		# magic, count, finished
    process_task_stop_pre_struct =          struct.Struct("!Q")	    		# magic

    unit_error_pre_struct =                 struct.Struct("!")      		# intentional
    data_error_pre_struct =                 struct.Struct("!")      		# intentional

    blank_datum_struct =                    struct.Struct("!")
    capabilities_datum_struct =             struct.Struct("!2Q")     		# inputs, outputs

    search_task_start_datum_struct =        struct.Struct("!B")	      	 	# input_set data items(s)
    search_task_status_datum_struct =       struct.Struct("!64s H 3Q")      # addr, port, index, in_offset, out_offset
    
    search_task_stop_datum_struct =         struct.Struct("!")	     		# intentional

    process_task_start_datum_struct =       struct.Struct("!B")	    		# input Stream data item(s)
    process_task_status_datum_struct =      struct.Struct("!B")	    		# output Stream data item(s)
    process_task_stop_datum_struct =        struct.Struct("!")      		# intentional

    unit_error_datum_struct =               struct.Struct("!")	   		    # intentional
    data_error_datum_struct =               struct.Struct("!")	    		# intentional

    unit_pre_structs = {BLANK: blank_pre_struct,
                        CAPABILITIES: capabilities_pre_struct,
                        SEARCH_TASK_STOP: search_task_stop_pre_struct,
                        PROCESS_TASK_STOP: process_task_stop_pre_struct,
                        SEARCH_TASK_START: search_task_start_pre_struct,
                        SEARCH_TASK_STATUS: search_task_status_pre_struct,
                        PROCESS_TASK_START: process_task_start_pre_struct,
                        PROCESS_TASK_STATUS: process_task_status_pre_struct,
                        UNIT_ERROR: unit_error_pre_struct,
                        DATA_ERROR: data_error_pre_struct}

    unit_datum_structs = {BLANK: blank_datum_struct,
                          CAPABILITIES: capabilities_datum_struct,
                          SEARCH_TASK_STOP: search_task_stop_datum_struct,
                          PROCESS_TASK_STOP: process_task_stop_datum_struct,
                          SEARCH_TASK_START: search_task_start_datum_struct,
                          SEARCH_TASK_STATUS: search_task_status_datum_struct,
                          PROCESS_TASK_START: process_task_start_datum_struct,
                          PROCESS_TASK_STATUS: process_task_status_datum_struct,
                          UNIT_ERROR: unit_error_datum_struct,
                          DATA_ERROR: data_error_datum_struct}

    valid_provider_to_accessor = {BLANK: (NOTHING,),
                                  CAPABILITIES: (NOTHING,),
                                  SEARCH_TASK_STATUS: (NOTHING,),
                                  PROCESS_TASK_STATUS: (NOTHING,)}

    valid_accessor_to_provider = {BLANK: (BLANK, CAPABILITIES),
                                  SEARCH_TASK_STOP: (NOTHING, BLANK, CAPABILITIES),
                                  PROCESS_TASK_STOP: (NOTHING, BLANK, CAPABILITIES),
                                  SEARCH_TASK_START: (NOTHING, BLANK, CAPABILITIES),
                                  PROCESS_TASK_START: (NOTHING, BLANK, CAPABILITIES)}


class ProviderTask:

    progress_callback = None
    proceed = True

    latest_args = None  # Intended for direct attribute access.
    latest_kwargs = None

    def __init__(self, progress_callback):
        self.progress_callback = progress_callback

    def update(self, *args, **kwargs):
        self.latest_args = args  # Intended for direct attribute access.
        self.latest_kwargs = kwargs  # ''

        if self.proceed:
            self.progress_callback(*args, **kwargs)
            return True
        else:
            return False


    def stop(self):
        self.proceed = False


class ProviderTaskMonitor:

    search_tasks = {}
    process_tasks = {}

    def add_search_task(self, magic, progress_callback):  # There's no point in having no progress_callback here
        new_task = ProviderTask(progress_callback)
        self.search_tasks[magic] = new_task
        return new_task.update  # as callable, that is.

    def add_process_task(self, magic, progress_callback):
        new_task = ProviderTask(progress_callback)
        self.process_tasks[magic] = new_task
        return new_task.update


    def stop_search_task(self, magic):
        self.search_tasks[magic].stop()

    def stop_process_task(self, magic):
        self.process_tasks[magic].stop()

    def get_search_task_latest_args(self, magic):
        return self.search_tasks[magic].latest_args

    def get_process_task_latest_args(self, magic):
        return self.process_tasks[magic].latest_args
