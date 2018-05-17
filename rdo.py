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
tofile=[]
payload = {}
index = 1
try:
        lcd = FaBoLCD_PCF8574.PCF8574(0x27)
        lcd.begin(20,4)
        lcd.write("BluGraphTechnologies")
except:
        print"LCD Error"
        pass

fieldname = ["Station_ID",
             "Time",
             "rdo",
             "Temp"]

client= ModbusClient(method = "rtu", port="/dev/ttyUSB0", stopbits = 1, bytesize = 8, parity = 'E', baudrate= 19200)
connection = client.connect()
print "RDO PRO-X Connection : ", client, "\n"
              # Read RDO-PROX             
address = 0x0025
payload[fieldname[0]] = config['DEVICE_ID']

print(datetime.datetime.now())
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y  %H:%M:%S')
payload[fieldname[index]] =st
index=index+1

try:
        lcd.setCursor(0,1)
        lcd.write(st)
except:
        print"LCD Error"
        pass

result = None
result1=None
raw1="0000"
raw="0000"
try:
        result = client.read_holding_registers(address,24,unit=0x01)
        time.sleep(1)
        result1 = client.read_holding_registers(address,24,unit=0x01)
#       time.sleep(1)
#        result1 = client.read_holding_registers(address,10,unit=0x01)
except:
        print"Comms with Reader failed"
        pass
try:
        raw = struct.pack('>HH', result1.registers[0], result1.registers[1])
        raw1= struct.pack('>HH', result1.registers[8], result1.registers[9])
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
try:
        lcd.setCursor(0,2)
        lcd.write(do)
except:
        print"LCD Error"
        pass

temp= (round(result_val1,2))
payload[fieldname[index]] =temp
index=1
temp = "Temperature   :"+str(temp)
print temp
try:
        lcd.setCursor(0,3)
        lcd.write(temp)
except:
        print"LCD Error"
        pass

dev_json= json.dumps(payload, sort_keys=True)
print dev_json

tofile.append(payload)
dir_name= "/home/arkbg/dev/data/"
try:
        os.makedirs(dir_name)
except OSError:
        if os.path.exists(dir_name):
                print ": Already directory exists"
        else:
                print ": Some system Error in creating directory"
try:
        base_filename=time.strftime("%d%m%Y")
        abs_file_name=os.path.join(dir_name, base_filename + "." + "txt")
        f = open(abs_file_name, 'a')
        print>>f, json.dumps(payload)
        f.close()
except:
        print"Error : File not written"
        pass

try:
        r1 = requests.put(SERVER_PATH, data=dev_json)
        print r1.status_code
except:
        print"Server Comms Error"
        try:
                base_filename=time.strftime("%d%m%Y")
                abs_file_name=os.path.join(dir_name, base_filename + "ns." + "dat")
                f = open(abs_file_name, 'a')
                print>>f, json.dumps(tofile)
                f.close()
        except:
                print"Error : NS File not written"
                pass
        pass
del tofile[:]





