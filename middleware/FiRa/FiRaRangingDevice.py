# -*- coding: utf-8 -*-
"""

@file: fira ranging device Class

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

import struct

from console_helper import *
from uci_message import *
from uci_defs import *
from uci_layer import UCILayer
from FiRaRegionParams import *
from uci_fira_range_ntf import *

class FiRaSessionParam():
    '''
        FiRa Ranging Session Parameters, used to configure a FiRa ranging session
    '''
    def __init__(self, session_id, device_type: int, device_role: int, device_addr: int, ranging_roound_usage=EnumFiraRangingRoundUsage.FIRA_DS_TWR_DEFERRED.value, anchor_num=1, sts_config=0, multi_node_mode=1, sts_index0=0, ranging_interval=200, slot_length=EnumRangingSlotLength.RANGING_SLOT_LENGTH_2MS.value,
                 slots_per_rr=25, channel_id=9, preamble_id=10, sfd_id=2, responder_slot_idx=1, session_state: UWBSessionState = None):
        self.session_id = session_id
        self.session_state = session_state
        # Session Parameters
        self.device_type = device_type
        self.ranging_round_usage = ranging_roound_usage
        self.sts_config = sts_config
        self.channel_id = channel_id
        self.anchor_num = anchor_num
        self.multi_node_mode = multi_node_mode
        self.device_mac_addr = device_addr
        # Initiator ：list of device mac addresss; Responder: Initiator's mac address
        self.dst_mac_addr = []
        self.ranging_slot_length = slot_length
        self.ranging_interval = ranging_interval
        self.sts_index0 = sts_index0
        self.mac_fcs_type = EnumFiraMacFcsType.FIRA_MAC_FCS_TYPE_CRC_16.value
        self.ranging_round_control = 0x03
        # TAG-ID: 0xD, NCJ29D5 not Support. do not config for NCJ29D5
        self.aoa_result_req = EnumFiraAoAResultReq.FIRA_AOA_DISABLE.value
        self.rng_data_ntf = EnumFiraRangeDataNtfConfig.FIRA_RANGE_DATA_NTF_ALWAYS.value
        self.rng_data_ntf_proximity_near = 0
        self.rng_data_ntf_proximity_far = 20000
        self.device_role = device_role
        self.rframe_config = EnumFiraRframeConfig.FIRA_RFRAME_CONFIG_SP3.value  # SP3
        self.preamble_id = preamble_id
        self.sfd_id = sfd_id
        self.psdu_data_rate = EnumFiraPsduDataRate.FIRA_PSDU_DATA_RATE_6M81.value
        self.preamble_duration = EnumFiraPreambuleDuration.FIRA_PREAMBULE_DURATION_64.value
        self.ranging_time_struct = 1
        self.slots_per_rr = slots_per_rr
        self.adaptive_payload_power = 0
        self.responder_slot_index = responder_slot_idx  # Fira from 1 to 8
        self.prf_mode = EnumFiraPrfMode.FIRA_PRF_MODE_BPRF.value
        self.scheduled_mode = 1
        self.key_rotation = EnumFiraKeyRotation.FIRA_NO_ROTATION.value  # default : disable
        self.key_rotation_rate = 0
        self.session_priority = 50
        self.mac_address_mode = EnumFiraMacAddrMode.FIRA_MAC_ADDR_MODE_SHORT_SHORT.value
        self.vendor_id = 0
        self.static_sts_iv = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
        self.number_of_sts_segments = EnumFiraStsSegments.FIRA_STS_SEGMENTS_1.value
        self.max_rr_retry = 0
        self.uwb_initiation_time = 0xFFFFFFFF
        self.hopping_mode = EnumFiraHoppingMode.FIRA_HOPPING_DISABLE.value
        self.block_stride_length = 0
        # [b3 b2 b1 b0] -- [AOA FoM, AoA elevation, AoA azimuth, TOF]
        self.result_report_config = 0b00000001
        # 0x00 disable in-band termination attempt;  0x1-0xA, attempt count
        self.in_band_termination_attempt_count = 1
        self.sub_session_id = 0  # 4 Bytes
        # only for PRF_MODE_HPRF, only FiRa
        self.hprf_phr_data_rate = EnumFiraPhrDataRate.FIRA_PHR_DATA_RATE_850K.value
        self.max_num_of_measurements = 0
        self.sts_length = EnumFiraStsLength.FIRA_STS_LENGTH_64.value
        # NCJ29D5 Vendor specific parameters, <NCJ29D5 UCI Specification.pdf> Table 57.
        # defalt values
        self.rx_start_margin = 0x64
        self.rx_timeout = 100
        self.adapted_ranging_index = 0xFFFF
        self.nbic_conf = 0x00
        self.groupdelay_recalc_enable = 0x00
        self.secSessionKey = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # only STS_CONFIG=1, dynamic STS
        self.rcm_rx_margin_time = 2000 # usage 1: 2000; usage 2: 4000
        self.rcm_rx_timeout = 1000 # usage 1: 1000; usage 2: 4000
        self.dynamic_priority_in_synch = 1
        self.tx_power_temp_compensation = 0
        self.long_src_address = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
        self.rr_retry_threshold = 10
        self.tx_power_id = 1  # CCC default tx power -12 dBm
        self.rx_phy_logging_enable = 0
        self.tx_phy_logging_enable = 0
        self.log_param_conf = 0
        self.cir_tap_offset = 0x302
        self.cir_num_taps = 0x64
        self.sts_index_restart = 0
        # FiRa OUI: [0xFF, 0x18, 0x5A], CCC OUI: [0x69, 0xDF, 0x04]
        self.vendor_specific_oui = [0xFF, 0x18, 0x5A]

    def set_dst_addresses(self, dst_mac_addr: list[int]):
        self.dst_mac_addr = dst_mac_addr

    def set_device_mac_addr(self, device_mac_addr: int):
        self.device_mac_addr = device_mac_addr

    def set_rx_phy_logging(self, enable: bool):
        if enable:
            self.rx_phy_logging_enable = 1
        else:
            self.rx_phy_logging_enable = 0

    def set_tx_phy_logging(self, enable: bool):
        if enable:
            self.tx_phy_logging_enable = 1
        else:
            self.tx_phy_logging_enable = 0

    def set_tx_power(self, dbm: int):
        '''
            TX Power (-12 ~ 14) dBm
        '''
        self.tx_power_id = (14 - dbm) * 4

    def set_responder_slot_index(self, responder_slot_index: int):
        if(responder_slot_index > 0 and responder_slot_index < 9):
            self.responder_slot_index = responder_slot_index

    def set_slots_per_rr(self, slots_per_rr: int):
        self.slots_per_rr = slots_per_rr

    def set_slot_length(self, slot_length: EnumRangingSlotLength):
        '''
            Set slot Length
        '''
        self.ranging_slot_length = slot_length.vale

    def get_app_config_tlv(self, param=None) -> list[UciConfigTLV]:
        default_param = None
        if not isinstance(param, FiRaSessionParam):
            default_param = FiRaSessionParam(0, EnumFiraDeviceType.FIRA_DEVICE_TYPE_CONTROLLER.value, EnumFiraDeviceRole.FIRA_DEVICE_ROLE_INITIATOR.value, device_addr=0xFFFF)
        else:
            default_param = param
        app_config_tlv = []
        for key, value in default_param.__dict__.items():
            if value != self.__dict__[key]:
                if key == 'device_type':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_DEVICE_TYPE.value, 1, [self.device_type]))
                elif key == 'ranging_round_usage':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RANGING_METHOD.value, 1, [self.ranging_round_usage]))
                elif key == 'sts_config':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_STS_CONFIG.value, 1, [self.sts_config]))
                elif key == 'multi_node_mode':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_MULTI_NODE_MODE.value, 1, [self.multi_node_mode]))
                elif key == 'channel_id':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_CHANNEL_NUMBER.value, 1, [self.channel_id]))
                elif key == 'anchor_num':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_NO_OF_CONTROLEE.value, 1, [self.anchor_num]))
                elif key == 'device_mac_addr':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_DEVICE_MAC_ADDRESS.value, 2, list(
                        struct.pack("<H", self.device_mac_addr))))
                elif key == 'dst_mac_addr':  # initiator is a device address list
                    number = len(self.dst_mac_addr)
                    buf = []
                    for i in range(number):
                        buf.extend(struct.pack("<H", self.dst_mac_addr[i]))
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_DST_MAC_ADDRESS.value, len(buf), buf))
                elif key == 'ranging_slot_length':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_SLOT_DURATION.value, 2, list(
                        struct.pack("<H", self.ranging_slot_length))))
                elif key == 'ranging_interval':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_RANGING_INTERVAL.value, 4, list(
                        struct.pack("<I", self.ranging_interval))))
                elif key == 'sts_index0':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_STS_INDEX.value, 4, list(struct.pack("<I", self.sts_index0))))
                elif key == 'mac_fcs_type':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_MAC_FCS_TYPE.value, 1, [self.mac_fcs_type]))
                elif key == 'ranging_round_control':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RANGING_ROUND_CONTROL.value, 1, [self.ranging_round_control]))
                elif key == 'rng_data_ntf':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RNG_DATA_NTF.value, 1, [self.rng_data_ntf]))
                elif key == 'rng_data_ntf_proximity_near':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_RNG_DATA_NTF_PROXIMITY_NEAR.value, 2, list(
                        struct.pack("<H", self.rng_data_ntf_proximity_near))))
                elif key == 'rng_data_ntf_proximity_far':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_RNG_DATA_NTF_PROXIMITY_FAR.value, 2, list(
                        struct.pack("<H", self.rng_data_ntf_proximity_far))))
                elif key == 'device_role':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_DEVICE_ROLE.value, 1, [self.device_role]))
                elif key == 'rframe_config':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RFRAME_CONFIG.value, 1, [self.rframe_config]))
                elif key == 'preamble_id':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_PREAMBLE_CODE_INDEX.value, 1, [self.preamble_id]))
                elif key == 'sfd_id':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_SFD_ID.value, 1, [self.sfd_id]))
                elif key == 'psdu_data_rate':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_PSDU_DATA_RATE.value, 1, [self.psdu_data_rate]))
                elif key == 'preamble_duration':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_PREAMBLE_DURATION.value, 1, [self.preamble_duration]))
                elif key == 'ranging_time_struct':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RANGING_TIME_STRUCT.value, 1, [self.ranging_time_struct]))
                elif key == 'slots_per_rr':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_SLOTS_PER_RR.value, 1, [self.slots_per_rr]))
                elif key == 'adaptive_payload_power':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_TX_ADAPTIVE_PAYLOAD_POWER.value, 1, [self.adaptive_payload_power]))
                elif key == 'responder_slot_index':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RESPONDER_SLOT_INDEX.value, 1, [self.responder_slot_index]))
                elif key == 'prf_mode':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_PRF_MODE.value, 1, [self.prf_mode]))
                elif key == 'key_rotation':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_KEY_ROTATION.value, 1, [self.key_rotation]))
                elif key == 'key_rotation_rate':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_KEY_ROTATION_RATE.value, 1, [self.key_rotation_rate]))
                elif key == 'session_priority':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_SESSION_PRIORITY.value, 1, [self.session_priority]))
                elif key == 'mac_address_mode':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_MAC_ADDRESS_MODE.value, 1, [self.mac_address_mode]))
                elif key == 'vendor_id':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_VENDOR_ID.value, 2, list(struct.pack("<H", self.vendor_id))))
                elif key == 'static_sts_iv':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_STATIC_STS_IV.value, 6, self.static_sts_iv))
                elif key == 'number_of_sts_segments':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_NUMBER_OF_STS_SEGMENTS.value, 1, [self.number_of_sts_segments]))
                elif key == 'max_rr_retry':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_MAX_RR_RETRY.value, 2, list(
                        struct.pack("<H", self.max_rr_retry))))
                elif key == 'uwb_initiation_time':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_UWB_INITIATION_TIME.value, 4, list(
                        struct.pack("<I", self.uwb_initiation_time))))
                elif key == 'hopping_mode':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RANGING_ROUND_HOPPING.value, 1, [self.hopping_mode]))
                elif key == 'block_stride_length':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_BLOCK_STRIDE_LENGTH.value, 1, [self.block_stride_length]))
                elif key == 'result_report_config':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RESULT_REPORT_CONFIG.value, 1, [self.result_report_config]))
                elif key == 'in_band_termination_attempt_count':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_IN_BAND_TERMINATION_ATTEMPT_COUNT.value, 1, [self.in_band_termination_attempt_count]))
                elif key == 'max_num_of_measurements':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_MAX_NUM_OF_MEASUREMENTS.value, 2, list(
                        struct.pack("<H", self.max_num_of_measurements))))
                elif key == 'sts_length':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_STS_LENGTH.value, 1, [self.sts_length]))
                elif key == 'tx_power_id':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_TX_POWER_ID.value, 1, [self.tx_power_id]))
                elif key == 'rx_start_margin':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PRRAM_ID_RX_START_MARGIN.value, 1, [self.rx_start_margin]))
                elif key == 'rx_timeout':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RX_TIMEOUT.value, 2, list(struct.pack("<H", self.rx_timeout))))
                elif key == 'adapted_ranging_index':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_ADAPTED_RANGING_INDEX.value, 2, list(
                        struct.pack("<H", self.adapted_ranging_index))))
                elif key == 'nbic_conf':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_NBIC_CONF.value, 1, [self.nbic_conf]))
                elif key == 'groupdelay_recalc_enable':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_GROUPDELAY_RECALC_ENA.value, 1, [self.groupdelay_recalc_enable]))
                elif key == 'secSessionKey':
                    buf = [0]
                    buf.extend(self.secSessionKey)
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_URSK_SecSessionKey.value, len(buf), buf))
                elif key == 'rcm_rx_margin_time':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RCM_RX_MARGIN_TIME.value, 2, list(struct.pack("<H", self.rcm_rx_margin_time))))
                elif key == 'rcm_rx_timeout':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RCM_RX_TIMEOUT.value, 2, list(struct.pack("<H", self.rcm_rx_timeout))))
                elif key == 'dynamic_priority_in_synch':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_DYNAMIC_PRIORITY_IN_SYNCH.value, 1, [self.dynamic_priority_in_synch]))
                elif key == 'tx_power_temp_compensation':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_TX_POWER_TEMP_COMPENSATION.value, 1, [self.tx_power_temp_compensation]))
                elif key == 'long_src_address':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_LONG_SRC_ADDRESS.value, 8, self.long_src_address))
                elif key == 'rr_retry_threshold':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_RR_RETRY_THR.value, 2, list(
                        struct.pack("<H", self.rr_retry_threshold))))
                elif key == 'rx_phy_logging_enable':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RX_PHY_LOGGING_ENBL.value, 1, [self.rx_phy_logging_enable]))
                elif key == 'tx_phy_logging_enable':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_TX_PHY_LOGGING_ENBL.value, 1, [self.tx_phy_logging_enable]))
                elif key == 'log_param_conf':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_LOG_PARAMS_CONF.value, 4, list(struct("<I", self.log_param_conf))))
                elif key == 'cir_tap_offset':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_CIR_TAP_OFFSET.value, 2, list(struct.pack("<H", self.cir_tap_offset))))
                elif key == 'cir_num_taps':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_CIR_NUM_TAPS.value, 2, list(struct.pack("<H", self.cir_num_taps))))
                elif key == 'sts_index_restart':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_STS_INDEX_RESTART.value, 1, [self.sts_index_restart]))
                elif key == 'vendor_specific_oui':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_VENDOR_SPECIFIC_OUI.value, 3, self.vendor_specific_oui))
        return app_config_tlv


def uci_uwb_range_data_ntf_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x62 0x00, FiRa UCI Specification
    '''
    range_data_ntf = FiraRangeDataNtf.from_bytes(payload)
    log_i(str(range_data_ntf))
    for result in range_data_ntf.results:
        log_i(str(result))
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, EnumUciStatus.UCI_STATUS_OK, range_data_ntf)

class FiRaRangingDevice(UCILayer):

    def __init__(self, device, mac_addr, session_map: dict[int, FiRaSessionParam] = {}):
        super().__init__(device)
        self.dev = device
        self.mac_addr = mac_addr
        self.session_map = session_map   # Dict[int, FiRaSessionParam]


    def fira_session_init(self, session: FiRaSessionParam):
        """
        Initiate a FiRa ranging session, store Session Param
        """
        self.session_map[session.session_id] = session
        # register and initialize UCI layer
        self.register_notification_callback(
                EnumUciGid.UWB_RANGE_GID, EnumUwbRangeOid.RANGE_START_OID.value, uci_uwb_range_data_ntf_callback)

        # Initiate FiRa ranging session
        self.uci_session_init(session.session_id,
                              EnumSessionType.SESSION_TYPE_FIRA_RANGING)

        # Wait for response
        result = self.wait_response(timeout_ms=200)

        if result.status is not EnumUciStatus.UCI_STATUS_OK:
            log_e("Error: " + str(result.status))
        else:
            log_i(str(result.uci_result))

        # Wait for SESSION_STATUS_NTF
        result = self.wait_response(timeout_ms=200)
        if result is not None:
            if result.status is not EnumUciStatus.UCI_STATUS_OK:
                log_e("Error: " + str(result.status))
            else:
                log_i(str(result.uci_result))
                if isinstance(result.uci_result, UWBSessionState):
                    self.session_map[result.uci_result.session_id].session_state = result.uci_result


    def fira_session_set_app_config(self, session_id : int):
        param = self.session_map[session_id]
        if param is None:
            log_e("Error: Session not configured! Please call fira_session_init first.")
            return
        if param.session_state is None:
            log_e("Error: Session not successful initialized, reinit!")
            return
        if param.session_state.state is not EnumSessionState.SESSION_STATE_INIT:
            log_e("Error: Session not successful initialized, reinit!")
            return
        else:
            app_config_tlv = param.get_app_config_tlv()
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_DEVICE_MAC_ADDRESS.value for tlv in app_config_tlv):
                log_e("Error: device_mac_addr is mandatory, please check and set the address!")
                return
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_DST_MAC_ADDRESS.value for tlv in app_config_tlv):
                log_e("Error: dst_mac_addr is mandatory, please check and set the addresses -> list[]!")
                return
            # configure mandatory parameters
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_DEVICE_TYPE.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_DEVICE_TYPE.value, 1, [param.device_type]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_RANGING_METHOD.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_RANGING_METHOD.value, 1, [param.ranging_round_usage]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_CHANNEL_NUMBER.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_CHANNEL_NUMBER.value, 1, [param.channel_id]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_MULTI_NODE_MODE.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_MULTI_NODE_MODE.value, 1, [param.multi_node_mode]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_NO_OF_CONTROLEE.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_NO_OF_CONTROLEE.value, 1, [param.anchor_num]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_SLOT_DURATION.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_SLOT_DURATION.value, 2, list(struct.pack("<H", param.ranging_slot_length))))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_RANGING_INTERVAL.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_RANGING_INTERVAL.value, 4, list(struct.pack("<I", param.ranging_interval))))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_DEVICE_ROLE.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_DEVICE_ROLE.value, 1, [param.device_role]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_TX_POWER_ID.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_TX_POWER_ID.value, 1, [param.tx_power_id]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_PREAMBLE_CODE_INDEX.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_PREAMBLE_CODE_INDEX.value, 1, [param.preamble_id]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_SFD_ID.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_SFD_ID.value, 1, [param.sfd_id]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_RESPONDER_SLOT_INDEX.value for tlv in app_config_tlv) and param.device_role == EnumFiraDeviceRole.FIRA_DEVICE_ROLE_RESPONDER.value:
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_RESPONDER_SLOT_INDEX.value, 1, [param.responder_slot_index]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_SLOTS_PER_RR.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_SLOTS_PER_RR.value, 1, [param.slots_per_rr]))
                
            # Transmit app config
            self.uci_session_set_app_config(session_id, app_config_tlv)
            # Wait for response
            result = self.wait_response(timeout_ms=200)

            if result.status is not EnumUciStatus.UCI_STATUS_OK:
                log_e("Error: " + str(result.status))
            else:
                log_i(str(result.uci_result))

    def fira_session_range_start(self, session_id):
        """
        Start a FiRa ranging session
        """
        # Start Fira ranging session
        self.uci_range_start(session_id)

        # Wait for response
        result = self.wait_response(timeout_ms=500)

        if result.status is not EnumUciStatus.UCI_STATUS_OK:
            log_e("Error: " + str(result.status))
        else:
            log_i(str(result.uci_result))

        # Wait for SESSION_STATUS_NTF
        result = self.wait_response(timeout_ms=200)
        if result.status is not EnumUciStatus.UCI_STATUS_OK:
            log_e("Error: " + str(result.status))
        else:
            log_i(str(result.uci_result))

    def fira_session_range_run(self) -> UciRspNtfResult:
        """
        Run FiRa ranging session run, always wait for response/ntf
        """
        return self.wait_response(timeout_ms=500)


    def fira_session_range_stop(self, session_id):
        """
        Stop a FiRa ranging session
        """
        self.uci_range_stop(session_id)

        # Wait for response
        result = self.wait_response(timeout_ms=200)

        if result.status is not EnumUciStatus.UCI_STATUS_OK:
            log_e("Error: " + str(result.status))
        else:
            log_i(str(result.uci_result))
            
        # Wait for SESSION_STATUS_NTF
        result = self.wait_response(timeout_ms=200)
        if result is not None:
            if result.status is not EnumUciStatus.UCI_STATUS_OK:
                log_e("Error: " + str(result.status))
            else:
                log_i(str(result.uci_result))
                self.session_map[result.uci_result.session_id].session_state = result.uci_result


    def fira_session_deinit(self, session_id):
        '''
        Deinitialize FiRa ranging session
        '''
        self.uci_session_deinit(session_id)
        # Wait for response
        result = self.wait_response(timeout_ms=200)
        if result is not None:
            if result.status is not EnumUciStatus.UCI_STATUS_OK:
                log_e("Error: " + str(result.status))
            else:
                log_i(str(result.uci_result))
                
        # Wait for SESSION_STATUS_NTF
        result = self.wait_response(timeout_ms=300)
        if result is not None:
            if result.status is not EnumUciStatus.UCI_STATUS_OK:
                log_e("Error: " + str(result.status))
            else:
                log_i(str(result.uci_result))
                if isinstance(result.uci_result, UWBSessionState):
                    self.session_map[result.uci_result.session_id].session_state = result.uci_result
                    # self.session_map.pop(session_id)        

        
