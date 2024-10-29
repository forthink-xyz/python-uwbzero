# -*- coding: utf-8 -*-
"""

@file: CCC Region Params for UWB MAC

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

from enum import IntEnum

class EnumCCCDeviceType(IntEnum):
    CCC_DEVICE_TYPE_CONTROLEE = 0
    CCC_DEVICE_TYPE_CONTROLLER = 1
    CCC_DEVICE_TYPE_DL_TAG = 2


class EnumCCCDeviceRole(IntEnum):
    CCC_DEVICE_ROLE_RESPONDER = 0
    CCC_DEVICE_ROLE_INITIATOR = 1


class EnumCCCStsConfig(IntEnum):
    CCC_STS_CONFIG_STATIC = 0
    CCC_STS_CONFIG_DYNAMIC = 1
    CCC_STS_CONFIG_DYNAMIC_INDIVIDUAL_KEY = 2
    CCC_STS_CONFIG_PROVISIONED = 3
    CCC_STS_CONFIG_PROVISIONED_INDIVIDUAL_KEY = 4


class EnumCCCMacFcsType(IntEnum):
    CCC_MAC_FCS_TYPE_CRC_16 = 0
    CCC_MAC_FCS_TYPE_CRC_32 = 1


class EnumCCCRangeDataNtfConfig(IntEnum):
    CCC_RANGE_DATA_NTF_DISABLED = 0x00
    CCC_RANGE_DATA_NTF_ALWAYS = 0x01
    CCC_RANGE_DATA_NTF_PROXIMITY = 0x02
    CCC_RANGE_DATA_NTF_AOA = 0x03,   # !< used for FIRA , and below
    CCC_RANGE_DATA_NTF_PROXIMITY_AND_AOA = 0x04
    CCC_RANGE_DATA_NTF_PROXIMITY_CROSSING = 0x05
    CCC_RANGE_DATA_NTF_AOA_CROSSING = 0x06
    CCC_RANGE_DATA_NTF_PROXIMITY_AND_AOA_CROSSING = 0x07


class EnumCCCKeyRotation(IntEnum):
    CCC_NO_ROTATION = 0
    CCC_STS_KEY_ROTATION = 1  # only if STS_CONFIG = 0x01
    CCC_dUDSK_ROTATION = 2
    CCC_KEY_dUDSK_ROTATION = 3


class EnumCCCHoppingMode(IntEnum):
    CCC_NO_HOPPING = 0
    # CCC_CONTINUOUS_HOPPING = 1  # not support
    CCC_ADAPTIVE_HOPPING_MODULO = 2
    CCC_CONTINUOUS_HOPPING_MODULO = 3
    CCC_ADAPTIVE_HOPPING_AES = 4
    CCC_CONTINUOUS_HOPPING_AES = 5


class EnumCCCPrfMode(IntEnum):
    CCC_PRF_MODE_BPRF = 0
    CCC_PRF_MODE_HPRF = 1
    CCC_PRF_MODE_HPRF_HIGH_RATE = 2


class EnumCCCPreambuleDuration(IntEnum):
    CCC_PREAMBULE_DURATION_32 = 0
    CCC_PREAMBULE_DURATION_64 = 1


class EnumCCCSfdId(IntEnum):
    CCC_SFD_ID_0 = 0   # @CCC_SFD_ID_0: Delimiter is [0 +1 0 –1 +1 0 0 –1]
    CCC_SFD_ID_1 = 1  # @CCC_SFD_ID_1: Delimiter is [ –1 –1 +1 –1 ]
    # @CCC_SFD_ID_2: Delimiter is [ –1 –1 –1 +1 –1 –1 +1 –1 ]
    CCC_SFD_ID_2 = 2
    # @CCC_SFD_ID_3: Delimiter is [ –1 –1 –1 –1 –1 +1 +1 –1 –1 +1 –1 +1 –1 –1 +1 –1 ]
    CCC_SFD_ID_3 = 3
    # * @CCC_SFD_ID_4: Delimiter is [ –1 –1 –1 –1 –1 –1 –1 +1 –1 –1 +1 –1 –1 +1 –1 +1 –1 +1 –1 –1 –1 +1 +1 –1 –1 –1 +1 –1 +1 +1 –1 –1 ]
    CCC_SFD_ID_4 = 4
    CCC_SFD_ID_RADIO = 0xFF  # NXP NCJ29D5, 0xFF use the radio configuration SFD


class EnumCCCStsSegments(IntEnum):
    CCC_STS_SEGMENTS_0 = 0
    CCC_STS_SEGMENTS_1 = 1
    CCC_STS_SEGMENTS_2 = 2
    CCC_STS_SEGMENTS_3 = 3
    CCC_STS_SEGMENTS_4 = 4


class EnumCCCPsduDataRate(IntEnum):
    CCC_PSDU_DATA_RATE_6M81 = 0
    CCC_PSDU_DATA_RATE_7M80 = 1
    CCC_PSDU_DATA_RATE_27M2 = 2
    CCC_PSDU_DATA_RATE_31M2 = 3


class EnumCCCPhrDataRate(IntEnum):
    CCC_PHR_DATA_RATE_850K = 0
    CCC_PHR_DATA_RATE_6M81 = 1


class EnumCCCRssiReportType(IntEnum):
    CCC_RSSI_REPORT_NONE = 0
    CCC_RSSI_REPORT_MINIMUM = 1
    CCC_RSSI_REPORT_AVERAGE = 2


class EnumCCCRangingStatus(IntEnum):
    CCC_STATUS_RANGING_INTERNAL_ERROR = -1
    CCC_STATUS_RANGING_SUCCESS = 0
    CCC_STATUS_RANGING_TX_FAILED = 1
    CCC_STATUS_RANGING_RX_TIMEOUT = 2
    CCC_STATUS_RANGING_RX_PHY_DEC_FAILED = 3
    CCC_STATUS_RANGING_RX_PHY_TOA_FAILED = 4
    CCC_STATUS_RANGING_RX_PHY_STS_FAILED = 5
    CCC_STATUS_RANGING_RX_MAC_DEC_FAILED = 6
    CCC_STATUS_RANGING_RX_MAC_IE_DEC_FAILED = 7
    CCC_STATUS_RANGING_RX_MAC_IE_MISSING = 8


class EnumCCCMeasurementType(IntEnum):
    CCC_MEASUREMENT_TYPE_RANGE = 0
    CCC_MEASUREMENT_TYPE_AOA = 1
    CCC_MEASUREMENT_TYPE_AOA_AZIMUTH = 2
    CCC_MEASUREMENT_TYPE_AOA_ELEVATION = 3
    CCC_MEASUREMENT_TYPE_AOA_AZIMUTH_ELEVATION = 4


class EnumCCCStsLength(IntEnum):
    CCC_STS_LENGTH_32 = 0
    CCC_STS_LENGTH_64 = 1
    CCC_STS_LENGTH_128 = 2


class EnumCCCPulseshapeCombo(IntEnum):
    CCC_PULSESHAPE_COMBO_0 = 0  # !< 0x0 - 0x0 */
    CCC_PULSESHAPE_COMBO_1 = 1  # !< 0x0 - 0x1 */
    CCC_PULSESHAPE_COMBO_2 = 2     # !< 0x0 - 0x2 */
    CCC_PULSESHAPE_COMBO_10 = 0x10  # !< 0x1 - 0x0 */
    CCC_PULSESHAPE_COMBO_11 = 0x11  # !< 0x1 - 0x1 */
    CCC_PULSESHAPE_COMBO_12 = 0x12  # !< 0x1 - 0x2 */
    CCC_PULSESHAPE_COMBO_20 = 0x20  # !< 0x2 - 0x0 */
    CCC_PULSESHAPE_COMBO_21 = 0x21  # !< 0x2 - 0x1 */
    CCC_PULSESHAPE_COMBO_22 = 0x22  # !< 0x2 - 0x2 */


class EnumCCCResponderListen(IntEnum):
    CCC_RESPONDER_NORMAL = 0
    CCC_RESPONDER_LISTEN = 1
