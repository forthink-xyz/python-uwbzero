# -*- coding: utf-8 -*-
"""

@file: fira session use UCI (UWB Command Interface)

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

import struct
from enum import IntEnum


class EnumMacAddrMode(IntEnum):
    '''
        MAC_ADDRESS_MODE, Tb. 29, Tag ID: 0x26
    '''
    MAC_SHORT_ADDR = 0x00
    MAC_LONG_ADDR = 0x03


class FiraTwrResult():
    '''
        @brief Two Way Ranging Measurement Result, reference <UCI generic specification> Table 23
    '''

    def __init__(self, mac_address, status, nlos, distance, slot_index,
                 aoa_azimuth, aoa_azimuth_fom,
                 aoa_elevation, aoa_elevation_fom,
                 dst_aoa_azimuth, dst_aoa_azimuth_fom,
                 dst_aoa_elevation, dst_aoa_elevation_fom
                 ):
        self.mac_address = mac_address
        self.status = status
        self.nlos = nlos
        self.distance = distance
        self.slot_index = slot_index
        self.aoa_azimuth = aoa_azimuth
        self.aoa_azimuth_fom = aoa_azimuth_fom
        self.aoa_elevation = aoa_elevation
        self.aoa_elevation_fom = aoa_elevation_fom
        self.dst_aoa_azimuth = dst_aoa_azimuth
        self.dst_aoa_azimuth_fom = dst_aoa_azimuth_fom
        self.dst_aoa_elevation = dst_aoa_elevation
        self.dst_aoa_elevation_fom = dst_aoa_elevation_fom

    @staticmethod
    def from_bytes(byte_stream, mac_addr_mode=EnumMacAddrMode.MAC_SHORT_ADDR.value):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        if mac_addr_mode > 0:
            mac_addr = struct.unpack("<Q", byte_stream[0:8])[0]
            status = byte_stream[8]
            nlos = byte_stream[9]
            distance = struct.unpack("<H", byte_stream[10:12])[0]
            aoa_azimuth = struct.unpack("<H", byte_stream[12:14])[0]
            aoa_azimuth_fom = byte_stream[14]
            aoa_elevation = struct.unpack("<H", byte_stream[15:17])[0]
            aoa_elevation_fom = byte_stream[17]
            dst_aoa_azimuth = struct.unpack("<H", byte_stream[18:20])[0]
            dst_aoa_azimuth_fom = byte_stream[20]
            dst_aoa_elevation = struct.unpack("<H", byte_stream[21:23])[0]
            dst_aoa_elevation_fom = byte_stream[23]
            slot_index = byte_stream[24]
            return FiraTwrResult(mac_addr, status, nlos, distance, slot_index, aoa_azimuth, aoa_azimuth_fom,
                                 aoa_elevation, aoa_elevation_fom,
                                 dst_aoa_azimuth, dst_aoa_azimuth_fom,
                                 dst_aoa_elevation, dst_aoa_elevation_fom)
        else:
            mac_addr = struct.unpack("<H", byte_stream[0:2])[0]
            status = byte_stream[2]
            nlos = byte_stream[3]
            distance = struct.unpack("<H", byte_stream[4:6])[0]
            aoa_azimuth = struct.unpack("<H", byte_stream[6:8])[0]
            aoa_azimuth_fom = byte_stream[8]
            aoa_elevation = struct.unpack("<H", byte_stream[9:11])[0]
            aoa_elevation_fom = byte_stream[11]
            dst_aoa_azimuth = struct.unpack("<H", byte_stream[12:14])[0]
            dst_aoa_azimuth_fom = byte_stream[14]
            dst_aoa_elevation = struct.unpack("<H", byte_stream[15:17])[0]
            dst_aoa_elevation_fom = byte_stream[17]
            slot_index = byte_stream[18]
            return FiraTwrResult(mac_addr, status, nlos, distance, slot_index, aoa_azimuth, aoa_azimuth_fom,
                                 aoa_elevation, aoa_elevation_fom,
                                 dst_aoa_azimuth, dst_aoa_azimuth_fom,
                                 dst_aoa_elevation, dst_aoa_elevation_fom)
    def __str__(self) -> str:
        return f"RANGE_DATA_NTF: idx: {self.slot_index} \n" \
            + f"         mac address: {hex(self.mac_address)} \n" \
            + f"            distance: {self.distance} \n" 


class FiraRangeDataNtf():
    '''
        @brief RANGE_DATA_NTF data payload, reference <UCI generic specification> Table 22
    '''

    def __init__(self, seq_num, session_id, cur_ranging_interval, ranging_measure_type, mac_addr_mode, result_num, results: list[FiraTwrResult]):
        self.seq_num = seq_num
        self.session_id = session_id
        self.cur_ranging_interval = cur_ranging_interval
        self.ranging_measure_type = ranging_measure_type
        self.mac_addr_mode = mac_addr_mode
        self.result_num = result_num
        self.results = results

    @staticmethod
    def from_bytes(byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        seq_num = struct.unpack("<I", byte_stream[0:4])[0]
        session_id = struct.unpack("<I", byte_stream[4:8])[0]
        # byte_stream[8] rfu
        range_interval = struct.unpack("<I", byte_stream[9:13])[0]
        type = byte_stream[13]
        # byte_stream[14] rfu
        mac_addr_mode = byte_stream[15]
        # byte_stream[16:23], rfu
        num = byte_stream[24]
        results = []
        for index in range(num):
            # the FiRaTwrResult 31 Bytes (all mac addr mode)
            result = FiraTwrResult.from_bytes(
                byte_stream[25 + index * 31 : index * 31 + 25 + 31], mac_addr_mode)
            results.append(result)

        fira_data_ntf = FiraRangeDataNtf(
            seq_num, session_id, range_interval, type, mac_addr_mode, num, results)

        return fira_data_ntf

    def __str__(self) -> str:
        return f"RANGE_DATA_NTF: seq_num: {self.seq_num} \n" \
            + f"             session_id: {hex(self.session_id)} \n" \
            + f"   cur_ranging_interval: {self.cur_ranging_interval} \n" \
            + f"   ranging_measure_type: {self.ranging_measure_type} \n" \
            + f"          mac_addr_mode: {self.mac_addr_mode} \n" \
            + f"result_num: {self.result_num}, results: {self.results}"
