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
payload = {}
index = 1
tofile=[]

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

try:
        lcd = FaBoLCD_PCF8574.PCF8574(0x27)
        lcd.begin(20,4)
        lcd.lcd_write( LCD_NOBACKLIGHT )
#        lcd.write("BluGraphTechnologies")
except:
        print"LCD Error"
        pass

client= ModbusClient(method = "rtu", port="/dev/ttyUSB0", stopbits = 1, bytesize = 8, parity = 'E', baudrate= 19200)
connection = client.connect()
print "RDO PRO-X Connection : ", client, "\n"
              # Read RDO-PROX             
address = 0x0000
payload[fieldname[0]] = config['DEVICE_ID']
print(datetime.datetime.now())
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y  %H:%M:%S')
payload[fieldname[1]] =st
result = None
cond="0000"
rest="0000"
tdsd="0000"
clpl="0000"
t2=0
t3=0
t4=0
t5=0
t8=0
t11=0
t12=0
clplf=0

try:
        result = client.read_input_registers(address,32,unit=0x01)
except:
        print"Comms with Reader failed"
        pass
try:
        t2 = float(result.registers[1]/100.0)
        print "Water Temperature", t2, "degC"
        t3 = float(result.registers[2]/100.0)
        print "pH Value", t3
        t4 = float(result.registers[3]/10.0)
        print "ORP", t4,"mV"
        t5 = float(result.registers[4]/10.0)
        print "Turbidity", t5, "NTU"
        t8 = float(result.registers[13]/100.00)
        print "Salinity", t8, "PSU"
        t11 = float(result.registers[17]/100.0)
        print "Diss.Oxyg.", t11,"mg/L"
        t12 = result.registers[18]
        print "Depth", t12, "cm"
        clpl= struct.pack('>HH', result.registers[30], result.registers[31])
        clpl1= struct.unpack('>f',clpl)
        clpl2= (clpl1)[0] * 1
        clplf= (round(clpl2,2))
        print "Chlorophyl", clplf,"mg/L"
except:
        print"Sensor Not Connected"
        pass

payload[fieldname[3]] = t2
payload[fieldname[6]] = t3
payload[fieldname[9]] = t4
payload[fieldname[8]] = t5
payload[fieldname[7]] = t8
payload[fieldname[2]] = t11
payload[fieldname[5]] = t12
payload[fieldname[4]] = clplf

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


try:
  for x in range (0,14):
        lcd.clear()
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        lcd.setCursor(0,0)
        l1=st +" T:"+str(int(t2))+" C"
        lcd.write(l1)
        lcd.setCursor(0,1)
        l2="DO:"+str(round(t11,1))+"mg/L"
        lcd.write(l2)
        lcd.setCursor(0,2)
        l3="Sal:"+str(int(t8))+" NTU"
        lcd.write(l3)
        lcd.setCursor(0,3)
        l4="Depth:"+str(round(t12/1000,1))+"m"
        lcd.write(l4)

        time.sleep(10)
        lcd.clear()

        lcd.setCursor(0,0)
        l1="ORP:"+str(round(t4,0))+"mV"
        lcd.write(l1)
        lcd.setCursor(0,1)
        l2="pH:"+str(round(t3,1))
        lcd.write(l2)
        lcd.setCursor(0,2)
        l3="Turb:"+str(round(t5,1))+"mg/L"
        lcd.write(l3)
        lcd.setCursor(0,3)
        l4="Chl:"+str(round(clplf,1))+"ug/L "
        lcd.write(l4)
        time.sleep(10)
except:
        print"LCD Error"
        pass









