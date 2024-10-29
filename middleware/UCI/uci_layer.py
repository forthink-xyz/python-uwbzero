import struct

from console_helper import *

from uci_defs import *
from uci_port import *
from uci_message import *

class UCILayer():

    def __init__(self, device: UCIDevice):
        self.device = device
        self.device_serial_num = ""
        self.device_license = ""
        self.rsp_callback_table = {}
        self.ntf_callback_table = {}
        # register default notification callbacks
        ## 0-core group notification
        self.register_notification_callback(EnumUciGid.CORE_GENERIC_GID.value, EnumCoreGenericOid.CORE_DEVICE_STATUS_NTF_OID.value, uci_core_device_status_ntf_callback)
        self.register_notification_callback(EnumUciGid.CORE_GENERIC_GID.value, EnumCoreGenericOid.CORE_GENERIC_ERROR_NTF_OID.value, uci_core_generic_error_ntf_callback)
        ## 1-uwb session group notification
        self.register_notification_callback(EnumUciGid.UWB_SESSION_GID.value, EnumUwbSessionOid.SESSION_STATUS_NTF_OID.value, uci_uwb_session_status_ntf_callback)
        self.register_notification_callback(EnumUciGid.UWB_SESSION_GID.value, EnumUwbSessionOid.SESSION_UPDATE_CONTROLLER_MULTICAST_LIST_OID.value, uci_uwb_session_update_controller_multicast_list_ntf_callback)
        ## 2-uwb range group notification
        self.register_notification_callback(EnumUciGid.UWB_RANGE_GID, EnumUwbRangeOid.RANGE_START_OID.value, uci_uwb_range_data_ntf_callback)
        ## forthink vendor-defined group notification
        self.register_notification_callback(EnumUciGid.FORTHINK_VENDOR_GID.value, EnumForthinkVendorOid.CCC_DATA_SET_OID.value, uci_forthink_ccc_data_ntf_callback)
        
        # register default response callbacks
        ## 0-core group response
        self.register_response_callback(EnumUciGid.CORE_GENERIC_GID.value, EnumCoreGenericOid.CORE_DEVICE_RESET_OID.value, uci_core_common_rsp_callback)
        self.register_response_callback(EnumUciGid.CORE_GENERIC_GID.value, EnumCoreGenericOid.CORE_DEVICE_INFO_OID.value, uci_core_get_device_info_rsp_callback)
        self.register_response_callback(EnumUciGid.CORE_GENERIC_GID.value, EnumCoreGenericOid.CORE_GET_CAPS_INFO_OID.value, uci_core_get_caps_info_rsp_callback)
        self.register_response_callback(EnumUciGid.CORE_GENERIC_GID.value, EnumCoreGenericOid.CORE_SET_CONFIG_OID.value, uci_core_set_config_rsp_callback)
        self.register_response_callback(EnumUciGid.CORE_GENERIC_GID.value, EnumCoreGenericOid.CORE_GET_CONFIG_OID.value, uci_core_get_config_rsp_callback)
        ## 1-uwb session group
        self.register_response_callback(EnumUciGid.UWB_SESSION_GID.value, EnumUwbSessionOid.SESSION_INIT_OID.value, uci_core_common_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SESSION_GID.value, EnumUwbSessionOid.SESSION_DEINIT_OID.value, uci_core_common_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SESSION_GID.value, EnumUwbSessionOid.SESSION_SET_APP_CONFIG_OID.value, uci_core_set_config_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SESSION_GID.value, EnumUwbSessionOid.SESSION_GET_APP_CONFIG_OID.value, uci_uwb_session_get_app_config_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SESSION_GID.value, EnumUwbSessionOid.SESSION_GET_COUNT_OID.value, uci_uwb_session_get_count_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SESSION_GID.value, EnumUwbSessionOid.SESSION_GET_STATE_OID.value, uci_uwb_session_get_state_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SESSION_GID.value, EnumUwbSessionOid.SESSION_UPDATE_CONTROLLER_MULTICAST_LIST_OID.value, uci_core_common_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SESSION_GID.value, EnumUwbSessionOid.SESSION_GET_POSSIBLE_RAN_MULTIPLIER_VALUE_OID.value, uci_uwb_session_get_possible_ran_multiplier_rsp_callback)
        ## 2-uwb range group
        self.register_response_callback(EnumUciGid.UWB_RANGE_GID.value, EnumUwbRangeOid.RANGE_START_OID.value, uci_core_common_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_RANGE_GID.value, EnumUwbRangeOid.RANGE_STOP_OID.value, uci_core_common_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_RANGE_GID.value, EnumUwbRangeOid.RANGE_GET_RANGING_COUNT_OID.value, uci_uwb_range_get_ranging_count_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_RANGE_GID.value, EnumUwbRangeOid.RANGE_RESUME_OID.value, uci_core_common_rsp_callback)
        ## 0xA - Forthink Vendor-defined Group
        self.register_response_callback(EnumUciGid.FORTHINK_VENDOR_GID.value, EnumForthinkVendorOid.ENCRYPT_GET_SERIAL_NUM_OID.value, uci_forthink_encrypt_get_serial_num_rsp_callback)
        self.register_response_callback(EnumUciGid.FORTHINK_VENDOR_GID.value, EnumForthinkVendorOid.ENCRYPT_LICENSE_CHECK_OID.value, uci_forthink_encrypt_license_check_rsp_callback)
        self.register_response_callback(EnumUciGid.FORTHINK_VENDOR_GID.value, EnumForthinkVendorOid.CCC_DATA_SET_OID.value, uci_forthink_ccc_data_set_rsp_callback)        
        

    def register_response_callback(self, gid: int, oid: int, callback):
        '''
            @brief callback  func(gid, oid, payload: list[int])
        '''
        index = gid * 256 + oid
        # if callback already exists, overwrite it
        self.rsp_callback_table[index] = callback

    def register_notification_callback(self, gid: int, oid: int, callback):
        '''
            @brief callback func(gid, oid, payload: list[int])
        '''
        index = gid * 256 + oid
        self.ntf_callback_table[index] = callback

    def wait_response(self, timeout_ms=200, crc_enabled=False):
        result = self.device.receive_uci_message(timeout_ms, crc_enabled)
        rsp_ntf_result = UciRspNtfResult(EnumUciMessageType.UCI_MT_UNDEF, 0, 0, EnumUciStatus.UCI_STATUS_FAILED, [])
        if result.status == EnumUCIPortStatus.UCI_PORT_STATUS_OK:
            msg = UciMessage.from_bytes(result.msg_buffer)
            if msg is not None:
                if msg.message_type == EnumUciMessageType.UCI_MT_RESPONSE:
                    index = msg.gid * 256 + msg.oid
                    if index in self.rsp_callback_table:
                        rsp_ntf_result = self.rsp_callback_table[index](msg.gid, msg.oid, msg.payload)
                    else:
                        log_i("UCI Layer: recv a response, no callback, GID: " + hex(msg.gid) + " OID: " + hex(msg.oid) + " payload len: " + str(msg.payload_length))
                        rsp_ntf_result = UciRspNtfResult(msg.message_type, msg.gid, msg.oid, EnumUciStatus.UCI_STATUS_NOT_IMPLEMENTED, msg.payload)
                elif msg.message_type == EnumUciMessageType.UCI_MT_NOTIFICATION:
                    index = msg.gid * 256 + msg.oid
                    if index in self.ntf_callback_table:
                        rsp_ntf_result = self.ntf_callback_table[index](msg.gid, msg.oid, msg.payload)
                    else:
                        log_i("UCI Layer: recv a notification, no callback, GID: " + hex(msg.gid) + " OID:" + hex(msg.oid) + " payload len: " + str(msg.payload_length))
                        rsp_ntf_result = UciRspNtfResult(msg.message_type, msg.gid, msg.oid, EnumUciStatus.UCI_STATUS_NOT_IMPLEMENTED, msg.payload)
                else:
                    log_e(f"UCI Layer: unknown message type: {msg.message_type}")
                    return UciRspNtfResult(msg.message_type, msg.gid, msg.oid, EnumUciStatus.UCI_STATUS_UNKNOWN)
            else:
                log_e("UCI Layer: invalid message received!")
        else:
            log_e(f"UCI Layer: wait response failed, status: {result.status.name}")
        return rsp_ntf_result


    def uci_layer_user_defined_cmd(self, gid: int, oid: int, payload: list[int]):
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, gid, 0, oid, len(payload), payload)
        return self.device.transmit_uci_command(msg.to_byte_stream())
    
    # Forthink Vendor-defined Group OID
    def uci_forthink_encrypt_get_serial_num(self):
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.FORTHINK_VENDOR_GID.value, 0,
                            EnumForthinkVendorOid.ENCRYPT_GET_SERIAL_NUM_OID.value, 0, [])
        return self.device.transmit_uci_command(msg.to_byte_stream())
    
    def uci_forthink_encrypt_verify_license(self, license: str):
        if len(license) != 128:
            log_e("UCI Layer: license length is not 128 bytes!")
            return None
        buf = []
        for c in license:
            buf.append(ord(c))
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.FORTHINK_VENDOR_GID.value, 0,
                            EnumForthinkVendorOid.ENCRYPT_LICENSE_CHECK_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())
    
    def uci_forthink_ccc_data_set(self, session_id: int, repeat_count: int, data: list[int]):
        buf = []
        buf += struct.pack("<IBB", session_id, repeat_count, len(data))
        buf += data
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.FORTHINK_VENDOR_GID.value, 0,
                            EnumForthinkVendorOid.CCC_DATA_SET_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())
         
    # UCI CORE-GROUP Commands
    def uci_core_devive_reset(self):
        payload = [0x0]
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.CORE_GENERIC_GID.value,
                         0, EnumCoreGenericOid.CORE_DEVICE_RESET_OID.value, len(payload), payload)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_core_get_device_info(self):
        payload = []
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.CORE_GENERIC_GID.value,
                         0, EnumCoreGenericOid.CORE_DEVICE_INFO_OID.value, len(payload), payload)
        return self.device.transmit_uci_command(msg.to_byte_stream(), timeout_ms=10)

    def uci_core_get_caps_info(self):
        payload = []
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.CORE_GENERIC_GID.value,
                         0, EnumCoreGenericOid.CORE_GET_CAPS_INFO_OID.value, len(payload), payload)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_core_set_config(self, config: list[UciConfigTLV]):
        buf = [0]
        for tlv in config:
            buf += tlv.to_byte_stream()
        buf[0] = len(config)
        
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.CORE_GENERIC_GID.value,
                         0, EnumCoreGenericOid.CORE_SET_CONFIG_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_core_get_config(self, param_ids: list[int]):
        buf = [len(param_ids)]
        buf += param_ids
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.CORE_GENERIC_GID.value, 0,
                         EnumCoreGenericOid.CORE_GET_CONFIG_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    # UCI UWB-Session Group Commands
    def uci_session_init(self, session_id: int, session_type: EnumSessionType):
        buf = []
        buf += struct.pack("<IB", session_id, session_type.value)
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SESSION_GID.value, 0,
                            EnumUwbSessionOid.SESSION_INIT_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_session_deinit(self, session_id: int):
        buf = []
        buf += struct.pack("<I", session_id)
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SESSION_GID.value, 0,
                            EnumUwbSessionOid.SESSION_DEINIT_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream(), timeout_ms=100)

    def uci_session_set_app_config(self, session_id, config: list[UciConfigTLV]):
        buf = []
        buf += struct.pack("<I", session_id)
        buf += [len(config)]
        for tlv in config:
            buf += tlv.to_byte_stream()
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SESSION_GID.value, 0,
                            EnumUwbSessionOid.SESSION_SET_APP_CONFIG_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_session_get_app_config(self, session_id: int, param_ids: list[int]):
        buf = []
        buf += struct.pack("<I", session_id)
        buf += [len(param_ids)]
        buf += param_ids
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SESSION_GID.value, 0,
                         EnumUwbSessionOid.SESSION_GET_APP_CONFIG_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_session_get_count(self):
        payload = []
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SESSION_GID.value,
                         0, EnumUwbSessionOid.SESSION_GET_COUNT_OID.value, len(payload), payload)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_session_get_state(self, session_id: int):
        buf = []
        buf += struct.pack("<I", session_id)
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SESSION_GID.value, 0,
                            EnumUwbSessionOid.SESSION_GET_STATE_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_session_update_controller_multicast_list(self, session_id, update, controlee_list: list[SessionMulticastControlee]):
        '''
            @brief SESSION_UPDATE_CONTROLLER_MULTICAST_LIST_CMD, used to add controlees dynamically during multicast ranging
                    only for a multicast session, and DEVICE_TYPE set to CONTROLLER
            @param update, 0: add/update, 1: delete from the multicast list
        '''
        buf = []
        buf += struct.pack("<IB", session_id, update)
        buf += [len(controlee_list)]
        for controlee in controlee_list:
            buf += controlee.to_byte_stream()
            
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SESSION_GID.value, 0,
                            EnumUwbSessionOid.SESSION_UPDATE_CONTROLLER_MULTICAST_LIST_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())
        

    def uci_session_get_possible_ran_multiplier(self):
        buf = []
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SESSION_GID.value, 0,
                            EnumUwbSessionOid.SESSION_GET_POSSIBLE_RAN_MULTIPLIER_VALUE_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_session_update_state(self, session_id: int, state: int):
        pass

    # UCI UWB-RANGE Group Commands
    def uci_range_start(self, session_id: int):
        buf = []
        buf += struct.pack("<I", session_id)
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_RANGE_GID.value, 0,
                            EnumUwbRangeOid.RANGE_START_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_range_stop(self, session_id: int):
        buf = []
        buf += struct.pack("<I", session_id)
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_RANGE_GID.value, 0,
                            EnumUwbRangeOid.RANGE_STOP_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_range_get_ranging_count(self, session_id: int):
        pass

    def uci_range_ctrl_req(self):
        pass

    def uci_range_resume(self, session_id: int, sts_index: int):
        buf = []
        buf += struct.pack("<II", session_id, sts_index)
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_RANGE_GID.value, 0,
                            EnumUwbRangeOid.RANGE_RESUME_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    # Android APP_DATA_MANAGE
    def uci_app_data_tx(self):
        pass

    def uci_app_data_rx(self):
        pass

    # FiRa RF Test-Group (0xD)
    def uci_rf_test_config_set(self):
        pass

    def uci_rf_test_config_get(self):
        pass

    def uci_rf_test_periodic_tx(self):
        pass

    def uci_rf_test_per_rx(self):
        pass

    def uci_rf_test_rx(self):
        pass

    def uci_rf_test_loopback(self):
        pass

    def uci_rf_test_stop_session(self):
        pass

    def uci_rf_test_ss_twr(self):
        pass

    def uci_nxp_reset_trim_value(self):
        '''
            when flash a new radio configuration to the NCJ29D5, reset the group delay in trim page
        '''
        buf = [0x01, 0x04, 0x00]
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.VENDOR_E_GID.value, 0,
                            EnumVendorEOid.VENDOR_E_SET_TRIM_VALUE.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())
    
