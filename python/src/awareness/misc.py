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


from abc import ABCMeta, abstractproperty

import struct

class Protocol0Constants:
    pduHeaderStruct = struct.Struct("!3BQ")

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

    blankPreStruct =                    struct.Struct("!")
    capabilitiesPreStruct =             struct.Struct("!")

    searchTaskStartPreStruct =          struct.Struct("!")
    searchTaskStatusPreStruct =         struct.Struct("!")
    searchTaskStopPreStruct =           struct.Struct("!")

    processTaskStartPreStruct =         struct.Struct("!")
    processTaskStatusPreStruct =        struct.Struct("!")
    processTaskStopDatumStruct =        struct.Struct("!")

    unitErrorPreStruct =                struct.Struct("!")
    dataErrorPreStruct =                struct.Struct("!")

    blankDatumStruct =                  struct.Struct("!")
    capabilitiesDatumStruct =           struct.Struct("!")

    searchTaskStartDatumStruct =        struct.Struct("!")
    searchTaskStatusDatumStruct =       struct.Struct("!")
    searchTaskStopDatumStruct =         struct.Struct("!")

    processTaskStartDatumStruct =       struct.Struct("!")
    processTaskStatusDatumStruct =      struct.Struct("!")
    processTaskStopPreStruct =          struct.Struct("!")

    unitErrorDatumStruct =              struct.Struct("!")
    dataErrorDatumStruct =              struct.Struct("!")

    unitPreStructs = {BLANK: blankPreStruct,
                      CAPABILITIES: capabilitiesPreStruct,
                      SEARCH_TASK_STOP: searchTaskStopPreStruct,
                      PROCESS_TASK_STOP: processTaskStopPreStruct,
                      SEARCH_TASK_START: searchTaskStartPreStruct,
                      SEARCH_TASK_STATUS: searchTaskStatusPreStruct,
                      PROCESS_TASK_START: processTaskStartPreStruct,
                      PROCESS_TASK_STATUS: processTaskStatusPreStruct,
                      UNIT_ERROR: unitErrorPreStruct,
                      DATA_ERROR: dataErrorPreStruct}

    unitDatumStructs = {BLANK: blankDatumStruct,
                        CAPABILITIES: capabilitiesDatumStruct,
                        SEARCH_TASK_STOP: searchTaskStopDatumStruct,
                        PROCESS_TASK_STOP: processTaskStopDatumStruct,
                        SEARCH_TASK_START: searchTaskStartDatumStruct,
                        SEARCH_TASK_STATUS: searchTaskStatusDatumStruct,
                        PROCESS_TASK_START: processTaskStartDatumStruct,
                        PROCESS_TASK_STATUS: processTaskStatusDatumStruct,
                        UNIT_ERROR: unitErrorDatumStruct,
                        DATA_ERROR: dataErrorDatumStruct}

    validProviderToAccessor = {BLANK: (NOTHING),
                               CAPABILITIES: (NOTHING),
                               SEARCH_TASK_STATUS: (NOTHING),
                               PROCESS_TASK_STATUS: (NOTHING)}

    validAccessorToProvider = {BLANK: (BLANK, CAPABILITIES, SEARCH_TASK_STATUS, PROCESS_TASK_STATUS),
                               SEARCH_TASK_STOP: (NOTHING, BLANK, SEARCH_TASK_STATUS, PROCESS_TASK_STATUS),
                               PROCESS_TASK_STOP: (NOTHING, BLANK, SEARCH_TASK_STATUS, PROCESS_TASK_STATUS),
                               SEARCH_TASK_START: (NOTHING, BLANK, CAPABILITIES, SEARCH_TASK_STATUS, PROCESS_TASK_STATUS),
                               PROCESS_TASK_START: (NOTHING, BLANK, CAPABILITIES, SEARCH_TASK_STATUS, PROCESS_TASK_STATUS)}


class ProvidorTask:

    progressCallback = None
    proceed = True

    latestArgs = None  # Intended for direct attribute access.
    latestKwargs = None

    def __init__(self, progressCallback):
        self.progressCallback = progressCallback

    def update(self, *args, **kwargs):
        self.latestArgs = args  # Intended for direct attribute access.
        self.latestKwargs = kwargs  # ''

        if self.proceed:
            self.progressCallback(*args, **kwargs)
            return True
        else:
            return False


    def stop(self):
        self.proceed = False


class ProvidorTaskMonitor:

    searchTasks = {}
    processTasks = {}

    def addSearchTask(self, magic, progressCallback):  # There's no point in having no progressCallback here
        newTask = ProvidorTask(progressCallback)
        self.searchTasks[magic] = newTask
        return newTask.update  # as callable, that is.

    def addProcessTask(self, magic, progressCallback):
        newTask = ProvidorTask(progressCallback)
        self.searchTasks[magic] = newTask
        return newTask.update


    def stopSearchTask(self, magic):
        self.searchTasks[magic].stop()

    def stopProcessTask(self, magic):
        self.processTasks[magic].stop()

    def getSearchTaskLatestArgsKwargs(self, magic):
        return self.searchTasks[magic].latestArgs, self.searchTasks[magic].latestKwargs

    def getProcessTaskLatestArgsKwargs(self, magic):
        return self.processTasks[magic].latestArgs, self.processTasks[magic].latestKwargs
