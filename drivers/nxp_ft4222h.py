import ft4222
import time
from enum import IntEnum

import nxp_crc
from uci_port import *

class EnumFtdiGpio(IntEnum):
    FTDI_GPIO_RDY_N = 0
    FTDI_GPIO_INT_N = 1
    FTDI_GPIO_RST_N = 2

class EnumFtdiSpiMode(IntEnum):
    FTDI_SPI_MODE_SINGLE = 0
    FTDI_SPI_MODE_QUAD = 0

class Ft4222hDeviceManager:
    #gets the unique locations of connected ft4222 devices
    def get_device_locations():
        device_locations = []        
        #by default, NCJ29D6 demoboard configures FT4222 chip to mode 0 (DCNF0 pin == 0 (GND) and DCNF1 pin == 0 (GND))
        #this mode emulates each NCJ29D6 demoboard as two separate devices (interfaces) in windows device manager:
        #  the first device 'FT4222 A' provides access to the 4 SPI master pins (SS0O, SCK, MOSI, MISO)
        #  the second device 'FT4222 B' provides access to the 4 GPIO pins (GPIO0,1,2,3)
        #only the location and index are unique for every interface
        number_of_devices = ft4222.createDeviceInfoList()
        for i in range(number_of_devices):
            #get current devices' information
            device_info = ft4222.getDeviceInfoDetail(i, False)
            #here, the function filters FTDI devices for ID 67330076 to only provide FT4222 FTDI IC's,
            #then only the SPI interface (FT4222 A) is returned to the caller
            #if device_info['id'] == 67330076 and device_info['serial'] == b'A':
            # 'A' ASCII == 65
            if device_info['id'] == 67330076 and device_info['serial'][-1] == 65:
                device_locations.append(device_info['location'])
        return device_locations


class Ft4222hDevice(UCIDevice):
    ftdi_spi_interface = object
    ftdi_gpio_interface = object
    device_index = b''
    device_location = 0

    def __init__(self, index, device_location, bD5=True) -> None:
        self.device_index = index
        self.device_location = device_location
        self.is_ncj29d5 = bD5

    #opens the initialized device based on input parameters and the pre-initialized device_location
    def open(self, spi_frequency_hz=1e07, mode=EnumFtdiSpiMode.FTDI_SPI_MODE_SINGLE):
        '''
        @brief Open the FT4222 device and initialize the SPI and GPIO interfaces
        @param spi_frequency_hz: SPI clock frequency in Hz
            support frequencies: 1.25 MHz, 1.5 MHz, 2.5 MHz, 3 MHz, 5 MHz, 6 MHz, 7.5MHz, 10 MHz, 12 MHz, 15MHz, 20 MHz, 40 MHz
        @param mode: SPI mode (single or quad)
        '''
        self.ftdi_spi_interface = ft4222.openByLocation(self.device_location)
        self.ftdi_gpio_interface = ft4222.openByLocation(self.device_location + 1)
        #initialize SPI interface as SPI host
        clock, divider = self.get_spi_clock_divider(requested_spi_frequency_hz=spi_frequency_hz)
        self.ftdi_spi_interface.setClock(clock)
        self.ftdi_spi_interface.spiMaster_Init(mode=ft4222.SPIMaster.Mode.SINGLE, clock=divider, cpol=ft4222.Cpol.IDLE_HIGH, cpha=ft4222.Cpha.CLK_LEADING, ssoMap=ft4222.SlaveSelect.SS0)
        self.ftdi_spi_interface.spi_SetDrivingStrength(clkStrength=ft4222.DrivingStrength.DS4MA, ioStrength=ft4222.DrivingStrength.DS4MA, ssoStrength=ft4222.DrivingStrength.DS4MA)
        self.ftdi_spi_interface.setTimeouts(100, 100)
        #initialize RST_N as GPIO0 output, RDY_N as GPIO1 input, CS_N as GPIO2 output, INT_N as GPIO3 input
        self.ftdi_gpio_interface.gpio_Init(gpio0=ft4222.GPIO.Dir.OUTPUT, gpio1=ft4222.GPIO.Dir.INPUT, gpio2=ft4222.GPIO.Dir.OUTPUT, gpio3=ft4222.GPIO.Dir.INPUT)
        #disable suspend out to enable GPIO2
        self.ftdi_gpio_interface.setSuspendOut(False)
        #disable wakeup interrupt to enable GPIO3
        self.ftdi_gpio_interface.setWakeUpInterrupt(False)
        #set CS_N and RST_N to high
        self.set_cs_n(True)
        self.set_rst_n(True)
        #reset the SPI interface
        self.ftdi_spi_interface.spi_Reset()
        return self

    def close(self) -> None:        
        self.ftdi_spi_interface.close()
        self.ftdi_gpio_interface.close()
        return True

    #returns a tuple of both devicelist of 2 members
    def get_device_info(self):
        return (ft4222.getDeviceInfoDetail(self.device_index, False), ft4222.getDeviceInfoDetail(self.device_index + 1, False))

    #currently, a clock of 80MHz (SysClock.CLK_80) divided by 8 (Clock.DIV_8) ~= 10 MHz SPI clock
    def get_spi_clock_divider(self, requested_spi_frequency_hz):
        if requested_spi_frequency_hz == 1.25e06: 
            return ft4222.SysClock.CLK_80, ft4222.Clock.DIV_64  
        elif requested_spi_frequency_hz == 1.5e06:
            return ft4222.SysClock.CLK_48, ft4222.Clock.DIV_32   
        elif requested_spi_frequency_hz == 2.5e06: 
            return ft4222.SysClock.CLK_80, ft4222.Clock.DIV_32
        elif requested_spi_frequency_hz == 3e06:
            return ft4222.SysClock.CLK_48, ft4222.Clock.DIV_16   
        elif requested_spi_frequency_hz == 5e06:
            return ft4222.SysClock.CLK_80, ft4222.Clock.DIV_16   
        elif requested_spi_frequency_hz == 6e06:
            return ft4222.SysClock.CLK_48, ft4222.Clock.DIV_8
        elif requested_spi_frequency_hz == 7.5e06:
            return ft4222.SysClock.CLK_60, ft4222.Clock.DIV_8
        elif requested_spi_frequency_hz == 1.0e07:
            return ft4222.SysClock.CLK_80, ft4222.Clock.DIV_8    
        elif requested_spi_frequency_hz == 1.2e07:
            return ft4222.SysClock.CLK_48, ft4222.Clock.DIV_4    
        elif requested_spi_frequency_hz == 1.5e07:
            return ft4222.SysClock.CLK_48, ft4222.Clock.DIV_4  
        elif requested_spi_frequency_hz == 2.0e07:
            return ft4222.SysClock.CLK_80, ft4222.Clock.DIV_4   
        elif requested_spi_frequency_hz == 4.0e07:
            return ft4222.SysClock.CLK_80, ft4222.Clock.DIV_2 
        else:
            return ft4222.SysClock.CLK_80, ft4222.Clock.DIV_16   # default 5 MHz
           
    def set_rst_n(self, gpio_level: bool) -> None:
        self.ftdi_gpio_interface.gpio_Write(ft4222.Port.P0, value=gpio_level)

    def get_rdy_n(self) -> bool:
        return bool(self.ftdi_gpio_interface.gpio_Read(ft4222.Port.P1))

    def get_int_n(self) -> bool:
        return bool(self.ftdi_gpio_interface.gpio_Read(ft4222.Port.P3))

    def set_cs_n(self, gpio_level: bool) -> None:
        self.ftdi_gpio_interface.gpio_Write(ft4222.Port.P2, value=gpio_level)

    def hard_reset(self) -> None:
        #put RST_N to low
        self.set_rst_n(False)
        #wait 100ms
        time.sleep(0.1)
        #set RST_N to high (release device)
        self.set_rst_n(True)
        time.sleep(0.1)

    def wait_for_gpio(self, pin: EnumFtdiGpio, gpio_level: bool, timeout_ms=0):
            if pin == EnumFtdiGpio.FTDI_GPIO_RDY_N:
                poll_function = self.get_rdy_n
            elif pin == EnumFtdiGpio.FTDI_GPIO_INT_N:
                poll_function = self.get_int_n
            else:
                return EnumUCIPortStatus.UCI_PORT_STATUS_ERR_BAD_PARAM

            current_gpio_level = poll_function()
            start = time.perf_counter()
            timeout_sec = timeout_ms / 1000
            while (True):
                if timeout_ms != 0:
                    delta = start + timeout_sec - time.perf_counter()
                    if (delta <= 0):
                        return EnumUCIPortStatus.UCI_PORT_STATUS_ERR_TIMEOUT
           
                current_gpio_level = poll_function()
                if (current_gpio_level == gpio_level):
                    return EnumUCIPortStatus.UCI_PORT_STATUS_OK

    def transmit_uci_command(self, input_command, append_crc=False, timeout_ms=0) -> UCIPortResult:
        command = list(input_command)
        target_miso_bytes = []
        status = EnumUCIPortStatus.UCI_PORT_STATUS_UNDEF
        is_crc_valid = False

        if command is None or len(command) < 4:
            status = EnumUCIPortStatus.UCI_PORT_STATUS_ERR_BAD_PARAM
            return UCIPortResult(status, list(target_miso_bytes), is_crc_valid)
        
        # MAX UCI PACKET LENGTH : 4 + 255 = 259 bytes
        if len(command) > 259:
            status = EnumUCIPortStatus.UCI_PORT_STATUS_ERR_BAD_PARAM
            return UCIPortResult(status, list(target_miso_bytes), is_crc_valid)
        
        #append CRC16 if required. If append_crc is false, the user is expected to include the crc bytes in the input command
        if append_crc is True:
            crc = nxp_crc.calculate_crc(frame=command)
            command += crc.to_bytes(2, 'little')
            
        #check if INT_N is asserted before sending the command. If yes, read the response first
        int_n_level = self.get_int_n()
        if int_n_level is False:
            result = self.receive_uci_message(timeout_ms)
            if result.status is EnumUCIPortStatus.UCI_PORT_STATUS_OK:
                status = EnumUCIPortStatus.UCI_PORT_STATUS_RECEIVED_PENDING_MSG
            #response read, wait for INT_N to go high
            self.wait_for_gpio(EnumFtdiGpio.FTDI_GPIO_INT_N, True, timeout_ms=10)
        
        #put CS_N to low to start transmission
        self.set_cs_n(False)
        #wait for RDY_N to go low
        status = self.wait_for_gpio(EnumFtdiGpio.FTDI_GPIO_RDY_N, False, timeout_ms)
        if status is not EnumUCIPortStatus.UCI_PORT_STATUS_OK:
            return UCIPortResult(status, list(target_miso_bytes), is_crc_valid)
        #clock out the data to the device over SPI (SCLK + MOSI lines)
        # target_miso_bytes is the data returned by the device over MISO line during command transmission
        target_miso_bytes = self.ftdi_spi_interface.spiMaster_SingleReadWrite(data = bytes(command), isEndTransaction=True)
        #put CS_N to high to stop transmission
        self.set_cs_n(True)
        status = EnumUCIPortStatus.UCI_PORT_STATUS_OK
        return UCIPortResult(status, list(target_miso_bytes), is_crc_valid)

    def receive_uci_message(self, timeout_ms=400, crc_enable=True) -> UCIPortResult:
        uci_frame = []
        is_crc_valid = False
        status = EnumUCIPortStatus.UCI_PORT_STATUS_UNDEF
        #wait for INT_N to go low
        status = self.wait_for_gpio(EnumFtdiGpio.FTDI_GPIO_INT_N, False, timeout_ms)
        if status is not EnumUCIPortStatus.UCI_PORT_STATUS_OK:
            return UCIPortResult(status, list(uci_frame), is_crc_valid)
        #put CS_N to low to start transmission
        self.set_cs_n(gpio_level=False)
        
        if self.is_ncj29d5 == True:
            #first get the uci header (host clocks out 4 zeroes over SPI (SCLK + MOSI lines))
            # NCJ29D5 UCI, contains one invalid byte
            header = self.ftdi_spi_interface.spiMaster_SingleReadWrite(data = bytes([0x00] * 5), isEndTransaction=False)
            if header is None or len(header) < 5:
                status = EnumUCIPortStatus.UCI_PORT_STATUS_ERR_GENERAL
                return UCIPortResult(status, list(uci_frame), is_crc_valid)
            #identify payload length to receive (two bytes)
            payload_length = header[4] +  (header[3] << 8)
            #get the rest of the payload plus 2 extra bytes of CRC-16
            if crc_enable == True:
                payload = self.ftdi_spi_interface.spiMaster_SingleReadWrite(data = bytes([0x00] * (payload_length + 2)), isEndTransaction=True)
            else:
                payload = self.ftdi_spi_interface.spiMaster_SingleReadWrite(data = bytes([0x00] * (payload_length + 0)), isEndTransaction=True)
                
        else:
            # NCJ29D6 UCI, no invalid byte
            header = self.ftdi_spi_interface.spiMaster_SingleReadWrite(data=bytes([0x00] * 4), isEndTransaction=False)
            if header is None or len(header) < 4:
                status = EnumUCIPortStatus.UCI_PORT_STATUS_ERR_GENERAL
                return UCIPortResult(status, list(uci_frame), is_crc_valid)
            # identify payload length to receive (two bytes)
            payload_length = header[3] + (header[2] << 8)
            if crc_enable == True:
                payload = self.ftdi_spi_interface.spiMaster_SingleReadWrite(data=bytes([0x00] * (payload_length + 2)), isEndTransaction=True)
            else:
                payload = self.ftdi_spi_interface.spiMaster_SingleReadWrite(data=bytes([0x00] * (payload_length + 0)), isEndTransaction=True)
        
        #wait for INT_N to go high: Tx done from Slave
        status = self.wait_for_gpio(EnumFtdiGpio.FTDI_GPIO_INT_N, True, timeout_ms)
        if status is not EnumUCIPortStatus.UCI_PORT_STATUS_OK:
            return UCIPortResult(status, list(uci_frame), is_crc_valid)
        #put CS_N to high to stop transmission
        self.set_cs_n(gpio_level=True)
        #assemble the UCI frame
        if payload is None:
            status = EnumUCIPortStatus.UCI_PORT_STATUS_ERR_GENERAL
            return UCIPortResult(status, list(uci_frame), is_crc_valid)
        
        if self.is_ncj29d5 == True:
            uci_frame = header[1:] + payload
        else:
            uci_frame = header + payload
        
        if crc_enable == True:
            #get the CRC16 from the received frame
            received_crc = uci_frame[-2] | (uci_frame[-1] << 8)
            #validate the CRC16
            is_crc_valid = nxp_crc.is_crc_valid(uci_frame[:-2], received_crc)
        status = EnumUCIPortStatus.UCI_PORT_STATUS_OK
        return UCIPortResult(status, list(uci_frame), is_crc_valid)
