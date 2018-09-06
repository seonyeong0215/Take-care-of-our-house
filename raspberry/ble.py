import sys
import binascii
import struct
import time
import bluepy
import webservice

class Ble:
	def __init__(self):
		self.bt = "C5:53:1E:89:9A:16"
		print(self.bt)

		p = bluepy.btle.Peripheral(self.bt,"random")
		services = p.getServices()		 
		for service in services:
			print(service)

		self.bi_service_uuid = "2220"
		print(self.bi_service_uuid)
		self.biService = p.getServiceByUUID(self.bi_service_uuid)
		print(self.biService)

		chList = self.biService.getCharacteristics()
		print("Handle   UUID                                Properties")
		print("-------------------------------------------------------")
		for ch in chList:
			print("  0x" + format(ch.getHandle(),'02X') + "   " + str(ch.uuid) + " " + ch.propertiesToString())

		self.bi_char_uuid = "00002221-0000-1000-8000-00805f9b34fb"
		print(self.bi_char_uuid)

		self.webservice = webservice.Webservice()

	def readValueInf(self):
		prevTime = time.gmtime(time.time()).tm_hour
		self.avgs = {'temp':{'avg':0, 'n':0}, 'bpm':{'avg':0, 'n':0}}
		self.vars = {'temp':0, 'bpm':0}

		sensorValue = self.biService.getCharacteristics(self.bi_char_uuid)[0]
		while 1:
			# 1. Read Vars & Get Avgs
			val = 0

			# temp < 0
			while val >= 0:
				val = binToFloat(sensorValue.read())
			self.vars['temp'] = val * -1
			calAvg(self.avgs['temp'], self.vars['temp'])
			
			# bpm >= 0
			while val <= 0:
				val = binToFloat(sensorValue.read())
			self.vars['bpm'] = val
			calAvg(self.avgs['bpm'], self.vars['bpm'])

			# 2. Send Avgs
			curTime = time.gmtime(time.time()).tm_hour
			if curTime != prevTime:
				self.webservice.stat(self.avgs['temp']['avg'], self.avgs['bpm']['avg'])
				prevTime = curTime
				self.avgs['temp']['avg'] = self.avgs['temp']['n'] = 0
				self.avgs['bpm']['avg'] = self.avgs['bpm']['n'] = 0

			time.sleep(0.2)

	def getValue(self):
		return self.vars

def binToFloat(binary):
    return struct.unpack('f', binary)[0]

def calAvg(var, value):
	var['avg'] = var['avg'] - ((var['avg'] - value) / (var['n'] + 1))
	var['n'] += 1 

'''
	Ble Class -> Singleton
'''

class SingletonInstance:
	__instance = None

	@classmethod
	def __getInstance(cls):
		return cls.__instance

	@classmethod
	def instance(cls, *args, **kargs):
		cls.__instance = cls(*args, **kargs)
		cls.instance = cls.__getInstance
		return cls.__instance

class MyBle(Ble, SingletonInstance):
	pass

# vars = MyBle.instance().getValue()