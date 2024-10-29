# -*- coding: utf-8 -*-
"""

@file: CCC session use UCI (UWB Command Interface)

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

import struct
from enum import IntEnum


class EnumCCCRangeStatus(IntEnum):
    '''
        RANGE_CCC_DATA_NTF, ranging status
    '''
    RANGING_SUCCESS = 0x00
    RANGING_TRANSACTION_OVERFLOW = 0x01
    RANGING_TRANSACTION_EXPIRED = 0x02
    RANGING_INCORRECT_FRAME = 0x03
    RAMGING_RESPONDER_LISTEN_MODE = 0x0D
    RANGING_CONTROL_MSG_LOST = 0x0F
    


class CCCRangeDataNtfControlee():
    
    def __init__(self, session_id: int, range_status: EnumCCCRangeStatus, sts_index, rr_index, distance, anchor_fom, initiator_fom, ccm_tag: list[int]):
        self.session_id = session_id
        self.range_status = range_status
        self.sts_index = sts_index
        self.rr_index = rr_index
        self.distance = distance
        self.anchor_fom = anchor_fom
        self.initiator_fom = initiator_fom
        self.ccm_tag = ccm_tag
    
    @staticmethod
    def from_bytes(byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        session_id = struct.unpack("<I", byte_stream[0:4])[0]
        range_status = EnumCCCRangeStatus((byte_stream[4]>>4)&0x0F)  # MSB 4 bit, Responder ranging status
        sts_index = struct.unpack("<I", byte_stream[5:9])[0]
        rr_index = struct.unpack("<H", byte_stream[9:11])[0]
        distance = struct.unpack("<H", byte_stream[11:13])[0]   # distance in cm
        anchor_fom = byte_stream[13]                            # Ranging timestamp uncertainty of controlee
        initiator_fom = byte_stream[14]                         # Ranging timestamp uncertainty of controller
        ccm_tag = byte_stream[15:23]                            # CCM* Tag calculated over all payload fileds, CCM* TAG can be set to all 0xFF if not used
        return CCCRangeDataNtfControlee(session_id, range_status, sts_index, rr_index, distance, anchor_fom, initiator_fom, ccm_tag)
        
    def __str__(self) -> str:
        return f"CCC_RANGE_DATA_NTF:\n" \
            +  f"        session_id: {hex(self.session_id)} \n" \
            +  f"      range_status: {self.range_status.name} \n" \
            +  f"         sts_index: {self.sts_index} \n" \
            +  f"          rr_index: {self.rr_index} \n" \
            +  f"      distance(cm): {self.distance} \n" \
            +  f"anchor_fom: {self.anchor_fom}, init_form: {self.initiator_fom}"
            
class CCCRangeDataNtfController():
    
    def __init__(self, session_id, range_status, sts_index, rr_index, response_status, ccm_tag: list[int]):
        self.session_id = session_id
        self.range_status = range_status
        self.sts_index = sts_index
        self.rr_index = rr_index
        self.response_status = response_status
        self.ccm_tag = ccm_tag
    
    @staticmethod
    def from_bytes(byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        session_id = struct.unpack("<I", byte_stream[0:4])[0]
        range_status = EnumCCCRangeStatus(byte_stream[4]&0x0F)
        sts_index = struct.unpack("<I", byte_stream[5:9])[0]
        rr_index = struct.unpack("<H", byte_stream[9:11])[0]
        response_status = struct.unpack("<I", byte_stream[11:15])[0]
        ccm_tag = byte_stream[15:23]
        return CCCRangeDataNtfController(session_id, range_status, sts_index, rr_index, response_status, ccm_tag)
    
    def __str__(self) -> str:
        return f"CCC_RANGE_DATA_NTF(Controller):\n" \
            +  f"        session_id: {hex(self.session_id)} \n" \
            +  f"      range_status: {self.range_status.name} \n" \
            +  f"         sts_index: {self.sts_index} \n" \
            +  f"          rr_index: {self.rr_index} \n" \
            +   "  responder status: " + str("0x{:08x}".format(self.response_status))


class CCCResponderResult():
    '''
        @brief CCC Responder distance, CCC 3.0 Expansion
    '''

    def __init__(self, index, distance):
        self.responder_index = index
        self.distance = distance

    @staticmethod
    def from_bytes(byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)

        index = byte_stream[0]
        distance = struct.unpack("<H", byte_stream[1:3])[0]
        return CCCResponderResult(index, distance)

    def __str__(self) -> str:
        return f"Responder idx: {self.responder_index} \n" \
            + f"      distance: {self.distance} \n" 


class CCCRangeDataNtfControllerExp():
    '''
        @brief the Forthink-CCC-MAC which expand the CCC 3.0, the CCC Controller support the distances from responders
    '''
    def __init__(self, session_id, range_status, sts_index, rr_index, response_status, num, results: list[CCCResponderResult]):
        self.session_id = session_id
        self.range_status = range_status
        self.sts_index = sts_index
        self.rr_index = rr_index
        self.response_status = response_status
        self.responder_num = num
        self.results = results
    
    @staticmethod
    def from_bytes(byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        session_id = struct.unpack("<I", byte_stream[0:4])[0]
        sts_index = struct.unpack("<I", byte_stream[4:8])[0]
        rr_index = struct.unpack("<H", byte_stream[8:10])[0]
        range_status = EnumCCCRangeStatus(byte_stream[10]&0x0F)
        range_num = byte_stream[11]
        response_status = struct.unpack("<I", byte_stream[12:16])[0]
        results = []
        for index in range(range_num):
            result = CCCResponderResult.from_bytes(
                byte_stream[16 + index * 3 : index * 3 + 16 + 3])
            results.append(result)
        return CCCRangeDataNtfControllerExp(session_id, range_status, sts_index, rr_index, response_status, range_num, results)
    
    def __str__(self) -> str:
        return f"CCC_RANGE_DATA_NTF(Controller):\n" \
            +  f"        session_id: {hex(self.session_id)} \n" \
            +  f"      range_status: {self.range_status.name} \n" \
            +  f"         sts_index: {self.sts_index} \n" \
            +  f"          rr_index: {self.rr_index} \n" \
            +   "  responder status: " + str("0x{:08x}".format(self.response_status)) \
            + str(self.results)
