# -*- coding: utf-8 -*-
"""

@file: uwb helpers

@author: pony

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""
from nxp_ft4222h import *
from console_helper import *

def print_forthink_logo():
    print('')                                                                                    
    print("███████╗ ██████╗ ██████╗ ████████╗██╗  ██╗██╗███╗   ██╗██╗  ██╗")
    print("██╔════╝██╔═══██╗██╔══██╗╚══██╔══╝██║  ██║██║████╗  ██║██║ ██╔╝")
    print("█████╗  ██║   ██║██████╔╝   ██║   ███████║██║██╔██╗ ██║█████╔╝ ")
    print("██╔══╝  ██║   ██║██╔══██╗   ██║   ██╔══██║██║██║╚██╗██║██╔═██╗ ")
    print("██║     ╚██████╔╝██║  ██║   ██║   ██║  ██║██║██║ ╚████║██║  ██╗")
    print("╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝")
    print('')

def scan_uwb_dongle_devices() -> list[Ft4222hDevice]:
    '''
        Scans for available UWB dongle devices and returns a list of them.
        @return : list[Ft4222hDevice]
    '''
    ft4222_device_list = []
    
    #get list of locations for available ftdi ft4222 devices
    ftdi_device_locations = Ft4222hDeviceManager.get_device_locations()

    #abort if no devices found
    if(len(ftdi_device_locations) <= 0):
        log_e("No FTDI devices found. Aborting program...")
        return ft4222_device_list

    #print all devices
    log_i("Detected " + str(len(ftdi_device_locations)) + " FTDI device(s): " + str(ftdi_device_locations))

    for idx in range(len(ftdi_device_locations)):
        device_location = ftdi_device_locations[idx]
        ft4222_device = Ft4222hDevice(idx, device_location)
        ft4222_device_list.append(ft4222_device)

    return ft4222_device_list

class forthink_uwb_dongle():
    
    def __init__(self, ft4222_device: Ft4222hDevice, uid = "", is_ncj29d5 = True):
        self.ft4222_device = ft4222_device
        self.UID = uid
        if is_ncj29d5 == False:
            self.ft4222_device.is_ncj29d5 = False
        
    
    