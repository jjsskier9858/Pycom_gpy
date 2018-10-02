
import pycom
import machine
import time
from machine import I2C

i2c2 = I2C()            #i2c instance
io_i2c_addr = 0x20     #io control i2c address read

#Set I2C instance.  This must be called before calling
#any other function in this file.
def set_io_i2c(i2c):
    i2c2 = i2c

def init_io():
    buf = bytearray([0x4F, 0x00])       #Set output port 1 push pull
    i2c2.writeto(io_i2c_addr, buf , stop=False)
    buf = bytearray([0x07, 0xC0])       #Set p1_7, p1_6 as inputs.
    i2c2.writeto(io_i2c_addr, buf , stop=False)

def led_rd_on(on):
    i2c2.writeto(io_i2c_addr, 0x03 , stop=False)       #read port 1 output state (0x03)
    port1_out = i2c2.readfrom(io_i2c_addr, 1)
    cmd = bytearray([0x03, 0x00])

    if(on):
        cmd[1] = port1_out[0] | 0x04            #set bit 2 high (p1_2) LED_RD
        i2c2.writeto(io_i2c_addr, cmd , stop=False)
    else:
        cmd[1] = port1_out[0] & (0xFF ^ 0x04)   #set bit 2 low (P1_2) LED_RD
        i2c2.writeto(io_i2c_addr, cmd , stop=False)

def measure_vbatt():
    i2c2.writeto(io_i2c_addr, 0x03 , stop=False)   #read port 1 output state (0x03)
    port1_out = i2c2.readfrom(0x20, 1)
    print("led port1_out")
    print(port1_out)
    cmd = bytearray([0x03, 0x00])

    adc = machine.ADC()                     # create ADC object
    apin = adc.channel(pin='P13',attn=machine.ADC.ATTN_6DB)   # create analog pin on P13
    cmd[1] = port1_out[0] | 0x10            #set bit 4 high (p1_4) VBAT_SNS_EN
    i2c2.writeto(io_i2c_addr, cmd , stop=False)
    val = apin()                            # read ADC value
    print(val)
    volt = apin.voltage()                   # read ADC voltage
    print(volt)
    cmd[1] = port1_out[0] & (0xFF ^ 0x10)   #set bit 4 low (p1_4) VBAT_SNS_EN
    i2c2.writeto(io_i2c_addr, cmd , stop=False)

def pmic_ce(enable):
    i2c2.writeto(io_i2c_addr, 0x03 , stop=False)   #read port 1 output state (0x03)
    port1_out = i2c2.readfrom(0x20, 1)
    cmd = bytearray([0x03, 0x00])

    if(enable): #enable charging
        cmd[1] = port1_out[0] & (0xFF ^ 0x20)   #set bit 5 low (P1_5) PIMC_CE
        i2c2.writeto(io_i2c_addr, cmd , stop=False)
    else:       # disable charging
        cmd[1] = port1_out[0] | 0x20            #set bit 5 high (P1_5) PIMC_CE
        i2c2.writeto(io_i2c_addr, cmd , stop=False)

def get_charger_status():
    i2c2.writeto(io_i2c_addr, 0x01 , stop=False)
    port1_in = i2c2.readfrom(io_i2c_addr, 1)
    print(port1_in)
