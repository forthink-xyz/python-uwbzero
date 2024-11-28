# -*- coding: utf-8 -*-
"""

@file: FiRa initiator demo script (normal FiRa protocol)

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""
import sys

from nxp_ft4222h import *
from console_helper import *
from forthink_uwb_dongle import *

from uci_port import *
from uci_defs import *
from uci_layer import *
from FiRaRangingDevice import *
from FiRaRegionParams import *

# Optional: enable Rx logs (in case of ranging errors)
RX_LOG_ENABLE = False

# the UID can get from the module, get LICENSE from : https://licenses.forthink.com.cn/
DONGLE_UID = "d05efb9e"
DONGLE_LICENSE = "7967f9ef4eb14809123fd3c43a30e4b606208a3a960b35d9281fc09b089389300c72ee360695164646c8728c2c3da03663acb0c0bf0ea08dfcc1187fff6d59f7"

def main():
    print_forthink_logo()
    log_i("**************************************************************")
    log_i("Start of UWB Dongle CCC MAC demo script...")
    log_i("**************************************************************")
    
    dongle_list = scan_uwb_dongle_devices()
    if len(dongle_list) == 0:
        sys.exit("No UWB dongle devices found. Aborting program...")

    # get the first device in the list
    dongle = forthink_uwb_dongle(dongle_list[0], uid=DONGLE_UID)
    dongle.ft4222_device.open(spi_frequency_hz=1e07, mode=EnumFtdiSpiMode.FTDI_SPI_MODE_SINGLE)
    # Convert the last 2 bytes of DONGLE_UID to a 16-bit short address
    dongle_addr = 0xFFFF
    if DONGLE_UID != "":
        dongle_addr = int(DONGLE_UID[-4:], 16)
    # register and initialize CCC Ranging Device (include UCI layer) 
    fira_demo_app = FiRaRangingDevice(dongle.ft4222_device, mac_addr=dongle_addr)

    #hard reset UWB Device, activate the device
    fira_demo_app.device.hard_reset()
    result = fira_demo_app.wait_response(timeout_ms=200)
    
    if result.status is not EnumUciStatus.UCI_STATUS_OK:
        log_e(": " + str(result.status))
    else:
        log_i(str(result.uci_result))
    
    # encrypt and verify license
    result = fira_demo_app.uci_forthink_encrypt_verify_license(DONGLE_LICENSE)
    
    log_i("Receiving RSP_ENCRYPT_VERIFY_LICENSE:")
    result = fira_demo_app.wait_response(timeout_ms=400)

    if result.status == EnumUciStatus.UCI_STATUS_OK:
        log_i("License verification successful!")
    else:
        log_e("Error: " + str(result.status.name))
    
    # FiRa Test Params
    fira_test_param = FiRaSessionParam(session_id=0x12345678, device_type=EnumFiraDeviceType.FIRA_DEVICE_TYPE_CONTROLLER.value, device_role=EnumFiraDeviceRole.FIRA_DEVICE_ROLE_INITIATOR.value, device_addr=0xAABB,
                                       ranging_roound_usage=EnumFiraRangingRoundUsage.FIRA_DS_TWR_DEFERRED.value, multi_node_mode=EnumFiraMultiNodeMode.FIRA_MULTI_NODE_MODE_ONE_TO_MANY.value, 
                                       channel_id=9, anchor_num=2)
    fira_test_param.set_dst_addresses([0xCCDD, 0xEEFF])
    fira_test_param.set_tx_power(10)
    
    # FiRa Session Initialization
    fira_demo_app.fira_session_init(fira_test_param)
    fira_demo_app.fira_session_set_app_config(fira_test_param.session_id) 
    fira_demo_app.fira_session_range_start(fira_test_param.session_id)
    
    while(True):
        try:
            result = fira_demo_app.fira_session_range_run()
        except KeyboardInterrupt:
            break
    
    fira_demo_app.fira_session_range_stop(fira_test_param.session_id)
    fira_demo_app.fira_session_deinit(fira_test_param.session_id)
    #close the device
    fira_demo_app.device.close()

    log_i("**************************************************************")
    log_i("End of UWB Dongle Demoboard FiRa MAC Driver program!")
    log_i("**************************************************************")
    
if __name__ == '__main__':
    main()
    