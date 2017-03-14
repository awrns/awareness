import struct



class Protocol0Constants:

    pduHeaderStruct = struct.Struct("!3cQ")


    VERSION_BYTE =          0xA0

    NOTHING =               0x00
    BLANK =                 0x01

    SEARCH_CAPABILITIES =   0x10
    SEARCH_TASK_PARAMS =    0x11
    SEARCH_TASK_START =     0x12
    SEARCH_TASK_STOP =      0x13
    SEARCH_TASK_STATUS =    0x14

    PROCESS_CAPABILITIES =  0x20
    PROCESS_TASK_PARAMS =   0x21
    PROCESS_TASK_START =    0x22
    PROCESS_TASK_STOP =     0x23
    PROCESS_TASK_STATUS =   0x24

    UNIT_ERROR =            0x30
    DATA_ERROR =            0x31


    blankPreStruct =                    struct.Struct("!")

    searchCapabilitiesPreStruct =       struct.Struct("!")
    searchTaskParamsPreStruct =         struct.Struct("!")
    searchTaskStartPreStruct =          struct.Struct("!")
    searchTaskStopPreStruct =           struct.Struct("!")
    searchTaskStatusPreStruct =         struct.Struct("!")

    processCapabilitiesPreStruct =      struct.Struct("!")
    processTaskParamsPreStruct =        struct.Struct("!")
    processTaskStartPreStruct =         struct.Struct("!")
    processTaskStopPreStruct =          struct.Struct("!")
    processTaskStatusPreStruct =         struct.Struct("!")

    unitErrorPreStruct =                struct.Struct("!")
    dataErrorPreStruct =                struct.Struct("!")


    blankDatumStruct =                  struct.Struct("!")

    searchCapabilitiesDatumStruct =     struct.Struct("!")
    searchTaskParamsDatumStruct =       struct.Struct("!")
    searchTaskStartDatumStruct =        struct.Struct("!")
    searchTaskStopDatumStruct =         struct.Struct("!")
    searchTaskStatusDatumStruct =       struct.Struct("!")

    processCapabilitiesDatumStruct =    struct.Struct("!")
    processTaskParamsDatumStruct =      struct.Struct("!")
    processTaskStartDatumStruct =       struct.Struct("!")
    processTaskStopDatumStruct =        struct.Struct("!")
    processTaskStatusDatumStruct =      struct.Struct("!")

    unitErrorDatumStruct =              struct.Struct("!")
    dataErrorDatumStruct =              struct.Struct("!")


    unitPreStructs = {BLANK: blankPreStruct,
                      SEARCH_CAPABILITIES: searchCapabilitiesPreStruct,
                      SEARCH_TASK_PARAMS: searchTaskParamsPreStruct,
                      SEARCH_TASK_START: searchTaskStartPreStruct,
                      SEARCH_TASK_STOP: searchTaskStopPreStruct,
                      SEARCH_TASK_STATUS: searchTaskStatusPreStruct,
                      PROCESS_CAPABILITIES: processCapabilitiesPreStruct,
                      PROCESS_TASK_PARAMS: processTaskParamsPreStruct,
                      PROCESS_TASK_START: processTaskStartPreStruct,
                      PROCESS_TASK_STOP: processTaskStopPreStruct,
                      PROCESS_TASK_STATUS: processTaskStatusPreStruct,
                      UNIT_ERROR: unitErrorPreStruct,
                      DATA_ERROR: dataErrorPreStruct}


    unitDatumStructs = {BLANK: blankDatumStruct,
                        SEARCH_CAPABILITIES: searchCapabilitiesDatumStruct,
                        SEARCH_TASK_PARAMS: searchTaskParamsDatumStruct,
                        SEARCH_TASK_START: searchTaskStartDatumStruct,
                        SEARCH_TASK_STOP: searchTaskStopDatumStruct,
                        SEARCH_TASK_STATUS: searchTaskStatusDatumStruct,
                        PROCESS_CAPABILITIES: processCapabilitiesDatumStruct,
                        PROCESS_TASK_PARAMS: processTaskParamsDatumStruct,
                        PROCESS_TASK_START: processTaskStartDatumStruct,
                        PROCESS_TASK_STOP: processTaskStopDatumStruct,
                        PROCESS_TASK_STATUS: processTaskStatusDatumStruct,
                        UNIT_ERROR: unitErrorDatumStruct,
                        DATA_ERROR: dataErrorDatumStruct}
