import time
import sys
import numpy as np
import cv2
import time
import threading
import video
#import ble
import ble_test4

def bleStart():
        #ble = ble.MyBle.instance()
	ble = ble.Ble()
	time.sleep(1)
	ble.readValueInf()

def videoStart():
	video = video.Video()
	time.sleep(1)
	video.nextFrame()
	video.testBackgroundFrame()

	while 1:
		video.nextFrame()
		video.testBackgroundFrame()
		video.updateBackground()
		video.compare()
		video.showFrame()
		video.testSettings()
		if video.testDestroy():
			sys.exit()


t1 = threading.Thread(target=bleStart)
t1.start()
print ("thread 1: BLE Start!")

time.sleep(5)

t2 = threading.Thread(target=videoStart)
t2.start()
print ("thread 2: Video Start!")