from abc import ABCMeta, abstractproperty

import struct



class Protocol0Constants:

    pduHeaderStruct = struct.Struct("!3c")


    VERSION_BYTE =          0xA0

    NOTHING =               0x00
    BLANK =                 0x01

    CAPABILITIES =          0x10
    TASK_STOP =             0x11

    SEARCH_TASK_START =     0x20
    SEARCH_TASK_STATUS =    0x21

    PROCESS_TASK_START =    0x30
    PROCESS_TASK_STATUS =   0x31

    UNIT_ERROR =            0x40
    DATA_ERROR =            0x41


    blankPreStruct =                    struct.Struct("!")

    capabilitiesPreStruct =             struct.Struct("!")
    taskStopPreStruct =                 struct.Struct("!")

    searchTaskStartPreStruct =          struct.Struct("!")
    searchTaskStatusPreStruct =         struct.Struct("!")

    processTaskStartPreStruct =         struct.Struct("!")
    processTaskStatusPreStruct =        struct.Struct("!")

    unitErrorPreStruct =                struct.Struct("!")
    dataErrorPreStruct =                struct.Struct("!")


    blankDatumStruct =                  struct.Struct("!")

    capabilitiesDatumStruct =           struct.Struct("!")
    taskStopDatumStruct =               struct.Struct("!")

    searchTaskStartDatumStruct =        struct.Struct("!")
    searchTaskStatusDatumStruct =       struct.Struct("!")

    processTaskStartDatumStruct =       struct.Struct("!")
    processTaskStatusDatumStruct =      struct.Struct("!")

    unitErrorDatumStruct =              struct.Struct("!")
    dataErrorDatumStruct =              struct.Struct("!")


    unitPreStructs = {BLANK: blankPreStruct,
                      CAPABILITIES: capabilitiesPreStruct,
                      TASK_STOP: taskStopPreStruct,
                      SEARCH_TASK_START: searchTaskStartPreStruct,
                      SEARCH_TASK_STATUS: searchTaskStatusPreStruct,
                      PROCESS_TASK_START: processTaskStartPreStruct,
                      PROCESS_TASK_STATUS: processTaskStatusPreStruct,
                      UNIT_ERROR: unitErrorPreStruct,
                      DATA_ERROR: dataErrorPreStruct}


    unitDatumStructs = {BLANK: blankDatumStruct,
                        CAPABILITIES: capabilitiesDatumStruct,
                        TASK_STOP: taskStopDatumStruct,
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
                               TASK_STOP: (NOTHING, BLANK, SEARCH_TASK_STATUS, PROCESS_TASK_STATUS),
                               SEARCH_TASK_START: (NOTHING, BLANK, CAPABILITIES, SEARCH_TASK_STATUS, PROCESS_TASK_STATUS),
                               PROCESS_TASK_START: (NOTHING, BLANK, CAPABILITIES, SEARCH_TASK_STATUS, PROCESS_TASK_STATUS)}


