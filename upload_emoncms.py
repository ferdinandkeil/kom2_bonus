import requests
from time import sleep
from serial.serialutil import SerialException
from plugwise import *

try:
	device = Stick('COM3')
	c = Circle('000D6F0000B1BDD3', device)
except SerialException as reason:
	print("Error: %s" % (reason,))
	exit()

while 1:

	try:
		powerUsage = c.get_power_usage()
	except ValueError:
		print("Error: Failed to read power usage")
		exit()
	except TimeoutException as reason:
		print("Error: %s" % (reason,))
		exit()

	print("power usage: %.2fW" % (c.get_power_usage(),))

	r = requests.get('http://emoncms.org/input/post.json?json={{power:{}}}&apikey=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'.format(powerUsage))
	print 'upload: ' + r.text

	sleep(10)