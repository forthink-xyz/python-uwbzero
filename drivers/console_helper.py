# -*- coding: utf-8 -*-
"""

@file: uwb helpers

@author: pony

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

import colorama 
import traceback

from math import ceil

colorama.init()

def log_i(info):
    print(colorama.Fore.GREEN + '[dbg/I] '+ info + colorama.Fore.RESET)

def log_d(info):
    print(colorama.Fore.CYAN + '[dbg/D] ' + info + colorama.Fore.RESET)

def log_w(warn):
    print(colorama.Fore.YELLOW + '[dbg/W] ' + warn + colorama.Fore.RESET)

def log_p(lg):
    print(colorama.Fore.WHITE + '[dbg/P] ' + lg + colorama.Fore.RESET)

def log_e(err):
    frame_info = traceback.extract_stack()[-2]
    filename = frame_info.filename
    lineno = frame_info.lineno
    print(colorama.Fore.RED + f'[dbg/E] {filename}:{lineno} {err}' + colorama.Fore.RESET)


def as_hex(input: int | list[int] | list[list[int]], uppercase = True, prepend_bytes: int = 0) -> str:
    '''
    ### Converts int | list[int] | list[list[int]] to a string in hex format.
    
    #### Arguments:
        input: int | list[int] | list[list[int]]
        uppercase: (optional) bool | True: format with uppercase letters like 0x5A. False: format with lowercase letters like 0x5a.
        
    #### Return:
        msg: str | formatted hex string. Multiple lists will be separated by comma and new line.
    
    '''
    if uppercase:
        hex_format = '0x{:02X}'
    else:
        hex_format = '0x{:02x}'
    
    if prepend_bytes:
        hex_format = hex_format.replace("{", prepend_bytes * "0" + "{")
        
    if input != []:
        if isinstance(input, int):
            if input >= 0:
                msg = f"{hex_format.format(input)}"
            else:
                n = ceil(input.bit_length() / 8)
                msg = f"{hex_format.format(input & (2**(n*8)-1))}"
        elif isinstance(input[0], list):
            msg = ""
            if len(input) == 1:
                msg = str([hex_format.format(i) for i in input[0]])
            else:
                msg += "[ "
                for hex_list in input:
                    msg += f"{[hex_format.format(i) for i in hex_list]},\n"
                msg = msg.removesuffix(",\n")
                msg += " ]"
        elif isinstance(input, list):
            msg = str([hex_format.format(i) for i in input])
        else:
            raise ValueError("Unexpected input")
    else:
        return input
    return msg

def print_hex(byte_stream: list[int]) -> None:
    '''
    Prints int or list of bytes as hex numbers (eg. 0xAA, 0,BB, ...) to console.
    '''
    print(as_hex(byte_stream))

