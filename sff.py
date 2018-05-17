import os
import sys
import time
import json
from os import listdir
from os.path import isfile, join
import glob, os
import requests
#import cPickle as pickle
import pickle

file_list = []

with open('/home/arkbg/dev/config/BG_Config.json', 'r') as config_file:
    # Convert JSON to DICT
    config = json.load(config_file)
print config['DEVICE_ID']
# Build destination server path
SERVER_PATH = "http://" + config['SERVER_ADDR'] + config['FAIL_PATH']
print SERVER_PATH

dir_name = "/home/arkbg/dev/data"

os.chdir(dir_name)
for file in glob.glob("*.dat"):
    file_list.append(file)

# print file_list
if len(file_list) == 0:
    print "There are no files in the directory"
    print "Nothing to do, Exit"
else:
    print "There are " + str(len(file_list)) + " files in the directory"
    for k in range(0, len(file_list)):
        data2 = []
        print file_list[k]
        with open(file_list[k], 'r') as data_file:
                for line in data_file:
                        data2.append(json.loads(line))
        print data2
        try:
                r1 = requests.put(SERVER_PATH, data=json.dumps(data2), timeout=1)
                print r1.status_code
                if r1.status_code==200:
                        try:
                                os.remove(file_list[k])
                                print "File Successfully uploaded removed"
                        except OSError, e:  ## if failed, report it back to the user ##
                                print ("File could not be removed Error: %s - %s." % (e.filename, e.strerror))
                                pass
        except:
                print "Network Failed Error:"
                sys.exit()
    print "All files Tried to send"



