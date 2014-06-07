#!/usr/bin/env python

import os
import RPi.GPIO as GPIO
import glob
import time
import urllib, httplib
import threading
 

#check temperature probe addresses
def query_probes():
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')
	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28*')[0]
	device_file = device_folder + '/w1_slave'
 
#send information to ThingSpeak API
def write(p0,p1,p2,p3,p4,p5):
	params = urllib.urlencode({'field1': p0, 'field2': p1, 'field3':p2, 'field4':p3, 'field5':p4,'field6':p5, 'key':'[YOUR KEY HERE]'})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("api.thingspeak.com:80")
	conn.request("POST", "/update", params, headers)
	response = conn.getresponse()
	print response.status, response.reason
	data = response.read()
	global bub1
	bub1 = 0
	global bub2
	bub2 = 0
	global bub3
	bub3 = 0
	global dd
	dd = 0
	conn.close()
 
#read temperature sensors
def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines
 
#get usable numbers from temperature sensors
def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_f,0,0
		
#self-calling loop that initiates ThingSpeak API regularly
def looploop():
		global temp1
		global temp2
		global temp3
		global bub1
		global bub2
		global bub3
		#initite ThingSpeak API
		write(temp1,temp2,temp3,bub1,bub2,bub3)
		print "Written"
		print temp1
		#reset bubble counters to 0
		bub1 = 0
		bub2 = 0
		bub3 = 0
		#schedule the next loop
		threading.Timer(300.0, looploop).start()
		
GPIO.setmode(GPIO.BCM)

#bubbler tuning
BT1 = 20
        
#Define RasPi Pins
##pins for temperature probes
TMP1 = 4

#Set up pins
##set up pins for temperature probes
GPIO.setup(TMP1, GPIO.IN)

#Set up global variables
temp1 = 0
temp2 = 0
temp3 = 0
bub1 = 0
bub2 = 0
bub3 = 0

#fetch data from sensors
temp = read_temp()
#bub = readbubblers()
temp1 = temp[0]
temp2 = temp[1]
temp3 = temp[2]
#bub1 = bub1 + bub[0]
#bub2 = bub2 + bub[1]
#bub3 = bub3 + bub[2]

looploop()
#begin main loop
while True:
        #fetch data from sensors
		temp = read_temp()
		#bub = readbubblers()
		temp1 = temp[0]
		temp2 = temp[1]
		temp3 = temp[2]
		#bub1 = bub1 + bub[0]
		#bub2 = bub2 + bub[1]
		#bub3 = bub3 + bub[2]
