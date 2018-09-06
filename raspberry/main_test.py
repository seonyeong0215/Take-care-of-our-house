import time
import sys
import numpy as np
import cv2
import time
import threading
import video
import ble

def bleStart():
	myble = ble.MyBle.instance()
	time.sleep(1)
	myble.readValueInf()

def videoStart():
	myvideo = video.Video()
	time.sleep(1)
	myvideo.nextFrame()
	myvideo.testBackgroundFrame()

	while 1:
		myvideo.nextFrame()
		myvideo.testBackgroundFrame()
		myvideo.updateBackground()
		myvideo.compare()
		myvideo.showFrame()
		myvideo.testSettings()
		if myvideo.testDestroy():
			sys.exit()


t1 = threading.Thread(target=bleStart)
t1.start()
print("thread 1: BLE Start!")

time.sleep(3)

t2 = threading.Thread(target=videoStart)
t2.start()
print("thread 2: Video Start!")


'''
	server test
'''

time.sleep(3)

import webservice

web = webservice.Webservice()
web.alarmToFall(36, 120)