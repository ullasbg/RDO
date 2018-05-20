import FaBoLCD_PCF8574
import time
import sys
import datetime
import time
import serial
import requests
import json
import string
import pymodbus
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
import struct
import RPi.GPIO as GPIO
import os

i = 0
lcd = FaBoLCD_PCF8574.PCF8574(0x27)

lcd.write("BluGraphTechnologies")

try:
    while True:
        lcd.setCursor(0,1)
        lcd.write(i)
        print(datetime.datetime.now())
        lcd.setCursor(0,2)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y  %H:%M:%S')
        lcd.write(st)
        i += 1
        time.sleep(.95)
except:
    pass




