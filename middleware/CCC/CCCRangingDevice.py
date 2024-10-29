# -*- coding: utf-8 -*-
"""

@file: CCC ranging device Class

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

from console_helper import *

from CCCRegionParams import *
from uci_message import *
from uci_defs import *
from uci_layer import UCILayer

class CCCSessionParam():

    def __init__(self, session_id, device_type: int, device_role: int, anchor_num, sts_config=1, sts_index0=0, ranging_interval=96, slot_length=EnumRangingSlotLength.RANGING_SLOT_LENGTH_2MS.value,
                 slots_per_rr=12, channel=9, preamble_id=9, responder_slot_idx=0, session_state: UWBSessionState = None, ccc_config_quirks = 0, uwb_config_id = 0x0001,
                 URSK=[0x00, 0x01, 0x02, 0x03, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 
                       0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f]):
        self.session_id = session_id
        self.device_type = device_type
        self.sts_config = sts_config
        self.channel_id = channel
        self.anchor_num = anchor_num
        self.device_mac_addr = 0
        self.dst_mac_addr = 0
        self.ranging_slot_length = slot_length
        self.ranging_interval = ranging_interval
        self.sts_index0 = sts_index0
        self.mac_fcs_type = EnumCCCMacFcsType.CCC_MAC_FCS_TYPE_CRC_16.value
        self.rng_data_ntf = EnumCCCRangeDataNtfConfig.CCC_RANGE_DATA_NTF_ALWAYS.value
        self.rng_data_ntf_proximity_near = 0
        self.rng_data_ntf_proximity_far = 20000
        self.device_role = device_role
        self.preamble_id = preamble_id
        self.sfd_id = 2
        self.slots_per_rr = slots_per_rr
        self.adaptive_payload_power = 0
        self.responder_slot_index = responder_slot_idx
        self.key_rotation = EnumCCCKeyRotation.CCC_STS_KEY_ROTATION.value
        self.session_priority = 50
        self.max_rr_retry = 0
        self.uwb_initiation_time = 0xFFFFFFFF
        self.hopping_mode = EnumCCCHoppingMode.CCC_NO_HOPPING.value
        self.max_num_of_measurements = 0xFFFF
        self.hop_mode_key = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
        self.ccc_config_quirks = ccc_config_quirks
        self.ranging_protocol_ver = 0x0100
        self.uwb_config_id = uwb_config_id
        if uwb_config_id == 0:
            self.sfd_id = 0
        self.pulse_shape_combo = EnumCCCPulseshapeCombo.CCC_PULSESHAPE_COMBO_0.value
        self.URSK_TTL = 0x02D0
        self.responder_listen_only = EnumCCCResponderListen.CCC_RESPONDER_NORMAL.value
        self.URSK = URSK
        self.last_sts_index_used = 0
        # defalt values
        self.tx_power_id = 1  # CCC default tx power -12 dBm
        self.rx_start_margin = 0x64
        self.rx_timeout = 100
        self.adapted_ranging_index = 0xFFFF
        self.nbic_conf = 0x01
        self.groupdelay_recalc_enable = 0x00
        self.rcm_rx_margin_time = 2000 # usage 1: 2000; usage 2: 4000
        self.rcm_rx_timeout = 1000 # usage 1: 1000; usage 2: 4000
        self.dynamic_priority_in_synch = 1
        self.tx_power_temp_compensation = 0
        self.long_src_address = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
        self.rr_retry_threshold = 10
        self.rx_phy_logging_enable = 0
        self.tx_phy_logging_enable = 0
        self.log_param_conf = 0
        self.cir_tap_offset = 0x302
        self.cir_num_taps = 0x64
        self.sts_index_restart = 0
        self.vendor_specific_oui = [0x69, 0xDF, 0x04]   # FiRa OUT [0xFF, 0x18, 0x5A]
        self.session_state = session_state
        self.ranging_round_usage = 2

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
        self.tx_power_id = (14 - dbm ) * 4
    
    def set_responder_slot_index(self, responder_slot_index: int):
        '''
            The CCC responder slot index from 0 to N-1 (N is the number of responders)
        '''
        self.responder_slot_index = responder_slot_index

    def set_slots_per_rr(self, slots_per_rr: int):
        '''
            slots_per_rr: 6, 8, 9, 12, 16, 18, 32, 36, 48, 72, 96
        '''
        if slots_per_rr not in [6, 8, 9, 12, 16, 18, 32, 36, 48, 72, 96]:
            raise ValueError(
                "Invalid value for slots_per_rr. Must be one of: 6, 8, 9, 12, 16, 18, 32, 36, 48, 72, 96")

        self.slots_per_rr = slots_per_rr

    def set_slot_length(self, slot_length: EnumRangingSlotLength):
        '''
            Set slot Length
        '''
        self.ranging_slot_length = slot_length.vale

    def get_app_config_tlv(self, param=None) -> list[UciConfigTLV]:
        default_param = None
        if not isinstance(param, CCCSessionParam):
            default_param = CCCSessionParam(
                0, EnumCCCDeviceType.CCC_DEVICE_TYPE_CONTROLLER.value, EnumCCCDeviceRole.CCC_DEVICE_ROLE_INITIATOR.value, 1)
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
                elif key == 'channel_id':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_CHANNEL_NUMBER.value, 1, [self.channel_id]))
                elif key == 'anchor_num':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_NO_OF_CONTROLEE.value, 1, [self.anchor_num]))
                elif key == 'device_mac_addr':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_DEVICE_MAC_ADDRESS.value, 2, list(
                        struct.pack("<H", self.device_mac_addr))))
                elif key == 'dst_mac_addr':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_DST_MAC_ADDRESS.value, 2, list(
                        struct.pack("<H", self.dst_mac_addr))))
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
                elif key == 'preamble_id':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_PREAMBLE_CODE_INDEX.value, 1, [self.preamble_id]))
                elif key == 'sfd_id':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_SFD_ID.value, 1, [self.sfd_id]))
                elif key == 'slots_per_rr':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_SLOTS_PER_RR.value, 1, [self.slots_per_rr]))
                elif key == 'adaptive_payload_power':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_TX_ADAPTIVE_PAYLOAD_POWER.value, 1, [self.adaptive_payload_power]))
                elif key == 'responder_slot_index':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RESPONDER_SLOT_INDEX.value, 1, [self.responder_slot_index]))
                elif key == 'key_rotation':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_KEY_ROTATION.value, 1, [self.key_rotation]))
                elif key == 'session_priority':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_SESSION_PRIORITY.value, 1, [self.session_priority]))
                elif key == 'max_rr_retry':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_MAX_RR_RETRY.value, 2, list(
                        struct.pack("<H", self.max_rr_retry))))
                elif key == 'uwb_initiation_time':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_UWB_INITIATION_TIME.value, 4, list(
                        struct.pack("<I", self.uwb_initiation_time))))
                elif key == 'hopping_mode':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RANGING_ROUND_HOPPING.value, 1, [self.hopping_mode]))
                elif key == 'max_num_of_measurements':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_MAX_NUM_OF_MEASUREMENTS.value, 2, list(
                        struct.pack("<H", self.max_num_of_measurements))))
                elif key == 'hop_mode_key':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_HOP_MODE_KEY.value, 16, self.hop_mode_key))
                elif key == 'ccc_config_quirks':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_CCC_CONFIG_QUIRKS.value, 1, [self.ccc_config_quirks]))
                elif key == 'ranging_protocol_ver':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_RANGING_PROTOCOL_VER.value, 2, list(
                        struct.pack("<H", self.ranging_protocol_ver))))
                elif key == 'uwb_config_id':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_UWB_CONFIG_ID.value, 2, list(
                        struct.pack("<H", self.uwb_config_id))))
                elif key == 'pulse_shape_combo':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_PULSE_SHAPE_COMBO.value, 1, [self.pulse_shape_combo]))
                elif key == 'URSK_TTL':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_URSK_TTL.value, 2, list(struct.pack("<H", self.URSK_TTL))))
                elif key == 'responder_listen_only':
                    app_config_tlv.append(UciConfigTLV(
                        EnumSessionAppConfigID.PARAM_ID_RESPONDER_LISTEN_ONLY.value, 1, [self.responder_listen_only]))
                elif key == 'last_sts_index_used':
                    app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_LAST_STS_INDEX_USED.value, 4, list(
                        struct.pack("<I", self.last_sts_index_used))))
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
                elif key == 'URSK':
                    buf = [0]
                    buf.extend(self.URSK)
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


class CCCRangingDevice(UCILayer):

    def __init__(self, device, mac_addr, session_map: dict[int, CCCSessionParam] = {}):
        super().__init__(device)
        self.dev = device
        self.mac_addr = mac_addr
        self.session_map = session_map   # Dict[int, CCCSessionParam]

    def ccc_session_init(self, session: CCCSessionParam):
        """
        Initiate a CCC ranging session, store Session Param
        """
        self.session_map[session.session_id] = session
        # register and initialize UCI layer, register the CCC Session callbacks
        if session.device_type == EnumCCCDeviceType.CCC_DEVICE_TYPE_CONTROLLER:
            self.register_notification_callback(
                EnumUciGid.UWB_RANGE_GID, EnumUwbRangeOid.RANGE_CCC_DATA_NTF_OID.value, uci_uwb_range_ccc_data_ntf_controller_callback)
            self.register_notification_callback(EnumUciGid.UWB_RANGE_GID, EnumUwbRangeOid.RANGE_CCC_DATA_NTF_EXP_OID.value, uci_uwb_range_ccc_data_ntf_controller_exp_callback)
        else:
            self.register_notification_callback(
                EnumUciGid.UWB_RANGE_GID, EnumUwbRangeOid.RANGE_CCC_DATA_NTF_OID.value, uci_uwb_range_ccc_data_ntf_controlee_callback)

        # Initiate CCC ranging session
        self.uci_session_init(session.session_id,
                              EnumSessionType.SESSION_TYPE_CCC_RANGING)

        # Wait for response
        result = self.wait_response(timeout_ms=200)

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
            if isinstance(result.uci_result, UWBSessionState):
                self.session_map[result.uci_result.session_id].session_state = result.uci_result

    def ccc_session_set_app_config(self, session_id : int):
        """
        Configure CCC ranging session parameters
        """
        param = self.session_map[session_id]
        if param is None:
            log_e("Error: Session not configured! Please call ccc_session_init first.")
            return
        if param.session_state is None:
            log_e("Error: Session not successful initialized, reinit!")
            return
        if param.session_state.state is not EnumSessionState.SESSION_STATE_INIT:
            log_e("Error: Session not successful initialized, reinit!")
            return
        else:
            app_config_tlv = param.get_app_config_tlv()
            # configure mandatory parameters
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_DEVICE_TYPE.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_DEVICE_TYPE.value, 1, [param.device_type]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_CHANNEL_NUMBER.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_CHANNEL_NUMBER.value, 1, [param.channel_id]))
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
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_RESPONDER_SLOT_INDEX.value for tlv in app_config_tlv) and param.device_role == EnumCCCDeviceRole.CCC_DEVICE_ROLE_RESPONDER.value:
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_RESPONDER_SLOT_INDEX.value, 1, [param.responder_slot_index]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_SLOTS_PER_RR.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_SLOTS_PER_RR.value, 1, [param.slots_per_rr]))
            if not any(tlv.tag == EnumSessionAppConfigID.PARAM_ID_URSK_SecSessionKey.value for tlv in app_config_tlv):
                app_config_tlv.append(UciConfigTLV(EnumSessionAppConfigID.PARAM_ID_URSK_SecSessionKey.value, 33, [0] + param.URSK))
                
            # Transmit app config
            self.uci_session_set_app_config(session_id, app_config_tlv)
            # Wait for response
            result = self.wait_response(timeout_ms=200)

            if result.status is not EnumUciStatus.UCI_STATUS_OK:
                log_e("Error: " + str(result.status))
            else:
                log_i(str(result.uci_result))

    def ccc_session_range_start(self, session_id):
        """
        Start a CCC ranging session
        """
        # Start CCC ranging session
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

    def ccc_session_range_run(self) -> UciRspNtfResult:
        """
        Run CCC ranging session run, always wait for response/ntf
        """
        return self.wait_response(timeout_ms=1000)

    def ccc_session_range_stop(self, session_id):
        """
        Stop a CCC ranging session
        """
        # Stop CCC ranging session
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

    def ccc_session_deinit(self, session_id):
        '''
        Deinitialize CCC ranging session
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

