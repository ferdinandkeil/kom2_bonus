#!/usr/bin/env python

"""
	YASPUtin

	Yet
	Another
	Simple
	Plugwise
	Uploader
	tin :)

	This simple tool fetches data from multiple Plugwise Circles and uploads
	it to EmonCMS.

	Configuration file has to be saved as yasputin_conf.json.
	Example configuration file:

		{
			"circle+": "B1BDD3",
			"circles": [
				"D36601",
				"B82E27"
			],
			"emoncms-apikey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
			"emoncms-url": "emoncms.org",
			"serial-port": "COM3",
			"update-interval": 10
		}

"""

from serial.serialutil import SerialException
import json
from time import sleep
import sys
import requests
from plugwise import *
from datetime import datetime
from string import Template

# Read config-file
try:
	json_config = open('yasputin_conf.json', 'r+')
except IOError:
	print('Error: Could not find yasputin_conf.json!')
	sys.exit(-1)
else:
	with json_config:
		config = json.load(json_config)
		# Rewrite config-file to convert it to the standard formatting
		json_config.seek(0)
		json.dump(config, json_config, sort_keys=True, indent=4, separators=(',', ': '))


# Check for settings
if not 'circle+' in config:
	print('Error: The configuration file is missing the MAC of the Circle+!')
	sys.exit(-1)
if not 'serial-port' in config:
	print('Error: The configuration file is missing the COM-port setting!')
	sys.exit(-1)
if not 'emoncms-url' in config:
	print('Error: The configuration file is missing the URL of your EmonCMS installation!')
	sys.exit(-1)
if not 'emoncms-apikey' in config:
	print('Error: The configuration file is missing the API-key of you EmonCMS installation!')
	sys.exit(-1)
if not 'update-interval' in config:
	config['update-interval'] = 10
if 'circles' in config:
	config['circles'] = [x for x in config['circles'] if x != config['circle+']]
	config['circles'] = list(set(config['circles'])) # remove duplicates
	if len(config['circles']) == 0:
		print('Warning: You have not configured any additional circles.')

# Create objects for the stick and all the circles
try:
	stick = Stick(config['serial-port'])
	circleplus = Circle('000D6F0000' + config['circle+'].encode('ascii'), stick)
	circles = {config['circle+']: circleplus}
	for circle in config['circles']:
		circles[circle] = Circle('000D6F0000' + circle.encode('ascii'), stick)
except SerialException as reason:
	print("Error: %s" % (reason,))
	sys.exit(-1)


# Read the actual data from the devices and transfer it to EmonCMS
while 1:

	print(datetime.now().isoformat())

	powerUsages = {}

	for mac, circle in circles.iteritems():
		try:
			powerUsage = round(circle.get_power_usage(), 2)
		except ValueError:
			print("Error: Failed to read power usage (MAC %s)!" % mac)
		except TimeoutException as reason:
			print("Error: %s (MAC %s)!" % (reason, mac))
		else:
			powerUsages[mac] = powerUsage
			print("Power usage (%s): %.2fW" % (mac, powerUsages[mac]))

	# Upload data to EmonCMS
	reqUrl = Template('http://$url/input/post.json?json={$json}&apikey=$apikey').substitute({'url': config['emoncms-url'], 'json': json.dumps(powerUsages), 'apikey': config['emoncms-apikey']})
	req = requests.get(reqUrl)
	print('Upload status: {}/{}'.format(req.status_code, req.text))

	sleep(config['update-interval'])