
"""
Necassary Instructions
1. Enable Serial Port
2. Remove "console=serial0,115200" from file /boot/firmware/cmdline.txt as it will impose 115200 baud rate while PZEM requires 9600
3. Run this script, if error is serial port permission denied, run this script as sudo 
"""

"""
An error faced mostly:
https://raspberrypi.stackexchange.com/questions/111817/serial-serialutil-serialexception-device-reports-readiness-to-read-but-returned
"""
# To install library for PZEM:
# pip3 install modbus-tk
# pip3 install pyserial

import time

#library for PZEM-004T V3
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

SLAVE_ADDR = 0x01

# Connect to the slave
serial = serial.Serial(
                       port='/dev/ttyS0',
                       baudrate=9600,
                       bytesize=8,
                       parity='N',
                       stopbits=1,
                       xonxoff=1
                      )

master = modbus_rtu.RtuMaster(serial)
master.set_timeout(2.0)
master.set_verbose(True)

# Changing power alarm value to 100 W
master.execute(SLAVE_ADDR, cst.WRITE_SINGLE_REGISTER, 1, output_value=1)

while True:
    data        = master.execute(SLAVE_ADDR, cst.READ_INPUT_REGISTERS, 0, 10)  # format: (slave address, cst.WRITE_SINGLE_REGISTER, from address, to address)
    voltage     = data[0] / 10.0 # [V]
    current     = (data[1] + (data[2] << 16)) / 1000.0 # [A]
    power       = (data[3] + (data[4] << 16)) / 10.0 # [W]
    energy      = data[5] + (data[6] << 16) # [Wh]
    frequency   = data[7] / 10.0 # [Hz]
    powerFactor = data[8] / 100.0
    alarm       = data[9] # 0 = no alarm

    print('Voltage [V]\t: ', voltage)
    print('Current [A]\t: ', current)
    print('Power [W]\t: ', power) # active power = (V * I * power factor)
    print('Energy [Wh]\t: ', energy)
    print('Frequency [Hz]\t: ', frequency)
    print('Power factor \t: ', powerFactor)
    print('Alarm \t\t: ', alarm)
    print("--------------------")

    
    time.sleep(1)

