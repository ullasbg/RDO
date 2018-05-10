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
from pymodbus.constants import Defaults

# Read Configuration JSON file
with open('/home/arkbg/dev/config/BG_Config.json', 'r') as config_file:
    # Convert JSON to DICT
    config = json.load(config_file)
print config['DEVICE_ID']
# Build destination server path
SERVER_PATH = "http://" + config['SERVER_ADDR'] + config['SERVER_PATH']
print SERVER_PATH

#Defaults.Timeout = 15

payload = {}
index = 1
lcd = FaBoLCD_PCF8574.PCF8574(0x27)
lcd.begin(20,4)
lcd.write("BluGraphTechnologies")

fieldname = ["Station_ID",
             "Time",
             "rdo",
             "Temp"]

client= ModbusClient(method = "rtu", port="/dev/ttyAMA0", stopbits = 1, bytesize = 8, parity = 'E', baudrate= 19200)
connection = client.connect()
print "RDO PRO-X Connection : ", client, "\n"
              # Read RDO-PROX             
address = 0x0025
payload[fieldname[0]] = config['DEVICE_ID']
while True:
        lcd.setCursor(0,1)
        print(datetime.datetime.now())
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y  %H:%M:%S')
        payload[fieldname[index]] =st
        index=index+1
        lcd.write(st)
        result = None
        raw1="0000"
        raw="0000"
        try:
                result = client.read_holding_registers(address,24,unit=0x01)
#               time.sleep(3) 
#               result = client.read_holding_registers(address,24,unit=0x01)
        except:
                print"Comms with Reader failed"
                pass
        try:
                raw = struct.pack('>HH', result.registers[0], result.registers[1])
                raw1= struct.pack('>HH', result.registers[8], result.registers[9])
        except:
                print"No Reg"
                pass
        val = struct.unpack('>f', raw)
        val1= struct.unpack('>f', raw1)
        result_val = (val)[0] * 1
        result_val1=(val1)[0] * 1
        do= (round(result_val,2))
        payload[fieldname[index]] =do
        index=index+1
        do="DissolvedOxygen:"+str(do)
        print do
        lcd.setCursor(0,2)
        lcd.write(do)
        temp= (round(result_val1,2))
        payload[fieldname[index]] =temp
        index=1
        temp = "Temperature   :"+str(temp)
        print temp
        lcd.setCursor(0,3)
        lcd.write(temp)
        dev_json= json.dumps(payload, sort_keys=True)
        print dev_json
        try:
# Send JSON to server
                r1 = requests.put(SERVER_PATH, data=dev_json)
                print r1.status_code
        except:
                print"Server Comms Error"
                pass

#       time.sleep(20)







