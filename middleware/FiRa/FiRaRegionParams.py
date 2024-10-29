# -*- coding: utf-8 -*-
"""

@file: FiRa Region Params for UWB MAC

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

from enum import IntEnum


class EnumFiraDeviceType(IntEnum):
    FIRA_DEVICE_TYPE_CONTROLEE = 0
    FIRA_DEVICE_TYPE_CONTROLLER = 1


class EnumFiraDeviceRole(IntEnum):
    FIRA_DEVICE_ROLE_RESPONDER = 0
    FIRA_DEVICE_ROLE_INITIATOR = 1


class EnumFiraRangingRoundUsage(IntEnum):
    FIRA_RANGING_ROUND_USAGE_OWR = 0
    FIRA_RANGING_ROUND_USAGE_SSTWR = 1
    FIRA_RANGING_ROUND_USAGE_DSTWR = 2


class EnumFiraMultiNodeMode(IntEnum):
    FIRA_MULTI_NODE_MODE_UNICAST = 0
    FIRA_MULTI_NODE_MODE_ONE_TO_MANY = 1
    FIRA_MULTI_NODE_MODE_MANY_TO_MANY = 2


class EnumFiraMeasurementReport(IntEnum):
    FIRA_MEASUREMENT_REPORT_AT_RESPONDER = 0
    FIRA_MEASUREMENT_REPORT_AT_INITIATOR = 1


class EnumFiraEmbeddedMode(IntEnum):
    # Ranging messages do not embed control message, SP0 + SP3
    FIRA_EMBEDDED_MODE_DEFERRED = 0
    # Ranging messages embed control messages, SP1
    FIRA_EMBEDDED_MODE_NON_DEFERRED = 1


class EnumFiraRframeConfig(IntEnum):
    FIRA_RFRAME_CONFIG_SP0 = 0
    FIRA_RFRAME_CONFIG_SP1 = 1
    FIRA_RFRAME_CONFIG_SP2 = 2
    FIRA_RFRAME_CONFIG_SP3 = 3


class EnumFiraPrfMode(IntEnum):
    FIRA_PRF_MODE_BPRF = 0
    FIRA_PRF_MODE_HPRF = 1
    FIRA_PRF_MODE_HPRF_HIGH_RATE = 2


class EnumFiraPreambuleDuration(IntEnum):
    FIRA_PREAMBULE_DURATION_32 = 0
    FIRA_PREAMBULE_DURATION_64 = 1


class EnumFiraSfdId(IntEnum):
    FIRA_SFD_ID_0 = 0   # @FIRA_SFD_ID_0: Delimiter is [0 +1 0 –1 +1 0 0 –1]
    FIRA_SFD_ID_1 = 1  # @FIRA_SFD_ID_1: Delimiter is [ –1 –1 +1 –1 ]
    # @FIRA_SFD_ID_2: Delimiter is [ –1 –1 –1 +1 –1 –1 +1 –1 ]
    FIRA_SFD_ID_2 = 2
    # @FIRA_SFD_ID_3: Delimiter is [ –1 –1 –1 –1 –1 +1 +1 –1 –1 +1 –1 +1 –1 –1 +1 –1 ]
    FIRA_SFD_ID_3 = 3
    # * @FIRA_SFD_ID_4: Delimiter is [ –1 –1 –1 –1 –1 –1 –1 +1 –1 –1 +1 –1 –1 +1 –1 +1 –1 +1 –1 –1 –1 +1 +1 –1 –1 –1 +1 –1 +1 +1 –1 –1 ]
    FIRA_SFD_ID_4 = 4


class EnumFiraRangingRoundUsage(IntEnum):
    FIRA_OWR_UL_TDOA = 0  # !< One Way Ranging Uplink TDOA
    FIRA_SS_TWR_DEFERRED = 1  # !< Single Sided Two Way Ranging Deferred
    FIRA_DS_TWR_DEFERRED = 2  # !< Double Sided Two Way Ranging Deferred
    FIRA_SS_TWR_NON_DEFERRED = 3  # !< Single Sided Two Way Ranging Non-Deferred
    FIRA_DS_TWR_NON_DEFERRED = 4  # !< Double Sided Two Way Ranging Non-Deferred
    FIRA_OWR_AOA = 5  # !< One Way Ranging, Angle of Arrival
    FIRA_OWR_DL_TDOA = 6  # !< One Way Ranging Downlink TDOA
    FIRA_DATA_TRANSFER_PHASE = 7  # !< Data Transfer Phase


class EnumFiraStsSegments(IntEnum):
    FIRA_STS_SEGMENTS_0 = 0
    FIRA_STS_SEGMENTS_1 = 1
    FIRA_STS_SEGMENTS_2 = 2
    FIRA_STS_SEGMENTS_3 = 3
    FIRA_STS_SEGMENTS_4 = 4


class EnumFiraPsduDataRate(IntEnum):
    FIRA_PSDU_DATA_RATE_6M81 = 0
    FIRA_PSDU_DATA_RATE_7M80 = 1
    FIRA_PSDU_DATA_RATE_27M2 = 2
    FIRA_PSDU_DATA_RATE_31M2 = 3
    FIRA_PSDU_DATA_RATE_850K = 4


class EnumFiraPhrDataRate(IntEnum):
    FIRA_PHR_DATA_RATE_850K = 0
    FIRA_PHR_DATA_RATE_6M81 = 1


class EnumFiraMacFcsType(IntEnum):
    FIRA_MAC_FCS_TYPE_CRC_16 = 0
    FIRA_MAC_FCS_TYPE_CRC_32 = 1

class EnumFiraAoAResultReq(IntEnum):
    FIRA_AOA_DISABLE = 0
    FIRA_AOA_ENABLE = 1

class EnumFiraRangeDataNtfConfig(IntEnum):
    FIRA_RANGE_DATA_NTF_DISABLED = 0x00
    FIRA_RANGE_DATA_NTF_ALWAYS = 0x01
    FIRA_RANGE_DATA_NTF_PROXIMITY = 0x02
    FIRA_RANGE_DATA_NTF_AOA = 0x03,   # !< used for FIRA , and below
    FIRA_RANGE_DATA_NTF_PROXIMITY_AND_AOA = 0x04
    FIRA_RANGE_DATA_NTF_PROXIMITY_CROSSING = 0x05
    FIRA_RANGE_DATA_NTF_AOA_CROSSING = 0x06
    FIRA_RANGE_DATA_NTF_PROXIMITY_AND_AOA_CROSSING = 0x07


class EnumFiraRssiReportType(IntEnum):
    FIRA_RSSI_REPORT_NONE = 0
    FIRA_RSSI_REPORT_MINIMUM = 1
    FIRA_RSSI_REPORT_AVERAGE = 2


class EnumFiraStsConfig(IntEnum):
    FIRA_STS_CONFIG_STATIC = 0
    FIRA_STS_CONFIG_DYNAMIC = 1
    FIRA_STS_CONFIG_DYNAMIC_INDIVIDUAL_KEY = 2
    FIRA_STS_CONFIG_PROVISIONED = 3
    FIRA_STS_CONFIG_PROVISIONED_INDIVIDUAL_KEY = 4


class EnumFiraRangingStatus(IntEnum):
    FIRA_STATUS_RANGING_INTERNAL_ERROR = -1
    FIRA_STATUS_RANGING_SUCCESS = 0
    FIRA_STATUS_RANGING_TX_FAILED = 1
    FIRA_STATUS_RANGING_RX_TIMEOUT = 2
    FIRA_STATUS_RANGING_RX_PHY_DEC_FAILED = 3
    FIRA_STATUS_RANGING_RX_PHY_TOA_FAILED = 4
    FIRA_STATUS_RANGING_RX_PHY_STS_FAILED = 5
    FIRA_STATUS_RANGING_RX_MAC_DEC_FAILED = 6
    FIRA_STATUS_RANGING_RX_MAC_IE_DEC_FAILED = 7
    FIRA_STATUS_RANGING_RX_MAC_IE_MISSING = 8


class EnumFiraMeasurementType(IntEnum):
    FIRA_MEASUREMENT_TYPE_RANGE = 0
    FIRA_MEASUREMENT_TYPE_AOA = 1
    FIRA_MEASUREMENT_TYPE_AOA_AZIMUTH = 2
    FIRA_MEASUREMENT_TYPE_AOA_ELEVATION = 3
    FIRA_MEASUREMENT_TYPE_AOA_AZIMUTH_ELEVATION = 4


class EnumFiraStsLength(IntEnum):
    FIRA_STS_LENGTH_32 = 0
    FIRA_STS_LENGTH_64 = 1
    FIRA_STS_LENGTH_128 = 2


class EnumFiraKeyRotation(IntEnum):
    FIRA_NO_ROTATION = 0
    FIRA_STS_KEY_ROTATION = 1  # only if STS_CONFIG = 0x01
    FIRA_dUDSK_ROTATION = 2
    FIRA_KEY_dUDSK_ROTATION = 3

class EnumFiraMacAddrMode(IntEnum):
    FIRA_MAC_ADDR_MODE_SHORT_SHORT = 0
    FIRA_MAC_ADDR_MODE_LONG_SHORT = 1  # not supporrted , 2 Bytes in MAC Header
    FIRA_MAC_ADDR_MODE_LONG_LONG = 2
    
class EnumFiraHoppingMode(IntEnum):
    FIRA_HOPPING_DISABLE = 0
    FIRA_HOPPING_ENABLE = 1
    
    