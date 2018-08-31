import sys
import binascii
import struct
import time
import bluepy
import threading

#2. binary to float

def bin_to_float(binary):
    return struct.unpack('f', binary)
    #return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

class Ble:

	#1. bluetooth

	def __init__(self):
		self.bt = "C5:53:1E:89:9A:16"
		print (self.bt)

		p = bluepy.btle.Peripheral(self.bt,"random")
		services = p.getServices()		 
		for service in services:
		   print (service)

		self.bi_service_uuid = "2220"
		print (self.bi_service_uuid)
		self.biService = p.getServiceByUUID(self.bi_service_uuid)
		print (self.biService)

		chList = self.biService.getCharacteristics()
		print ("Handle   UUID                                Properties")
		print ("-------------------------------------------------------")
		for ch in chList:
		    print ("  0x" + format(ch.getHandle(),'02X') + "   " + str(ch.uuid) + " " + ch.propertiesToString())

		self.bi_char_uuid = "00002221-0000-1000-8000-00805f9b34fb"
		print (self.bi_char_uuid)

	def readValueInf(self):
		self.vals = {'temp':0, 'bpm':0}

		try:
                    sensorValue = self.biService.getCharacteristics(self.bi_char_uuid)[0]
                    while 1:
                        val = sensorValue.read()
                        print (val)
                        
                        val = struct.unpack('f', val)[0]
                        print (val)
                        
                        time.sleep(0.5)
		
		finally:
                    pass

	def getValue(self):
		return self.vals


'''
	main part
'''
def bleStart():
    ble = Ble()
    time.sleep(1)
    ble.readValueInf()

t1 = threading.Thread(target=bleStart)
t1.start()
print ("thread 1: BLE Start!")