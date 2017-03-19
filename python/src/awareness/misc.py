from abc import ABCMeta, abstractproperty

import struct



class Protocol0Constants:

    pduHeaderStruct = struct.Struct("!3c")


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


