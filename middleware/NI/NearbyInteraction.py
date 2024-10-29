# -*- coding: utf-8 -*-
"""

@file: Forthink NearbyInteraction library in python

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

import struct
from enum import Enum


class PreferredUpdateRate(Enum):
    '''
        @brief: allows the accessory to indicate a preference for a ranging measurement update intterval
    '''
    PreferredUpdateRate_Automatic = 0  # iOS will choose a value
    PreferredUpdateRate_Infrequent = 10  # ~1.3Hz
    PreferredUpdateRate_UserInteractive = 20  # ~5.5Hz, ranging_interval = 180 ms


class NINearbyMessageId(Enum):
    # From accessory
    MessageId_accessoryConfigurationData = 0x1
    MessageId_accessoryUwbDidStart = 0x2
    MessageId_accessoryUwbDidStop = 0x3

    # To accessory
    MessageId_init = 0xA
    MessageId_configure_and_start = 0xB
    MessageId_stop = 0xC


class NINearbyUwbConfigData():
    '''
        @breif: uwb config data, by the UWB middleware to the embedded application
    '''
    def __init__(self, device_role, short_addr, major_version=1, minor_version=0,
                 manufacture_id=bytearray([0x3f, 0xf5, 0x03, 0x00]),
                 model_id=bytearray([0xb8, 0x0b, 0x00, 0x00]),
                 mw_version=bytearray([0x01, 0x09, 0x09, 0x00])):
        self.length = 19
        self.major_version = major_version
        self.minor_version = minor_version
        self.manufacture_id = manufacture_id
        self.model_id = model_id
        self.mw_version = mw_version
        self.device_role = device_role
        self.short_addr = short_addr
        self.rfu = bytearray([0x19, 0x00])

    def get_uwb_config_bytes(self):
        uwb_config = []
        if self.minor_version == 0:
            uwb_config += bytearray([19])
            uwb_config += struct.pack("<H", self.major_version)  # Specification Major Version 1
            uwb_config += struct.pack("<H", self.minor_version)  # Specification Minor Version 0
            uwb_config += self.manufacture_id  # Manufacture Id
            # uwb_config += bytearray([0x32, 0x11, 0x10, 0x00])  # NXP manufacture ID
            uwb_config += self.model_id  # model_id for device specific
            uwb_config += self.mw_version  # middleware version (qorvo niq version) : 0.9.9.1
            uwb_config += bytearray([self.device_role])  # 0x00 
            uwb_config += struct.pack("<H", self.short_addr)
            self.length = 19
        else:
            uwb_config += bytearray([21])
            uwb_config += struct.pack("<H", self.major_version)  # Specification Major Version 1
            uwb_config += struct.pack("<H", self.minor_version)  # Specification Minor Version 0
            uwb_config += self.manufacture_id  # Manufacture Id
            # uwb_config += bytearray([0x32, 0x11, 0x10, 0x00])  # NXP manufacture ID
            uwb_config += self.model_id  # model_id for device specific
            uwb_config += self.mw_version  # middleware version (qorvo niq version) : 0.9.9.1
            uwb_config += bytearray([self.device_role])  # 0x00 ?
            uwb_config += struct.pack("<H", self.short_addr)
            uwb_config += self.rfu
            self.length = 21
        return bytearray(uwb_config)

class NINearbyAccessoryConfigData():
    '''
        @brief accessory must generate a new AccessoryConfigurationData message, messageId = 0x1
             from the accessory to the Apple device
    '''
    def __init__(self, uwb_config_data:NINearbyUwbConfigData, update_rate=PreferredUpdateRate.PreferredUpdateRate_Automatic):
        self.MajorVersion = 1  # NI Accessory Protocol major version, SpecMajorVersion 00.01
        self.MinorVersion = 0  # NI Accessory Protocol minor version, SpecMinorVersion 00.00
        self.PreferredUpdateRate = update_rate  # UserInteractive = 20 (~5.5Hz), Automatic = 0 (iOS choose one), Infrequent = 10 (~1.3Hz)
        self.RFU = bytes([0x00] * 10)
        self.UWBConfigData = uwb_config_data.get_uwb_config_bytes()

    def get_accessory_config_bytes(self):
        accessory_config = []
        accessory_config += bytearray([0x1])  # MessageId_accessoryConfigurationData = 0x1  1 Byte message id
        accessory_config += struct.pack("<H", self.MajorVersion)
        accessory_config += struct.pack("<H", self.MinorVersion)
        accessory_config += bytearray([self.PreferredUpdateRate.value])
        accessory_config += self.RFU  # rfu
        accessory_config += self.UWBConfigData
        print("accessory config data len: ", len(accessory_config))
        return bytearray(accessory_config)


class NINearbyShareableData():
    '''
        @breif Nearby Interaction Data from iPhone, Message Id 0x0B, used to config FiRa Session
                From the Apple device to the accessory, contains the final configuration parameter selection.
    '''
    def __init__(self, version, length, country_code, session_id, preamble_id, channel, num_slots_rr,
                 slot_duration, ranging_interval, rr_control, sts_init_iv, dst_addr, block_timing_stability=0x64):
        self.version = version
        self.config_data_len = length
        self.country_code = country_code
        self.session_id = session_id
        self.preamble_id = preamble_id
        self.channel_number = channel
        self.num_slots_per_rround = num_slots_rr
        self.slot_duration = slot_duration
        self.ranging_interval = ranging_interval
        self.ranging_round_control = rr_control
        self.sts_init_iv = sts_init_iv
        self.dest_address = dst_addr
        self.block_timing_stability = block_timing_stability

    @staticmethod
    def from_bytes(byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        if len(byte_stream) >= 28:
            version = struct.unpack("<I", byte_stream[0:4])[0]
            length = byte_stream[4]
            datas = struct.unpack("<HIBBHHHB", byte_stream[5: 20])
            country_code = datas[0]
            session_id = datas[1]
            preamble_id = datas[2]
            ch = datas[3]
            num_slots_rr = datas[4]
            slot_duration = datas[5]
            ranging_interval = datas[6]
            ranging_round_control = datas[7]
            sts_init_iv = byte_stream[20:26]
            dst_addr = struct.unpack("<H", byte_stream[26:28])[0]
            if length == 0x17:
                return NINearbyShareableData(version, length, country_code, session_id, preamble_id, ch, num_slots_rr,
                                          slot_duration, ranging_interval, ranging_round_control, sts_init_iv, dst_addr)
            elif length == 0x19:
                stability = struct.unpack("<H", byte_stream[28:30])[0]
                return NINearbyShareableData(version, length, country_code, session_id, preamble_id, ch, num_slots_rr,
                                          slot_duration, ranging_interval, ranging_round_control, sts_init_iv, dst_addr, stability)
            else:
                raise ValueError("Bytes Length Error, not support, only 23 or 25 Bytes")
        else:
            raise ValueError("Bytes Length Error, not support, only 23 or 25 Bytes")


