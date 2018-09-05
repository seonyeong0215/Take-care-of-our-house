#!/usr/bin/env python
# Fall detector webservice
#
# Kim Salmi, kim.salmi(at)iki(dot)fi
# http://tunn.us/arduino/falldetector.php
# License: GPLv3

import requests

class Webservice(object):
	
	def __init__(self, place, phone):
            #http://ec2-54-180-8-72.ap-northeast-2.compute.amazonaws.com/test.php?place='+place+'&phone='+phone	
		#self.url = 'http://tunn.us/tools/healthservice/add.php?place='+place+'&phone='+phone
		#self.url = 'http://salmi.pro/ject/fall/add.php?place='+place+'&phone='+phone
		#self.url = 'http://ec2-54-180-8-72.ap-northeast-2.compute.amazonaws.com/test.php?place='+place+'&phone='+phone
		self.url = 'http://ec2-54-180-8-72.ap-northeast-2.compute.amazonaws.com/test.php'
		self.data = 'test'

	def alarm(self, detectiontype, personid):
		#tempurl = self.url
		#tempurl = tempurl+'&type='+detectiontype+'&personid='+str(personid)
		#response = requests.get(tempurl, data=self.data)
		response = requests.get(self.url, data=self.data)
		print self.url
		print self.data
		print response