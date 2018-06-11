from time import sleep
from widgetlords.pi_spi import *
from widgetlords import *
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

with open('/home/arkbg/dev/config/BG_Config.json', 'r') as config_file:
    # Convert JSON to DICT
    config = json.load(config_file)
print (config['DEVICE_ID'])
# Build destination server path
SERVER_PATH = "http://" + config['SERVER_ADDR'] + config['SERVER_PATH']
print (SERVER_PATH)
payload = {}
index = 1
tofile=[]

fieldname = ["Station_ID",
             "Time",
             "rdo",
             "Temp",
             "Chloro",
             "Depth",
             "pH"]

payload[fieldname[0]] = config['DEVICE_ID']
print(datetime.datetime.now())
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y  %H:%M:%S')
payload[fieldname[1]] =st

init()
inputs = Mod8AI()

while True:
    for x in range(0, 8):
        adc=(inputs.read_single(x))
        if (adc<5):
            adc=0
            print (adc)
        else:
            print ("next")
            print('{:f}'.format(adc))
            curr = counts_to_value(adc,745,3723,4,20)
            print('{:f}'.format(curr))
            depth = float(((curr-4)/16)*10)
            print('{:f}'.format(depth)), "m"
            sleep(1)


dev_json= json.dumps(payload, sort_keys=True)
print (dev_json)

tofile.append(payload)
dir_name= "/home/arkbg/dev/data/"
try:
        os.makedirs(dir_name)
except OSError:
        if os.path.exists(dir_name):
                print (": Already directory exists")
        else:
                print (": Some system Error in creating directory")
try:
        base_filename=time.strftime("%d%m%Y")
        abs_file_name=os.path.join(dir_name, base_filename + "." + "txt")
        f = open(abs_file_name, 'a')
        print>>f, json.dumps(payload)
        f.close()
except:
        print("Error : File not written")
        pass

try:
# Send JSON to server
        print ("Nothing")
        r1 = requests.put(SERVER_PATH, data=dev_json, timeout=1)
        print (r1.status_code)
except:
        print("Server Comms Error")
        try:
                base_filename=time.strftime("%d%m%Y")
                abs_file_name=os.path.join(dir_name, base_filename + "ns." + "dat")
                f = open(abs_file_name, 'a')
                print>>f, json.dumps(tofile)
                f.close()
        except:
                print("Error : NS File not written")
                pass
        pass
del tofile[:]








