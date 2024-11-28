# -*- coding: utf-8 -*-
"""

@file: CCC responder demo script (normal CCC protocol)

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

from CCCRangingDevice import *
from CCCRegionParams import *

# Optional: enable Rx logs (in case of ranging errors)
RX_LOG_ENABLE = False

# the UID can get from the module, get LICENSE from : https://licenses.forthink.com.cn/
DONGLE_UID = "d05efba6"
DONGLE_LICENSE = "395a761af4df0850a94bc5d5a5bdaaa6387c88d1d15ae444ee5ab7f1c4d542f42e1654777b9addc1c25a0084f35f8e27e1ee5fb2c19df273cba4930d61ed675c"


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
    ccc_demo_app = CCCRangingDevice(dongle.ft4222_device, mac_addr=dongle_addr)

    #hard reset UWB Device, activate the device
    ccc_demo_app.device.hard_reset()
    result = ccc_demo_app.wait_response(timeout_ms=200)
    
    if result.status is not EnumUciStatus.UCI_STATUS_OK:
        log_e(": " + str(result.status))
    else:
        log_i(str(result.uci_result))
    
    # encrypt and verify license
    result = ccc_demo_app.uci_forthink_encrypt_verify_license(DONGLE_LICENSE)
    
    log_i("Receiving RSP_ENCRYPT_VERIFY_LICENSE:")
    result = ccc_demo_app.wait_response(timeout_ms=400)
    if result.status == EnumUciStatus.UCI_STATUS_OK:
        log_i("License verification successful!")
    else:
        log_e("Error: " + str(result.status.name))
    
    # CCC Car key Test Params
    ccc_car_keys_param = CCCSessionParam(session_id=0x12345678, device_type=EnumCCCDeviceType.CCC_DEVICE_TYPE_CONTROLEE.value, uwb_config_id=0,
                                    device_role=EnumCCCDeviceRole.CCC_DEVICE_ROLE_RESPONDER.value, anchor_num=1, sts_index0=0x075BCD15, slots_per_rr=6, ranging_interval=960, ccc_config_quirks=1,
                                    URSK=[0xed, 0x07, 0xa8, 0x0d, 0x2b, 0xeb, 0x00, 0xf7, 0x85, 0xaf, 0x26, 0x27, 0xc9, 0x6a, 0xe7, 0xc1, 0x18, 0x50, 0x42, 0x43, 0xcb, 0x2c, 0x32, 0x26, 0xb3, 0x67, 0x9d, 0xaa, 0x0f, 0x7e, 0x61, 0x6c])
    ccc_car_keys_param.channel_id = 9
    ccc_car_keys_param.ranging_slot_length = 2400
    # ccc_car_keys_param.mac_fcs_type = 0
    ccc_car_keys_param.hopping_mode = EnumCCCHoppingMode.CCC_NO_HOPPING.value
    # ccc_car_keys_param.hopping_mode = EnumCCCHoppingMode.CCC_CONTINUOUS_HOPPING_MODULO.value
    # ccc_car_keys_param.hopping_mode = EnumCCCHoppingMode.CCC_CONTINUOUS_HOPPING_AES.value
    ccc_car_keys_param.hop_mode_key = [0x4C, 0x57, 0x72, 0xBC, 0x90, 0x79, 0x8c, 0x8e, 0x51, 0x8d, 0x24, 0x49, 0x09, 0x2f, 0x1b, 0x56]
    ccc_car_keys_param.set_tx_power(10)
    ccc_car_keys_param.set_responder_slot_index(0)
    # CCC Session Initialization
    ccc_demo_app.ccc_session_init(ccc_car_keys_param)
    ccc_demo_app.ccc_session_set_app_config(ccc_car_keys_param.session_id) 
    ccc_demo_app.ccc_session_range_start(ccc_car_keys_param.session_id)
    
    while(True):
        try:
            result = ccc_demo_app.ccc_session_range_run()
        except KeyboardInterrupt:
            break
    
    ccc_demo_app.ccc_session_range_stop(ccc_car_keys_param.session_id)
    ccc_demo_app.ccc_session_deinit(ccc_car_keys_param.session_id)
    #close the device
    ccc_demo_app.device.close()

    log_i("**************************************************************")
    log_i("End of UWB Dongle Demoboard CCC MAC Driver program!")
    log_i("**************************************************************")
    
if __name__ == '__main__':
    main()
    