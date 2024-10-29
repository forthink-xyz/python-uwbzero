# -*- coding: utf-8 -*-
"""

@file: uwb helpers

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

import crcengine

def calculate_crc(frame: list[int]) -> int:
    ''' Calculate crc as int based on list of input bytes '''
    crc = crcengine.new('crc16-xmodem').calculate(frame)
    return crc

def is_crc_valid(frame: list[int], received_crc: int) -> bool:
    ''' Check if received crc (int) matches received frame '''
    actual_crc = calculate_crc(frame)
    return actual_crc == received_crc

def check_for_crc(uci_frame: list[int]):
    '''
    Input:
        frame: The received uci package bytes
    Output:
        calculated_crc: The calculated crc (list[int]) based on the input frame
        provided_crc: The crc bytes (list[int]) of the input frame | Will be 'None' of frame without crc is provided
        
    Disclaimer: CRC16 is expected
    '''
    payload_length = uci_frame[3] + (uci_frame[2] << 8)
    
    # if CRC is not provided
    if payload_length == (len(uci_frame) - 4):
        calculated_crc_int = calculate_crc(uci_frame)
        calculated_crc = [(calculated_crc_int & 0xFF), calculated_crc_int >> 8]
        provided_crc = None
        return calculated_crc, provided_crc
    # if CRC provided
    elif payload_length == (len(uci_frame) - 6):
        calculated_crc_int = calculate_crc(uci_frame[:-2])
        calculated_crc = [(calculated_crc_int & 0xFF), calculated_crc_int >> 8]
        provided_crc = uci_frame[-2:]
        return calculated_crc, provided_crc
    else:
        raise ValueError
    
def analyse_crc(uci_message, provided_crc, calculated_crc):
    '''
    Use-case: Interpreter
    
    Input:
        uci_message: UciMessage | crc will be removed from payload
        provided_crc: list[int]
        calculated_crc: list[int]
    Output:
        crc_value_string: Message about provided CRC
        crc_status_string: Message stating if CRC is valid
        
    Disclaimer: CRC16 is expected
    '''
    if provided_crc is not None:
        crc_value_string = "Provided CRC: " + str(["0x{:02x}".format(i) for i in provided_crc])
        # delete crc from payload
        uci_message.payload = uci_message.payload[:-2]
    else:
        crc_value_string = "Provided CRC: None"
    
    crc_value_string += "\n" + "Calculated CRC: " + str(["0x{:02x}".format(i) for i in calculated_crc])
    
    if provided_crc is not None and provided_crc == calculated_crc:
        crc_status_string = "CRC is valid!"
    elif provided_crc is not None and provided_crc != calculated_crc:
        crc_status_string = "CRC is NOT valid!"
    else:
        crc_status_string = None
        
    return crc_value_string, crc_status_string
