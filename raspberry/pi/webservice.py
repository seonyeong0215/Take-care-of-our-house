import requests
from datetime import datetime

class Webservice(object):
	def __init__(self):
		self.myurl = 'http://ec2-54-180-8-72.ap-northeast-2.compute.amazonaws.com'
		self.urlStat = self.myurl + '/RegisterAvg.php'
		self.urlAlarm = self.myurl + '/RegisterAlarm.php'

	def stat(self, avgTemp, avgBpm):
		time = self.getTime()
		params = {'avgTemp':avgTemp, 'avgBpm':avgBpm, 'time':time}
		response = requests.get(self.urlStat, params=params)
		print(response)

	'''
		0 : not moving
		1 : fall
		2 : abnormal temperature
		3 : abnormal bpm
	'''

	def alarm(self, status, temp, bpm):
		time = self.getTime()
		params = {'status': status, 'temp':temp, 'bpm':bpm, 'time':time}
		response = requests.get(self.urlAlarm, params=params)
		print(response)

	def alarmToNotMoving(self, temp, bpm):
		self.alarm(0, temp, bpm)

	def alarmToFall(self, temp, bpm):
		self.alarm(1, temp, bpm)

	def alarmToAbnormalTemp(self, temp, bpm):
		self.alarm(2, temp, bpm)

	def alarmToAbnormalBpm(self, temp, bpm):
		self.alarm(3, temp, bpm)

	def getTime(self):
		now = datetime.now()
		time = ''
		if now.hour <= 9 and now.hour >= 0:
			time += '0'
		time += str(now.hour)
		time += ':'
		if now.minute <= 9 and now.minute >= 0:
			time += '0'
		time += str(now.minute)