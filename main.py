
import pycom
import time
import machine
from machine import I2C
from gps import disable_nmea_messages, receiver_on, request_satellites_in_view
from gps import get_lat_long, set_gps_i2c, request_lat_long
from io_control import set_io_i2c, init_io, led_rd_on, measure_vbatt
from io_control import pmic_ce, get_charger_status
from network import LTE
​
pycom.heartbeat(False)
​
while False:
    pycom.rgbled(0xFF0000)  # Red
    time.sleep(1)
    pycom.rgbled(0x00FF00)  # Green
    time.sleep(1)
    pycom.rgbled(0x0000FF)  # Blue
    time.sleep(1)

if False:
    lte = LTE(carrier="verizon")
    imei = lte.imei()
    print(imei)

if False:
    adc = machine.ADC()             # create an ADC object
    apin = adc.channel(pin='P13',attn=machine.ADC.ATTN_0DB)   # create an analog pin on P13
    val = apin()                    # read an analog value
    print(val)
    volt = apin.voltage()
    print(volt)

if False:
    #i2c = I2C(0, pins=('P9','P10'))     # create and use non-default PIN assignments (P9=SDA, P10=SCL)
    #i2c.init(I2C.MASTER, baudrate=1000) # init as a master
    i2c = I2C(0)
    sda = 'P9'
    scl = 'P3'
    i2c.init(I2C.MASTER, baudrate=5000, pins=(sda,scl))

    set_gps_i2c(i2c)
    disable_nmea_messages()
    time.sleep(1)
    loopcount = 3
    while loopcount > 0:
        loopcount -= 1
        lat,ns,long,ew = get_lat_long()
        print(lat)
        print(ns)
        print(long)
        print(ew)
        # receiver_on(False)
        print("Receiver off. (Waiting 5 seconds.)")
        time.sleep(5)
        lat,ns,long,ew = get_lat_long()
        print(lat)
        print(ns)
        print(long)
        print(ew)
        receiver_on(True)
        print ("Receiver on.")
        time.sleep(4)

#Get Satellites in request_satellites_in_view
if False:
    i2c = I2C(0)
    sda = 'P9'
    scl = 'P3'
    i2c.init(I2C.MASTER, baudrate=1000, pins=(sda,scl))
    set_io_i2c(i2c)
    init_io()
    set_gps_i2c(i2c)
    disable_nmea_messages()
    while True:
        info = request_satellites_in_view()
        print('----')
        print(info)
        time.sleep(5)


#command to invert antenna enable
#Sent one time.
if False:
    i2c = I2C(0)
    sda = 'P9'
    scl = 'P3'
    i2c.init(I2C.MASTER, baudrate=10000, pins=(sda,scl))
    i2c.writeto(0x42,bytearray([0xB5, 0x62, 0x06, 0x41, 0x0C, 0x00, 0x00, 0x00, 0x03, 0x1F, 0x90, 0x47, 0x4F, 0xB1, 0xFF, 0xFF, 0xEA, 0xFF, 0x33, 0x98]))

# I/O Expander
if False:


    #command = bytearray([0xB5, 0x62])
    i2c.writeto(0x20, 0x05 , stop=False) #0x21 read, 0x20 write, 0x06 configuration port 0
    #print("Wait 3 sec")
    #time.sleep(0.01)
    buf = bytearray(2)
    i2c.readfrom_into(0x20, buf)
    print(buf)

# I/O control
if True:
    i2c = I2C(0)
    sda = 'P9'
    scl = 'P3'
    i2c.init(I2C.MASTER, baudrate=5000, pins=(sda,scl))
    set_io_i2c(i2c)
    init_io()
    led_rd_on(True)
    time.sleep(1)
    led_rd_on(False)
    measure_vbatt()
    pmic_ce(True)
    time.sleep(15)
    pmic_ce(False)
    get_charger_status()

#change to test github
#change added to b1
#2nd change added to b1