# This file contains functions for controlling the EVA-M8M-0 gps
# Functions meant to be called in the following order.
#
#  set_gps_i2c(i2c)                  (Call this once to pass in i2c instance)
#  disable_nmea_messages()           (Call this once to disable unsolicited messages.)
#  lat,ns,long,ew = get_lat_long()   (Call as necessary to get gps data)
#  receiver_on(False)                (Call to turn off receiver to save power)
#  receiver_on(True)                 (Call to turn on receiver)

import pycom
import time
from machine import I2C
import binascii

#command[5] is nmea message id
#command[8] I2C message frequency.  Set to one for one message per event.
command = bytearray([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
#list of nmea message ids
messageIds = bytearray([0x0a, 0x44, 0x09, 0x00, 0x01, 0x43, 0x42, 0x0d, 0x40, 0x06, 0x02, 0x07, 0x03, 0x04, 0x41, 0x0f, 0x05, 0x08])

i2c2 = I2C()            #i2c instance
gps_i2c_addr = 0x42     #GPS i2c address

#Set I2C instance.  This must be called before calling
#any other function in this file.
def set_gps_i2c(i2c):
    i2c2 = i2c

#calculate UBX message checksum
#called by disable_nmea_messages()
def add_checksum():
    ck_a = 0x00
    ck_b = 0x00

    for index in range(len(command)-2):
        if(index > 1):
            ck_a = ck_a + command[index]
            ck_b = ck_b + ck_a
    command[14] = ck_a & 0xff
    command[15] = ck_b & 0xff

#disable all unsolicited nmea messages on all ports.
def disable_nmea_messages():
    for index in range(len(messageIds)):
        command[7] = messageIds[index]
        add_checksum()
        print(binascii.hexlify(command))
        i2c2.writeto(gps_i2c_addr, command , stop=False)
        time.sleep(0.01)
        buf = bytearray(5)
        i2c2.readfrom_into(gps_i2c_addr, buf)
        print(buf)
    buf = bytearray(100)
    i2c2.readfrom_into(gps_i2c_addr, buf)
    print(buf)

#Receiver power control
def receiver_on(On):
    if On:
        #On
        i2c2.writeto(gps_i2c_addr,bytearray([0xB5, 0x62, 0x06, 0x57, 0x08, 0x00, 0x01, 0x00, 0x00, 0x00, 0x20, 0x4E, 0x55, 0x52, 0x7B, 0xC3]))
    else:
        #Off
        i2c2.writeto(gps_i2c_addr,bytearray([0xB5, 0x62, 0x06, 0x57, 0x08, 0x00, 0x01, 0x00, 0x00, 0x00, 0x50, 0x4F, 0x54, 0x53, 0xAC, 0x85]))

#Get current lattitude longitude data
def get_lat_long():
    buf = request_lat_long()
    print(buf)
    if buf[0] == 0x00 or buf[0:10] == b'GNGLL,,,,,':
        lat = "nan"
        ns = "nan"
        long = "nan"
        ew = "nan"
    else:
        lat = str(buf[6:16],"utf-8")
        ns = chr(buf[17])
        long = str(buf[20:30],"utf-8")
        ew = chr(buf[31])
    return lat,ns,long,ew

#Send command to request GNGLL message and parse lat,long data
#Called by get_lat_long()
def request_lat_long():
    i2c2.writeto(gps_i2c_addr, '$EIGNQ,GLL*3F\r\n')
    notfound = True
    loopcount = 0
    while notfound == True and loopcount < 20:
        loopcount += 1
        time.sleep(0.1)
        dollarsign = i2c2.readfrom(gps_i2c_addr, 1)
        if dollarsign == b'$':
            notfound = False
    time.sleep(0.25)
    buf = bytearray(60)
    i2c2.readfrom_into(gps_i2c_addr, buf)
    header = buf[0:5]
    if header == b'GNGLL':
        return buf
    else:
        return bytearray(60)

def request_satellites_in_view():
    i2c2.writeto(gps_i2c_addr, '$EIGNQ,GSV*3A\r\n')
    notfound = True
    loopcount = 0
    while notfound == True and loopcount < 20:
        loopcount += 1
        time.sleep(0.1)
        dollarsign = i2c2.readfrom(gps_i2c_addr, 1)
        if dollarsign == b'$':
            notfound = False
    time.sleep(0.25)
    buf = bytearray(60)
    i2c2.readfrom_into(gps_i2c_addr, buf)
    header = buf[0:5]
    if header == b'GPGSV':
        return buf
    else:
        return bytearray(60)
