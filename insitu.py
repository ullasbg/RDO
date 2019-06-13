import time
import sys
import datetime
import time
import serial
import requests
import json
import string
import pymodbus
import struct
import RPi.GPIO as GPIO
import os

# Read Configuration JSON file
with open('/home/arkbg/dev/config/BG_Config.json', 'r') as config_file:
    # Convert JSON to DICT
    config = json.load(config_file)
print config['DEVICE_ID']
# Build destination server path
SERVER_PATH = "http://" + config['SERVER_ADDR'] + config['SERVER_PATH']
SERVER_PATH2 = "http://" + config['SERVER_ADDR'] + "/rdbat.php"
print SERVER_PATH
print SERVER_PATH2
payload = {}
index = 1
tofile=[]

payload2 = {}

fieldname0 = ["deviceID",
              "battvolt"]

fieldname = ["Station_ID",
             "Time",
             "rdo",
             "Temp",
             "Chloro",
             "Depth",
             "pH",
             "Salinity",
             "Turbid",
             "Orp"]

ser=serial.Serial('/dev/ttyAMA0',9600) 

payload[fieldname[0]] = config['DEVICE_ID']
payload2[fieldname0[0]] = config['DEVICE_ID']
print(datetime.datetime.now())
t=[]
resp=""
ser.write("R")
while (ser.in_waiting==0):
#       print "Waiting for response"
        time.sleep(1)

if (ser.in_waiting>0):
                try:    
                        resp=ser.read_until("\n")
                except:
                        print "Serial Read Error"
                print resp
                list=resp.split(",")
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y  %H:%M:%S')
                payload[fieldname[1]] =st
                payload[fieldname[2]] = float(list[2])
                payload[fieldname[3]] = float(list[1])
                payload[fieldname[4]] = float(list[6])
                payload[fieldname[5]] = float(list[7])
                payload[fieldname[6]] = float(list[3])
                payload[fieldname[7]] = float(list[5])
                payload[fieldname[8]] = 0
                payload[fieldname[9]] = float(list[4])
                dev_json= json.dumps(payload, sort_keys=True)
                payload2[fieldname0[1]] = float(list[8])
                dev_json2= json.dumps(payload2, sort_keys=True)
                print dev_json
                print dev_json2
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
                        print "Sending Batt to Server"
                        r2 = requests.put(SERVER_PATH2, data=dev_json2, timeout=1)
                        print r2.status_code
                except:
                        print"Batt Server Comms Error"
                try:
# Send JSON to server
                        print "Sending to Server"
                        r1 = requests.put(SERVER_PATH, data=dev_json, timeout=1)
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
                del list[:]

#else:
#               time.sleep(1)
#               print "Waiting on Sensor reading"




