import struct



class Protocol0Constants:

    pduHeaderStruct = struct.Struct("!3cQ")


    VERSION_BYTE =          0xA0

    NOTHING =               0x00
    BLANK =                 0x01

    SEARCH_CAPABILITIES =   0x10
    SEARCH_PARAMS =    0x11
    SEARCH_START =     0x12
    SEARCH_STOP =      0x13
    SEARCH_STATUS =    0x14

    PROCESS_CAPABILITIES =  0x20
    PROCESS_PARAMS =   0x21
    PROCESS_START =    0x22
    PROCESS_STOP =     0x23
    PROCESS_STATUS =   0x24

    UNIT_ERROR =            0x30
    DATA_ERROR =            0x31


    blankPreStruct =                    struct.Struct("!")

    searchCapabilitiesPreStruct =       struct.Struct("!")
    searchParamsPreStruct =             struct.Struct("!")
    searchStartPreStruct =              struct.Struct("!")
    searchStopPreStruct =               struct.Struct("!")
    searchStatusPreStruct =             struct.Struct("!")

    processCapabilitiesPreStruct =      struct.Struct("!")
    processParamsPreStruct =            struct.Struct("!")
    processStartPreStruct =             struct.Struct("!")
    processStopPreStruct =              struct.Struct("!")
    processStatusPreStruct =            struct.Struct("!")

    unitErrorPreStruct =                struct.Struct("!")
    dataErrorPreStruct =                struct.Struct("!")


    blankDatumStruct =                  struct.Struct("!")

    searchCapabilitiesDatumStruct =     struct.Struct("!")
    searchParamsDatumStruct =           struct.Struct("!")
    searchStartDatumStruct =            struct.Struct("!")
    searchStopDatumStruct =             struct.Struct("!")
    searchStatusDatumStruct =           struct.Struct("!")

    processCapabilitiesDatumStruct =    struct.Struct("!")
    processParamsDatumStruct =          struct.Struct("!")
    processStartDatumStruct =           struct.Struct("!")
    processStopDatumStruct =            struct.Struct("!")
    processStatusDatumStruct =          struct.Struct("!")

    unitErrorDatumStruct =              struct.Struct("!")
    dataErrorDatumStruct =              struct.Struct("!")


    unitPreStructs = {BLANK: blankPreStruct,
                      SEARCH_CAPABILITIES: searchCapabilitiesPreStruct,
                      SEARCH_PARAMS: searchParamsPreStruct,
                      SEARCH_START: searchStartPreStruct,
                      SEARCH_STOP: searchStopPreStruct,
                      SEARCH_STATUS: searchStatusPreStruct,
                      PROCESS_CAPABILITIES: processCapabilitiesPreStruct,
                      PROCESS_PARAMS: processParamsPreStruct,
                      PROCESS_START: processStartPreStruct,
                      PROCESS_STOP: processStopPreStruct,
                      PROCESS_STATUS: processStatusPreStruct,
                      UNIT_ERROR: unitErrorPreStruct,
                      DATA_ERROR: dataErrorPreStruct}


    unitDatumStructs = {BLANK: blankDatumStruct,
                        SEARCH_CAPABILITIES: searchCapabilitiesDatumStruct,
                        SEARCH_PARAMS: searchParamsDatumStruct,
                        SEARCH_START: searchStartDatumStruct,
                        SEARCH_STOP: searchStopDatumStruct,
                        SEARCH_STATUS: searchStatusDatumStruct,
                        PROCESS_CAPABILITIES: processCapabilitiesDatumStruct,
                        PROCESS_PARAMS: processParamsDatumStruct,
                        PROCESS_START: processStartDatumStruct,
                        PROCESS_STOP: processStopDatumStruct,
                        PROCESS_STATUS: processStatusDatumStruct,
                        UNIT_ERROR: unitErrorDatumStruct,
                        DATA_ERROR: dataErrorDatumStruct}
