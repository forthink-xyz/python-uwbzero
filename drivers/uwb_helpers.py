# -*- coding: utf-8 -*-
"""

@file: uwb helpers

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

from enum import IntEnum

SPEED_OF_LIGHT_METERS_PER_SEC = 299792458
UWB_TICKS_TO_SEC_CONVERSION_FACTOR = 15.65 * 1e-12 #one bb tick is equal to 15.65 ps
UWB_TICKS_TO_METERS_CONVERSION_FACTOR = 0.0047     #one bb tick equals to 4.7mm

class EnumUwbChannelFrequency(IntEnum):
    ch5 = 6489600
    ch6 = 6988800
    ch8 = 7488000
    ch9 = 7987200
    
def calculate_tof_ticks_twrds(trnd1: int, trsp1: int, trnd2: int, trsp2: int, group_delay_ticks: int = 0):
    '''
    DS-TWR calculate tof, in UWB ticks (15.65ps)
    :param trnd1:
    :param trsp1:
    :param trnd2:
    :param trsp2:
    :param group_delay_ticks:
    :return:
    '''
    tof_ticks = ((trnd1 * trnd2) - (trsp1 * trsp2)) / (trnd1 + trsp1 + trnd2 + trsp2)
    tof_ticks -= group_delay_ticks
    return int(tof_ticks)

def convert_tof_ticks_to_sec(tof_ticks: int):
    tof_sec = tof_ticks * UWB_TICKS_TO_SEC_CONVERSION_FACTOR
    return tof_sec

def convert_tof_to_distance(tof_sec: float):
    distance_meter = tof_sec * SPEED_OF_LIGHT_METERS_PER_SEC 
    return distance_meter
    