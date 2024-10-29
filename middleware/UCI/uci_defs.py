# -*- coding: utf-8 -*-
"""

@file: uci definitions

@brief: This file contains the definition from UCI specification

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

from enum import IntEnum
import nxp_crc

## @defgroup Forthink_UCI
# This is forthink UWB Communication Interface Common Class and Functions.
# @{

class EnumUciStatus(IntEnum):
    '''
        UCI Rangging Status Enum, <UCI generic specification 8.5 Table 32>
        usage example:
        status = UciRangingStatus(rcv_data[i])
        if status == UciRangingStatus.UCI_STATUS_OK:
            pass
    '''
    # CORE Generic status codes
    UCI_STATUS_OK = 0x00
    UCI_STATUS_REJECTED = 0x01
    UCI_STATUS_FAILED = 0x02
    UCI_STATUS_SYNTAX_ERROR = 0x03
    UCI_STATUS_INVALID_PARAM = 0x04
    UCI_STATUS_INVALID_RANGE = 0x05
    UCI_STATUS_INVALID_MESSAGE_SIZE = 0x06
    UCI_STATUS_UNKNOWN_GID = 0x07
    UCI_STATUS_UNKNOWN_OID = 0x08
    UCI_STATUS_READ_ONLY = 0x09
    UCI_STATUS_COMMAND_RETRY = 0x0A
    UCI_STATUS_UNKNOWN = 0x0B
    UCI_STATUS_NOT_APPLICABLE = 0x0C

    # UWB session specific status codes
    UCI_STATUS_ERROR_SESSION_NOT_EXIST = 0x11
    UCI_STATUS_ERROR_SESSION_DUPLICATE = 0x12   # session already exist/created
    UCI_STATUS_ERROR_SESSION_ACTIVE = 0x13
    UCI_STATUS_ERROR_MAX_SESSIONS_EXCEEDED = 0x14
    UCI_STATUS_ERROR_SESSION_NOT_CONFIGURED = 0x15
    UCI_STATUS_ERROR_ACTIVE_SESSIONS_ONGOING = 0x16
    UCI_STATUS_ERROR_MULTICAST_LIST_FULL = 0x17
    UCI_STATUS_ERROR_ADDRESS_NOT_FOUND = 0x18
    UCI_STATUS_ERROR_ADDRESS_ALREADY_PRESENT = 0x19
    UCI_STATUS_ERROR_UWB_INITIATION_TIME_TOO_OLD = 0x1A
    UCI_STATUS_OK_NEGATIVE_DISTANCE_REPORT = 0x1B
    UCI_STATUS_INVALID_STS_IDX = 0x1C # <NXP CCC UCI>

    # UWB ranging session specific status codes
    UCI_STATUS_RANGING_TX_FAILED = 0x20
    UCI_STATUS_RANGING_RX_TIMEOUT = 0x21
    UCI_STATUS_RANGING_RX_PHY_DEC_FAILED = 0x22
    UCI_STATUS_RANGING_RX_PHY_TOA_FAILED = 0x23
    UCI_STATUS_RANGING_RX_PHY_STS_FAILED = 0x24
    UCI_STATUS_RANGING_RX_MAC_DEC_FAILED = 0x25
    UCI_STATUS_RANGING_RX_MAC_IE_DEC_FAILED = 0x26
    UCI_STATUS_RANGING_RX_MAC_IE_MISSING = 0x27

    # Vendor specific status codes
    UCI_STATUS_INVALID_RESPONDER_SLOT_INDEX = 0xA0
    ## Forthink Vendor specific status codes
    UCI_STATUS_LICENSE_NEED = 0xA1
    UCI_STATUS_LICENSE_VERIFIED_FAILED = 0xA2
    UCI_STATUS_INVALID_PUBLIC_KEY = 0xA3
    UCI_STATUS_SN_TOO_LONG = 0xA4
    # UCI_STATUS_SLOT_LEN_NOT_SUPPORTED = 0xA1
    # UCI_STATUS_INVALID_SLOT_PER_RR = 0xA2
    # UCI_STATUS_INVALID_STS_IDX = 0xA3
    # UCI_STATUS_RESPONDER_LISTEN_ONLY_MODE = 0xA4

    # Proprietary status codes
    UCI_STATUS_RANGING_CONSISTENCY_CHECK_FAILED = 0xE1

    # NXP Testware status codes
    UCI_STATUS_VERIFICATION_FAILED = 0x7D
    UCI_STATUS_REBOOT = 0x80
    UCI_STATUS_REBOOT_WDT = 0x81
    UCI_STATUS_CRC_ERROR = 0xF8
    UCI_STATUS_NOT_IMPLEMENTED = 0xFE
    UCI_STATUS_UNDEF = 0xFF


class EnumDeviceState(IntEnum):
    '''
        Device State Values, FiRa Consortium UCI Generic Specification Table 10
    '''
    DEVICE_STATE_RFU = 0x00
    DEVICE_STATE_READY = 0x01
    DEVICE_STATE_ACTIVE = 0x02
    DEVICE_STATE_ERROR = 0xFF


class EnumUciMessageType(IntEnum):
    '''
        UCI Message Type
    '''
    UCI_MT_COMMAND = 0x01
    UCI_MT_RESPONSE = 0x02
    UCI_MT_NOTIFICATION = 0x03
    UCI_MT_UNDEF = 0xFF


class EnumUciGid(IntEnum):
    '''
        UCI GID
    '''
    CORE_GENERIC_GID = 0x00
    UWB_SESSION_GID = 0x01
    UWB_RANGE_GID = 0x02
    FORTHINK_VENDOR_GID = 0x0A
    VENDOR_B_GID = 0x0B
    VENDOR_C_GID = 0x0C
    RF_TEST_GID = 0x0D
    VENDOR_E_GID = 0x0E
    VENDOR_F_GID = 0x0F


class EnumCoreGenericOid(IntEnum):
    '''
        UCI Core Group-0: Opcodes
    '''
    CORE_DEVICE_RESET_OID = 0x00
    CORE_DEVICE_STATUS_NTF_OID = 0x01
    CORE_DEVICE_INFO_OID = 0x02
    CORE_GET_CAPS_INFO_OID = 0x03
    CORE_SET_CONFIG_OID = 0x04
    CORE_GET_CONFIG_OID = 0x05
    CORE_DEVICE_SUSPEND = 0x06
    CORE_GENERIC_ERROR_NTF_OID = 0x07


class EnumUwbSessionOid(IntEnum):
    '''
        UCI UWB Session Group-1: opcodes
    '''
    SESSION_INIT_OID = 0x00
    SESSION_DEINIT_OID = 0x01
    SESSION_STATUS_NTF_OID = 0x02
    SESSION_SET_APP_CONFIG_OID = 0x03
    SESSION_GET_APP_CONFIG_OID = 0x04
    SESSION_GET_COUNT_OID = 0x05
    SESSION_GET_STATE_OID = 0x06
    SESSION_UPDATE_CONTROLLER_MULTICAST_LIST_OID = 0x07
    SESSION_GET_POSSIBLE_RAN_MULTIPLIER_VALUE_OID = 0x20


class EnumUwbRangeOid(IntEnum):
    '''
        UCI UWB RANGE Group-2: opcodes
    '''
    RANGE_START_OID = 0x00
    RANGE_STOP_OID = 0x01
    RANGE_CTRL_REQ_OID = 0x02
    RANGE_GET_RANGING_COUNT_OID = 0x03
    RANGE_CCC_DATA_NTF_OID = 0x20
    RANGE_RESUME_OID = 0x21
    RANGE_CCC_DATA_NTF_EXP_OID = 0x23
    RANGE_CCC_DATA_NTF_TAG_OID = 0x24


class EnumTestOid(IntEnum):
    '''
        UCI RF TEST Group-0x0D: opcodes
    '''
    TEST_CONFIG_SET_OID = 0x00
    TEST_CONFIG_GET_OID = 0x01
    TEST_PERIODIC_TX_OID = 0x02
    TEST_PER_RX_OID = 0x03
    TEST_RFU_OID = 0x04
    TEST_RX_OID = 0x05
    TEST_LOOPBACK_OID = 0x06
    TEST_STOP_SESSION_OID = 0x07
    TEST_SS_TWR_OID = 0x08

class EnumForthinkVendorOid(IntEnum):
    '''
        Forthink Vendor Group-0x0A: opcodes
    '''
    CCC_DATA_SET_OID = 0x20
    ENCRYPT_GET_SERIAL_NUM_OID = 0x30
    ENCRYPT_LICENSE_CHECK_OID = 0x31

class EnumVendorEOid(IntEnum):
    '''
        Vendor E Group-0x0E: opcodes
    '''
    VENDOR_E_SET_TRIM_VALUE = 0x26
    

## @defgroup Forthink_UCI_Group_Core
# This is forthink UWB Communication Interface Core Group.
# @{
    
# CORE_GENERIC_ERROR_NTF
class EnumGenericError(IntEnum):
    STATUS_SYNTAX_ERROR = 0x03
    STATUS_INVALID_MESSAGE_SIZE = 0x06
    STATUS_CRC_ERROR = 0xF8

class EnumCoreDeviceConfigID(IntEnum):
    PARAM_ID_DEVICE_STATE = 0x00
    PARAM_ID_LOW_POWER_MODE = 0x01

class EnumCoreCapsInfoID(IntEnum):
    CAP_ID_SLOT_BITMASK = 0xA0
    CAP_ID_SYNC_CODE_IDX_BITMASK = 0xA1
    CAP_ID_HOPPING_CONFIG_BITMASK = 0xA2
    CAP_ID_CHAN_BITMASK = 0xA3
    CAP_ID_SUPPORTED_PROTOCOL_VERSION = 0xA4
    CAP_ID_SUPPORTED_UWB_CONFIG_ID = 0xA5
    CAP_ID_SUPPORTED_PULSESHAPE_COMBO = 0xA6
    CAP_ID_MAX_PAYLOAD_LEN = 0xE3
    CAP_ID_MIN_SLOT_LEN = 0xE4
    CAP_ID_MAX_SESSION_NUM = 0xE5
    CAP_ID_MAX_ANCHOR_NUM = 0xE6
    CAP_ID_MIN_UWB_FREQ = 0xE7
    CAP_ID_MAX_UWB_FREQ = 0xE8
    CAP_ID_SUPPORT_ROLE_PROTOCOL = 0xE9


# @}

## @defgroup Forthink_UCI_Group_Session
# This is forthink UWB Communication Interface Session Group.
# @{
    
# UWB_SESSION Specific Status codes
class EnumSessionStatus(IntEnum):
    STATUS_SESSION_NOT_EXIST = 0x11
    STATUS_SESSION_DUPLICATE = 0x12
    STATUS_SESSION_ACTIVE = 0x13
    STATUS_MAX_SESSIONS_EXCEEDED = 0x14
    STATUS_SESSION_NOT_CONFIGURED = 0x15

# UWB RANGE Session Specific Status codes

class EnumRangingStatus(IntEnum):
    STATUS_RANGING_TX_FAILED = 0x20
    STATUS_RANGING_RX_TIMEOUT = 0x21
    STATUS_RANGING_RX_PHY_DEC_FAILED = 0x22
    STATUS_RANGING_RX_PHY_TOA_FAILED = 0x23
    STATUS_RANGING_RX_PHY_STS_FAILED = 0x24
    STATUS_RANGING_RX_MAC_DEC_FAILED = 0x25
    STATUS_RANGING_RX_MAC_IE_DEC_FAILED = 0x26
    STATUS_RANGING_RX_MAC_IE_MISSING = 0x27
    STATUS_ERROR_ROUND_INDEX_NOT_ACTIVATED = 0x28
    STATUS_ERROR_NUMBER_OF_ACTIVE_RANGING_ROUNDS_EXCEEDED = 0x29
    STATUS_ERROR_ROUND_INDEX_NOT_SET_AS_INITIATOR = 0x2A
    STATUS_ERROR_DL_TDOA_DEVICE_ADDRESS_NOT_MATCHING_IN_REPLY_TIME_LIST = 0x2B

# UWB SESSION SET_APP_CONFIG Parameter IDS

class EnumSessionAppConfigID(IntEnum):
    PARAM_ID_DEVICE_TYPE = 0x00
    PARAM_ID_RANGING_METHOD = 0x01
    PARAM_ID_STS_CONFIG = 0x02
    PARAM_ID_MULTI_NODE_MODE = 0x03
    PARAM_ID_CHANNEL_NUMBER = 0x04
    PARAM_ID_NO_OF_CONTROLEE = 0x05
    PARAM_ID_DEVICE_MAC_ADDRESS = 0x06
    PARAM_ID_DST_MAC_ADDRESS = 0x07
    PARAM_ID_SLOT_DURATION = 0x08
    PARAM_ID_RANGING_INTERVAL = 0x09
    PARAM_ID_STS_INDEX = 0x0A
    PARAM_ID_MAC_FCS_TYPE = 0x0B
    PARAM_ID_RANGING_ROUND_CONTROL = 0x0C
    PARAM_ID_AOA_RESULT_REQ = 0x0D
    PARAM_ID_RNG_DATA_NTF = 0x0E
    PARAM_ID_RNG_DATA_NTF_PROXIMITY_NEAR = 0x0F
    PARAM_ID_RNG_DATA_NTF_PROXIMITY_FAR = 0x10
    PARAM_ID_DEVICE_ROLE = 0x11
    PARAM_ID_RFRAME_CONFIG = 0x12
    PARAM_ID_RX_MODE = 0x13
    PARAM_ID_PREAMBLE_CODE_INDEX = 0x14
    PARAM_ID_SFD_ID = 0x15
    PARAM_ID_PSDU_DATA_RATE = 0x16
    PARAM_ID_PREAMBLE_DURATION = 0x17
    PARAM_ID_ANTENNA_PAIR_SELECTION = 0x18
    PARAM_ID_MAC_CFG = 0x19
    PARAM_ID_RANGING_TIME_STRUCT = 0x1A
    PARAM_ID_SLOTS_PER_RR = 0x1B
    PARAM_ID_TX_ADAPTIVE_PAYLOAD_POWER = 0x1C
    PARAM_ID_TX_ANTENNA_SELECTION = 0x1D
    PARAM_ID_RESPONDER_SLOT_INDEX = 0x1E
    PARAM_ID_PRF_MODE = 0x1F
    PARAM_ID_MAX_CONTENTION_PHASE_LEN = 0x20
    PARAM_ID_CONTENTION_PHASE_UPDATE_LEN = 0x21
    PARAM_ID_SCHEDULED_MODE = 0x22
    PARAM_ID_KEY_ROTATION = 0x23
    PARAM_ID_KEY_ROTATION_RATE = 0x24
    PARAM_ID_SESSION_PRIORITY = 0x25
    PARAM_ID_MAC_ADDRESS_MODE = 0x26
    PARAM_ID_VENDOR_ID = 0x27
    PARAM_ID_STATIC_STS_IV = 0x28
    PARAM_ID_NUMBER_OF_STS_SEGMENTS = 0x29
    PARAM_ID_MAX_RR_RETRY = 0x2A
    PARAM_ID_UWB_INITIATION_TIME = 0x2B
    PARAM_ID_RANGING_ROUND_HOPPING = 0x2C
    # ------------- FIRA specific parameters ------------------#
    PARAM_ID_BLOCK_STRIDE_LENGTH = 0x2D
    PARAM_ID_RESULT_REPORT_CONFIG = 0x2E
    PARAM_ID_IN_BAND_TERMINATION_ATTEMPT_COUNT = 0x2F
    PARAM_ID_SUB_SESSION_ID = 0x30
    PARAM_ID_BPRF_PHR_DATA_RATE = 0x31
    PARAM_ID_MAX_NUM_OF_MEASUREMENTS= 0x32
    PARAM_ID_STS_LENGTH = 0x35
    ############################################################
    PARAM_ID_SUSPEND_RANGING_ROUNDS = 0x36
    PARAM_ID_SESSION_KEY = 0x45
    PARAM_ID_SUB_SESSION_KEY = 0x46
    # ------------- CCC specific parameters ------------------#
    PARAM_ID_HOP_MODE_KEY = 0xA0
    PARAM_ID_CCC_CONFIG_QUIRKS = 0xA1
    PARAM_ID_RANGING_PROTOCOL_VER = 0xA3
    PARAM_ID_UWB_CONFIG_ID = 0xA4
    PARAM_ID_PULSE_SHAPE_COMBO = 0xA5
    PARAM_ID_URSK_TTL = 0xA6
    PARAM_ID_RESPONDER_LISTEN_ONLY = 0xA7
    PARAM_ID_LAST_STS_INDEX_USED = 0xA8
    # ------- Proprietary APP Configuration parameters -------#
    PRRAM_ID_RX_START_MARGIN = 0xE3
    PARAM_ID_RX_TIMEOUT = 0xE4
    PARAM_ID_ADAPTED_RANGING_INDEX = 0xE5
    PARAM_ID_NBIC_CONF = 0xE6
    PARAM_ID_GROUPDELAY_RECALC_ENA = 0xE7  # 1: Group Delay Recalculation at the start of the session
    PARAM_ID_URSK_SecSessionKey = 0xE8     # CCC : URSK, 33 Bytes; FiRa : 17 Bytes, secSessionKey
    PARAM_ID_STATIC_KEYS = 0xE9            # CCC oonly
    PARAM_ID_RCM_RX_MARGIN_TIME = 0xEA
    PARAM_ID_RCM_RX_TIMEOUT = 0xEB
    PARAM_ID_DYNAMIC_PRIORITY_IN_SYNCH = 0xEC
    PARAM_ID_TX_POWER_TEMP_COMPENSATION = 0xED
    PARAM_ID_LONG_SRC_ADDRESS = 0xEF
    PARAM_ID_KDF_CASCADE = 0xF0  # used to calculate dURSK and dUDSK
    PARAM_ID_RR_RETRY_THR = 0xF1
    PARAM_ID_TX_POWER_ID = 0xF2
    PARAM_ID_RX_PHY_LOGGING_ENBL = 0xF4
    PARAM_ID_TX_PHY_LOGGING_ENBL = 0xF5
    PARAM_ID_LOG_PARAMS_CONF = 0xF6
    PARAM_ID_CIR_TAP_OFFSET = 0xF7
    PARAM_ID_CIR_NUM_TAPS = 0xF8
    PARAM_ID_STS_INDEX_RESTART = 0xF9
    PARAM_ID_VENDOR_SPECIFIC_OUI = 0xFA
    PARAM_ID_RADIO_CFG_IDXS = 0xFB
    PARAM_ID_CRYPTO_KEY_USAGE_FLAG = 0xFD
    PARAM_ID_SEND_FINAL_ALWAYS = 0xFE
    


class EnumRangingSlotLength(IntEnum):
    RANGING_SLOT_LENGTH_1MS = 1200
    RANGING_SLOT_LENGTH_1_3MS = 1600
    RANGING_SLOT_LENGTH_2MS = 2400
    RANGING_SLOT_LENGTH_2_6MS = 3200
    RANGING_SLOT_LENGTH_3MS = 3600
    RANGING_SLOT_LENGTH_4MS = 4800
    RANGING_SLOT_LENGTH_8MS = 9600

class EnumSessionType(IntEnum):
    SESSION_TYPE_FIRA_RANGING = 0x00
    SESSION_TYPE_CCC_RANGING = 0xA0
    SESSION_TYPE_DEVICE_TEST = 0xD0
    
class EnumSessionState(IntEnum):
    SESSION_STATE_INIT = 0x00
    SESSION_STATE_DEINIT = 0x01
    SESSION_STATE_ACTIVE = 0x02
    SESSION_STATE_IDLE = 0x03
    SESSION_UNKNOWN = 0xFF
    
class EnumSessionStateChangeReason(IntEnum):
    STATE_CHANGE_WITH_SESSION_MANAGEMENT_CMD = 0x00
    MAX_RANGING_ROUND_RETRY_COUNT_REACHED = 0x01
    MAX_NUMBER_OF_MEAUREMENTS_REACHED = 0x02    # MAX_RANGING_BLOCKS_REACHED
    ERR_URSK_EXPIRED = 0x03                     # NXP-MAC All in One, NCJ29D5
    ERR_TERMINATION_ON_MAX_STS = 0x04           # NXP All in One
    ERR_SLOT_LENGTH_NOT_SUPPORTED = 0x20        # FiRa Consortium, UCI Generic Specification
    ERR_INSUFFICIENT_SLOTS_PER_RR = 0x21
    ERR_MAC_ADDR_MODE_NOT_SUPPORTED = 0x22
    ERR_INVALID_RANGING_INTERVAL = 0x23
    ERR_INVALID_STS_CONFIG = 0x24
    ERR_INVALID_RFRAME_CONFIG = 0x25

class EnumMulticastUpdateStatus(IntEnum):
    STATUS_OK_MULTICAST_LIST_UPDATE = 0x00
    STATUS_ERROR_MULTICAST_LIST_FULL = 0x01
    STATUS_ERROR_KEY_FETCH_FAIL = 0x02
    STATUS_ERROR_SUB_SESSION_ID_NOT_FOUND = 0x03

# @}  

## @defgroup Forthink_UCI_RF_Test_Group
# This is forthink UWB Communication Interface RF Test Group.
# @{
    
class EnumTestConfigID(IntEnum): 
    PARAM_ID_NUM_PACKETS = 0x00
    PARAM_ID_T_GAP = 0x01  # !< Gap between start of one packet to the next, in us, default 2000
    PARAM_ID_T_START = 0x02  # !< max time from the start of T_GAP to SFD found state in us, default 450 us
    PARAM_ID_T_WIN  = 0x03  # !< max time which RX is looking for a packet from the start of T_GAP in us, T_WIN > T_START, default 750 us
    PARAM_ID_RANDOM_PSDU = 0x04
    PARAM_ID_PHR_RANGING_BIT = 0x05
    PARAM_ID_RMARKER_TX_START = 0x06
    PARAM_ID_RMARKER_RX_START = 0x07
    STS_INDEX_AUTO_INCR = 0x08
    
# @}  

## @defgroup Forthink_UCI_Vender_defined_Group
# This is forthink UWB Communication Interface Forthink Vendor-defined Group.
# @{


# @}  
class InvalidFormatError(Exception):
    def __init__(self, input: str = ""):
        message = "Error, invalid format! " + input
        super().__init__(message)

class UciMessage:
    def __init__(self, message_type: EnumUciMessageType, packet_boundary_flag: int, gid: int, payload_extension: int, oid: int, payload_length: int, payload: list[int], uci_packets: list = None, response_status: EnumUciStatus = None):
        self.message_type = message_type
        self.packet_boundary_flag = packet_boundary_flag
        self.gid = gid
        self.payload_extension = payload_extension
        self.oid = oid
        self.payload_length = payload_length
        self.response_status = response_status
        self.payload = payload
        self.uci_packets = uci_packets
        self.to_byte_stream()

    @classmethod
    def from_bytes(cls, bytes: list[int], remove_crc: bool = False, prior_pbf: bool = False):
        uci_packets = [bytes]
        bytes = bytes[:-2] if remove_crc == True else bytes
        if len(bytes) >= 4:
            message_type = EnumUciMessageType.UCI_MT_UNDEF
            try:
                message_type = EnumUciMessageType(((bytes[0] & 0xe0) >> 5))
            except ValueError as e:
                print("unsupported message type, ValueError: ", e)
            packet_boundary_flag = (bytes[0] & 0x10) >> 4
            gid = bytes[0] & 0x0f
            payload_extension = ((bytes[1] & 0x80) >> 7)
            oid = bytes[1] & 0x3f
            payload_length = bytes[3] + (bytes[2] << 8)
            response_status = None
            # check if a status field is required in case it is a response
            if message_type == EnumUciMessageType.UCI_MT_RESPONSE and prior_pbf == False:
                response_status = EnumUciStatus(bytes[4] & 0xFF)
                payload = bytes[4:]
                # if len(bytes) >= 5:
                #     response_status = EnumUciStatus(bytes[4] & 0xFF)
                #     payload = bytes[5:]
                # else:
                #     raise InvalidFormatError("UCI response status missing!")
            else:
                payload = bytes[4:]
        else:
            raise InvalidFormatError("UCI Input message too short!")
        
        return UciMessage(message_type=message_type,
                          packet_boundary_flag=packet_boundary_flag,
                          gid=gid,
                          payload_extension=payload_extension,
                          oid=oid,
                          payload_length=payload_length,
                          payload=payload,
                          uci_packets=uci_packets,
                          response_status=response_status)

    def __str__(self):
        return "message type: " + str(self.message_type.name) + " (" + str("0x{:02x}".format(self.message_type.value)) + ")\n" \
            + "packet boundary flag: " + str(self.packet_boundary_flag) + "\n" \
            + "gid: " + str("0x{:02x}".format(self.gid)) + "\n" \
            + "payload extension: " + str(self.payload_extension) + "\n" \
            + "oid: " + str("0x{:02x}".format(self.oid)) + "\n" \
            + "payload length: " + str(self.payload_length) + " bytes (" + str("0x{:02x}".format(self.payload_length)) + ")\n" \
            + "payload: " + str(["0x{:02x}".format(x) for x in self.payload])

    def to_byte_stream(self, append_crc=False):
        self.byte_stream: list[int] = []
        # assemble the byte stream
        self.byte_stream.append(self.message_type.value <<
                                5 | self.packet_boundary_flag << 4 | self.gid)
        self.byte_stream.append(self.payload_extension << 7 | self.oid)
        # check for extended payload size
        if (self.payload_extension > 0):
            self.byte_stream.append((self.payload_length & 0xFF00) >> 8)
        else:
            self.byte_stream.append(0)
        self.byte_stream.append(self.payload_length & 0x00FF)
        if self.response_status is not None:
            self.byte_stream.append(self.response_status.value & 0xFF)
        self.byte_stream += self.payload
        if append_crc:
            crc: int = nxp_crc.calculate_crc(frame=self.byte_stream)
            self.byte_stream += crc.to_bytes(2, 'little')
        return self.byte_stream


class UciConfigTLV:

    def __init__(self, tag: int, length: int, value: list[int]):
        self.tag = tag
        self.length = length
        self.value = value

    def __eq__(self, value: object) -> bool:
        '''
            tlv1 = UciConfigTLV(0x01, 0x02, [0x03, 0x04])
            tlv2 = UciConfigTLV(0x01, 0x02, [0x03, 0x04])
            print(tlv1 == tlv2) # True
        '''
        if(isinstance(value, UciConfigTLV)):
            return self.tag == value.tag and self.length == value.length and self.value == value.value
        else:
            return False

    @classmethod
    def from_bytes(cls, byte_stream: list[int], is_support_extension=False):
        tag = 0
        length = 0
        value = []
        if len(byte_stream) > 2:
            if not is_support_extension:
                tag = byte_stream[0]
                length = byte_stream[1]
                value = byte_stream[2:2+length]
            else:
                # check if the Extension Tag ID, if the tag is 0xE0-0xE4, the tag is 2 bytes
                if (tag==0xE0 or tag==0xE1 or tag==0xE2 or tag==0xE3 or tag == 0xE4) and (len(byte_stream) > 3):
                    tag = byte_stream[1] * 256 + byte_stream[0]
                    length = byte_stream[2]
                    value = byte_stream[3:3+length]
                else:
                    tag = byte_stream[0]
                    length = byte_stream[1]
                    value = byte_stream[2:2+length]


        return UciConfigTLV(tag, length, value)
    
    def to_byte_stream(self):
        # Extension ID
        if self.tag > 0xFF:
            return [self.tag & 0xFF, (self.tag >> 8) & 0xFF, self.length] + self.value
        return [self.tag, self.length] + self.value
    
    def __str__(self):
        return "Tag: " + str("0x{:02x}".format(self.tag)) + " " + EnumSessionAppConfigID(self.tag).name + " Len: " + str(self.length) + " Value: " + str(["0x{:02x}".format(x) for x in self.value])
    

class UciRspNtfResult:
    
    def __init__(self, message_type: EnumUciMessageType, gid: int, oid: int, response_status: EnumUciStatus, result = None):
        self.message_type = message_type
        self.gid = gid
        self.oid = oid
        self.status = response_status
        self.uci_result = result
        
    def __str__(self) -> str:
        return "message type: " + str(self.message_type.name) + " (" + str("0x{:02x}".format(self.message_type.value)) + ")\n" \
            + "gid: " + str("0x{:02x}".format(self.gid)) + "\n" \
            + "oid: " + str("0x{:02x}".format(self.oid)) + "\n" \
            + "status: " + str(self.status.name) + " (" + str("0x{:02x}".format(self.status.value)) + ")\n" \
            + "payload: " + str(self.uci_result)

# @}

