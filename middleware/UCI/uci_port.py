# -*- coding: utf-8 -*-
"""

@file:   UCI Port for different Hardware Interface

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

from enum import IntEnum
from abc import ABC, abstractmethod

class EnumUCIPortStatus(IntEnum):
    UCI_PORT_STATUS_UNDEF = 0
    UCI_PORT_STATUS_OK = 1
    UCI_PORT_STATUS_RECEIVED_PENDING_MSG = 2
    UCI_PORT_STATUS_ERR_GENERAL = 3
    UCI_PORT_STATUS_ERR_TIMEOUT = 4
    UCI_PORT_STATUS_ERR_BAD_PARAM = 5


class EnumUCIPortType(IntEnum):
    # UCI NXP SPI handshake interface, IRQ/RDY + SPI(4-wire)
    UCI_INTF_ABSTRACT = 0x00
    UCI_INTF_NXP_SPI = 0x01    # UCI NXP 6-wire SPI handshake interface
    UCI_INTF_UART_HS = 0x02    # UCI UART handshake interface
    UCI_INTF_UART = 0x03       # UCI_UART interface
    UCI_INTF_SPI_FD_HS = 0x04  # UCI SPI Full-Duplex handshake interface
    UCI_INTF_SPI_HD_HS = 0x05  # UCI SPI Half-Duplex handshake interface


class EnumUCIDeviceStatus(IntEnum):
    UCI_DEVICE_STATUS_OPEN = 0x00
    UCI_DEVICE_STATUS_CLOSED = 0x01

class UCIPortResult():
    def __init__(self, status, msg_buffer: list[int], is_crc_valid):
        self.status = status
        self.msg_buffer = msg_buffer
        self.is_crc_valid = is_crc_valid


class UCIDevice(ABC):

    def __init__(self, device, type: EnumUCIPortType):
        self.device = device
        self.device_type = type
        self.device_status = EnumUCIDeviceStatus.UCI_DEVICE_STATUS_CLOSED

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def hard_reset(self):
        pass

    @abstractmethod
    def transmit_uci_command(self, msg, append_crc=False, timeout_ms=0) -> UCIPortResult:
        '''
            @brief abstract method to transmit UCI message, max pakcet size is: 4 + 255 = 259 bytes
            @param msg: list[int]
            @return: UCIPortResult / [status, list(target_miso_bytes), is_crc_valid]
                    if param wrong, status = EnumUCIPortStatus.UCI_PORT_STATUS_ERR_BAD_PARAM
        '''
        pass

    @abstractmethod
    def receive_uci_message(self, timeout_ms=200, crc_enabled=False) -> UCIPortResult:
        '''
            @brief abstract method to receive UCI message
            @return: UCIPortResult / [status: EnumUCIPortStatus, recv_msg_buffer, is_crc_valid]
        '''
        pass
