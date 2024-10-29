# -*- coding: utf-8 -*-
"""

@file:   UCI Message Class and callbacks

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

from uci_defs import *
from console_helper import *
from uci_fira_range_ntf import FiraRangeDataNtf
from uci_ccc_range_ntf import *
import struct


# @defgroup Forthink_UCI
# This is forthink UWB Communication Interface message Class and callbacks ( RESPONSE/NOTIFICATION ).
# @{

# UCI Core Message Classes

class UciCoreDeviceInfo:

    def __init__(self, status: EnumUciStatus, uci_generic_version, mac_version, phy_version, uci_test_version, vendor_spec_info: list[int]):
        self.status = status
        self.uci_generic_version = uci_generic_version
        self.mac_version = mac_version
        self.phy_version = phy_version
        self.uci_test_version = uci_test_version
        self.vendor_spec_info = vendor_spec_info

    @classmethod
    def from_bytes(cls, byte_stream: list[int]):
        try:
            status = EnumUciStatus(byte_stream[0])
            if status != EnumUciStatus.UCI_STATUS_OK:
                return UciCoreDeviceInfo(status, '0.0', '0.0', '0.0', '0.0', [])
            else:
                uci_generic_version = f"{byte_stream[1]}.{byte_stream[2]}"
                mac_version = f"{byte_stream[3]}.{byte_stream[4]}"
                phy_version = f"{byte_stream[5]}.{byte_stream[6]}"
                uci_test_version = f"{byte_stream[7]}.{byte_stream[8]}"
                if len(byte_stream) > 10:
                    vendor_spec_info = byte_stream[10:]
                else:
                    vendor_spec_info = []
                return UciCoreDeviceInfo(status, uci_generic_version, mac_version, phy_version, uci_test_version, vendor_spec_info)
        except ValueError as e:
            log_e(f"Error: {e}")
            return UciCoreDeviceInfo(EnumUciStatus.UCI_STATUS_UNDEF, '0.0', '0.0', '0.0', '0.0', [])

    def __str__(self):
        if self.status == EnumUciStatus.UCI_STATUS_OK:
            return "CORE_GET_DEVICE_INFO_RSP: Status: STATUS_OK\n" \
                + "UCI Generic Version: " + self.uci_generic_version + "\n" \
                + "        MAC Version: " + self.mac_version + "\n" \
                + "        PHY Version: " + self.phy_version + "\n" \
                + "   UCI Test Version: " + self.uci_test_version + "\n" \
                + "   vendor_spec_info: " + \
                str(["0x{:02x}".format(x) for x in self.vendor_spec_info])

        else:
            return f"CORE_GET_DEVICE_INFO_RSP: Status: {self.status}"


class UciCoreCapsInfo():

    def __init__(self, status: EnumUciStatus, uci_caps: list[UciConfigTLV]):
        self.status = status
        self.uci_caps = uci_caps

    @classmethod
    def from_bytes(cls, byte_stream: list[int]):
        status = EnumUciStatus(byte_stream[0])
        if status != EnumUciStatus.UCI_STATUS_OK:
            return UciCoreCapsInfo(status, [])
        else:
            uci_caps = []
            num_caps = byte_stream[1]
            index = 2
            for i in range(num_caps):
                tlv = UciConfigTLV.from_bytes(byte_stream[index:])
                uci_caps.append(tlv)
                index += tlv.length + 2
            return UciCoreCapsInfo(status, uci_caps)

    def __str__(self):
        if self.status == EnumUciStatus.UCI_STATUS_OK:
            return "CORE_GET_CAPS_INFO_RSP: Status: STATUS_OK\n" \
                + "UCI Caps: " + str([f"{x}" for x in self.uci_caps])
        else:
            return f"CORE_GET_CAPS_INFO_RSP: Status: {self.status}"


class UciCoreConfigParamStatus():

    def __init__(self, id: EnumSessionAppConfigID, status: EnumUciStatus):
        self.id = id
        self.status = status


class UciCoreSetConfigRsp():

    def __init__(self, status: EnumUciStatus, param_status: list[UciCoreConfigParamStatus]):
        self.status = status
        self.param_status = param_status

    @classmethod
    def from_bytes(cls, byte_stream: list[int]):
        status = EnumUciStatus(byte_stream[0])
        if status != EnumUciStatus.UCI_STATUS_OK:
            num = byte_stream[1]
            param_status_list = []
            for i in range(0, num):
                id = EnumSessionAppConfigID(byte_stream[2+2*i])
                param_status = EnumUciStatus(byte_stream[2+2*i+1])
                param_status_list.append(
                    UciCoreConfigParamStatus(id, param_status))
            return UciCoreSetConfigRsp(status, param_status_list)
        return UciCoreSetConfigRsp(status, [])

    def __str__(self):
        if self.status != EnumUciStatus.UCI_STATUS_OK:
            return f"CORE_SET_CONFIG_RSP: Status: {self.status}\n" \
                + "Param Status: " + \
                str([f"ID: {x.id}, Status: {x.status}" for x in self.param_status])
        else:
            return f"CORE_SET_CONFIG_RSP: Status: {self.status}"

# UCI UWB Session Message Classes


class SessionMulticastControlee():
    '''
        FiRa Consortium UCI Specification v1.1, 6 Bytes: mac_addr(2) + sub_session_id(4)
    '''

    def __init__(self, sub_session_id: int, short_addr: int = 0):
        self.short_addr = short_addr
        self.sub_session_id = sub_session_id

    @classmethod
    def from_bytes(cls, byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        short_addr = struct.unpack("<H", byte_stream[0:2])[0]
        sub_session_id = struct.unpack("<I", byte_stream[2:6])[0]
        return SessionMulticastControlee(short_addr, sub_session_id)

    def to_byte_stream(self):
        return list(struct.pack("<HI", self.short_addr, self.sub_session_id))

    def __str__(self) -> str:
        return f"Short Address: {self.short_addr}, Sub Session ID: {self.sub_session_id} \n"


class SessionMulticastControleeStatus():

    def __init__(self, size, controlee_list: list[SessionMulticastControlee], status_list: list[EnumMulticastUpdateStatus]):
        self.remain_size = size
        self.controlee_list = controlee_list
        self.status_list = status_list


class UWBSessionState():

    def __init__(self, session_id, state: EnumSessionState, reason_code: EnumSessionStateChangeReason):
        self.session_id = session_id
        self.state = state
        self.reason_code = reason_code

    def __str__(self) -> str:
        return f"CCC_SESSION_STATUS:\n" \
            + f"        session_id: {self.session_id} \n" \
            + f"            status: {self.state.name} \n" \
            + f"       reason_code: {self.reason_code.name} \n"


# UCI Common RSP/NTF callbacks, can used by most of the RESPONSE

def uci_core_common_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4X 0xXX, common response callback, only support CMD Status
    '''
    status = EnumUciStatus.UCI_STATUS_UNDEF
    try:
        status = EnumUciStatus(payload[0] & 0xFF)
        log_i(f"UCI_COMMON_RSP GID: {gid} OID: {oid} Status: {status.name}")
    except ValueError as e:
        log_e(f"Error: {e}")
    result = []
    if len(payload) > 1:
        result = payload[1:]
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status, result)


def uci_core_common_ntf_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x6X 0xXX, common notification callback, only support CMD Status
    '''
    status = EnumUciStatus.UCI_STATUS_UNDEF
    try:
        status = EnumUciStatus(payload[0] & 0xFF)
        log_i(f"UCI_COMMON_NTF GID: {gid} OID: {oid} Status: {status.name}")
    except ValueError as e:
        log_e(f"Error: {e}")
    result = []
    if len(payload) > 1:
        result = payload[1:]
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, status, result)


# UCI Core-Group RSP/NTF callbacks

def uci_core_device_status_ntf_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID:  0x60 0x01
    '''
    state = EnumDeviceState(payload[0])
    log_i(f"CORE_DEVICE_STATUS_NTF: State: {state}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, EnumUciStatus.UCI_STATUS_OK, state)


def uci_core_get_device_info_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x40 0x02
    '''
    dev_info = UciCoreDeviceInfo.from_bytes(byte_stream=payload)
    log_i(str(dev_info))
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, dev_info.status, dev_info)


def uci_core_get_caps_info_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x40 0x03
    '''
    caps_info = UciCoreCapsInfo.from_bytes(payload)
    log_i(str(caps_info))
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, caps_info.status, caps_info)


def uci_core_set_config_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x40 0x04
    '''
    config_rsp = UciCoreSetConfigRsp.from_bytes(payload)
    log_i(str(config_rsp))
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, config_rsp.status, config_rsp)


def uci_core_get_config_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x40 0x05
    '''
    status = EnumUciStatus(payload[0])
    num = payload[1]
    config_list = []
    idx = 2
    for i in range(num):
        tlv = UciConfigTLV.from_bytes(payload[idx:])
        idx += tlv.length + 2
        config_list.append(tlv)
    log_i(f"CORE_GET_CONFIG_RSP: Status: {status}, Number: {num}")
    for tlv in config_list:
        log_i(str(tlv))
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status, config_list)


def uci_core_generic_error_ntf_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x60 0x07
    '''
    error = EnumUciStatus(payload[0])
    log_e(f"CORE_GENERIC_ERROR_NTF: Error: {error}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, error)


# UCI UWB-Session-Group RSP/NTF callbacks

def uci_uwb_session_status_ntf_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x61 0x02
    '''
    ntf = struct.unpack("<IBB", bytes(payload))
    session_id = ntf[0]
    session_state = EnumSessionState(ntf[1])
    reason_code = EnumSessionStateChangeReason(ntf[2])

    log_i(
        f"UCI_UWB_SESSION_STATUS_NTF: session_id: {session_id} session_state: {session_state} reason_code: {reason_code}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, EnumUciStatus.UCI_STATUS_OK, UWBSessionState(session_id, session_state, reason_code))


def uci_uwb_session_get_app_config_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x41 0x04
    '''
    status = EnumUciStatus(payload[0])
    num = payload[1]
    config_list = []
    idx = 2
    for i in range(num):
        # do not include extension TAG ID
        tlv = UciConfigTLV.from_bytes(payload[idx:])
        idx += tlv.length + 2
        config_list.append(tlv)
    log_i(f"UWB_SESSION_GET_APP_CONFIG_RSP: Status: {status}, Number: {num}")
    for tlv in config_list:
        log_i(str(tlv))
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status, config_list)


def uci_uwb_session_get_count_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x41 0x05
    '''
    status = EnumUciStatus(payload[0])
    count = payload[1]
    log_i(
        f"UCI_UWB_SESSION_GET_COUNT_RSP: status: {status.name}, count: {count}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status, count)


def uci_uwb_session_get_state_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x41 0x06
    '''
    status = EnumUciStatus(payload[0])
    state = EnumSessionState(payload[1])
    log_i(
        f"UCI_UWB_SESSION_GET_STATE_RSP: status: {status.name}, state: {state.name}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status, state)

# def uci_uwb_session_update_controller_multicast_list_rsp_callback(gid: int, oid: int, payload: list[int]):
#     '''
#         GID OID: 0x41 0x07, common response
#     '''
#     status = EnumUciStatus(payload[0])


def uci_uwb_session_update_controller_multicast_list_ntf_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x61 0x07
        FiRa Consortium UCI Specification v1.1, 7 Bytes; MAC 3.7.0 supportted 7 Bytes.
        NXP NCJ29D5 MAC 3.5.0, only 5 bytes, from payload length to compatible. 
    '''
    session_id = struct.unpack("<I", bytes(payload[0:4]))[0]
    remain_size = payload[4]
    num = payload[5]
    controlee_list = []
    status_list = []
    if len(payload) == (6 + num*7):
        for i in range(num):
            controlee = SessionMulticastControlee.from_bytes(
                payload[6 + i*7: 6 + i*7 + 6])
            controlee_list.append(controlee)
            status = EnumMulticastUpdateStatus(payload[6 + i*7 + 6])
            status_list.append(status)
    elif len(payload) == (6 + num*5):
        for i in range(num):
            sub_session_id = struct.unpack(
                "<I", bytes(payload[6 + i*5: 6 + i*5 + 4]))[0]
            controlee = SessionMulticastControlee(sub_session_id)
            controlee_list.append(controlee)
            status = EnumMulticastUpdateStatus(payload[6 + i*5 + 4])
            status_list.append(status)

    log_i(
        f"UCI_UWB_SESSION_UPDATE_CONTROLLER_MULTICAST_LIST_NTF: session_id: {session_id}, remain_size: {remain_size}, num: {num}")
    ntf = SessionMulticastControleeStatus(
        remain_size, controlee_list, status_list)
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, EnumUciStatus.UCI_STATUS_OK, ntf)


def uci_uwb_session_get_possible_ran_multiplier_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x41 0x20
    '''
    status = EnumUciStatus(payload[0])
    ran_multiplier = payload[1]
    log_i(
        f"UCI_UWB_SESSION_GET_POSSIBLE_RAN_MULTIPLIER_RSP: status: {status}, ran_multiplier: {ran_multiplier}")
    if ran_multiplier == 1:
        log_i("UWB Session Load is below 25%")
    elif ran_multiplier == 2:
        log_i("UWB Session Load is between 25% ~ 50%")
    elif ran_multiplier == 3:
        log_i("UWB Session Load is between 50% ~ 75%")
    elif ran_multiplier == 4:
        log_i("UWB Session Load is between 75% ~ 100%")
    else:
        log_i("UWB Session Load is 100%")

    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status, ran_multiplier)


# UCI UWB-Range-Group RSP/NTF callbacks

def uci_uwb_range_data_ntf_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x62 0x00, FiRa Consortium UCI Specification
    '''
    range_data_ntf = FiraRangeDataNtf.from_bytes(payload)
    log_i(str(range_data_ntf))
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, EnumUciStatus.UCI_STATUS_OK, range_data_ntf)


def uci_uwb_range_get_ranging_count_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x42 0x02
    '''
    status = EnumUciStatus(payload[0])
    count = struct.unpack("<I", bytes(payload[1:5]))[0]
    log_i(
        f"UCI_UWB_RANGE_GET_RANGING_COUNT_RSP: status: {status}, count: {count}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status, count)

# CCC Range data NTF callbacks, controller or controlee, only register one of them


def uci_uwb_range_ccc_data_ntf_controller_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x62 0x20, CCC Digital Key 3.0 Specification
    '''
    range_data_ntf = CCCRangeDataNtfController.from_bytes(payload)
    log_i(str(range_data_ntf))
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, EnumUciStatus.UCI_STATUS_OK, range_data_ntf)


def uci_uwb_range_ccc_data_ntf_controlee_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x62 0x21, CCC Digital Key 3.0 Specification
    '''
    range_data_ntf = CCCRangeDataNtfControlee.from_bytes(payload)
    log_i(str(range_data_ntf))
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, EnumUciStatus.UCI_STATUS_OK, range_data_ntf)


def uci_uwb_range_ccc_data_ntf_controller_exp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x62 0x23, Controller Expand CCC Digital Key 3.0 Specification
    '''
    range_data_ntf = CCCRangeDataNtfControllerExp.from_bytes(payload)
    log_i(str(range_data_ntf))
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, EnumUciStatus.UCI_STATUS_OK, range_data_ntf)


def uci_forthink_ccc_data_ntf_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x6A 0x20, Forthink CCC Digital Key 3.0 Specification
    '''
    session_id = struct.unpack("<I", bytes(payload[0:4]))[0]
    length = payload[4]
    broadcast_data = payload[5:]
    log_str = f"CCC_DATA_NTF:\n" \
        + f"  session_id: {hex(session_id)} \n" \
        + f"      length: {length} \n"
    log_str += "  broadcast_data: " + \
        str([" 0x{:02x}".format(x) for x in broadcast_data])
    log_i(log_str)

    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, EnumUciStatus.UCI_STATUS_OK)

# Forthink UCI Message Callbacks


def uci_forthink_encrypt_get_serial_num_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4A 0x30
        @return UciRspNtfResult
                uci_result: serial number -> str
    '''
    status = EnumUciStatus(payload[0])
    serial_num = [chr(payload[7]), chr(payload[8]),
                  chr(payload[5]), chr(payload[6]),
                  chr(payload[3]), chr(payload[4]),
                  chr(payload[1]), chr(payload[2])]
    serial_num = ''.join(serial_num).lower()
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status, serial_num)


def uci_forthink_encrypt_license_check_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4A 0x31
    '''
    status = EnumUciStatus(payload[0])
    license = ""
    if status == EnumUciStatus.UCI_STATUS_OK:
        log_i("License verification successful!")
    else:
        log_e("Error: " + str(status.name))
        license = bytes(payload[1:])
        log_i("License: " + license.decode('utf-8'))
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status, license)


def uci_forthink_ccc_data_set_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4A 0x20
    '''
    status = EnumUciStatus(payload[0])
    log_i(f"UCI_FORTHINK_CCC_DATA_SET_RSP: status: {status.name}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status)

# @}
