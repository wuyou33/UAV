'''
Created on Aug 15, 2013

@author: ejracah
'''

"""from imu import IMU
from sensor_class import Sensor"""

from imu import IMU
from robovero.extras import roboveroConfig
import time
from ComplementaryFilter import ComplementaryFilter
from motor import Motor
from PID import PIDControl
import signal
import sys
import thread

roboveroConfig()

# Initialize IMU
imu = IMU()

#imu.calibrate(0, 0, -1)
cfRoll = ComplementaryFilter(0.9, 0)
cfPitch = ComplementaryFilter(0.9, 0)

m = Motor(4)

m.setSpeed(1000)
m.go()
time.sleep(1)
m.setSpeed(0)
m.go()
time.sleep(1)


pitchPID = PIDControl(0, [0.168, 0.654 ,0.008])
#rollPID = PIDControl(0, [1, 0 ,0])

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    for m in motors:
        m.setSpeed(0)
        m.go()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def getInput(PIDControl):
	angle = 0
	while(1):
		angle = raw_input('Set desired angle: ')
		PIDControl.set_set_point(int(angle))
try:
	thread.start_new_thread(getInput, (pitchPID, ))
except:
	print "error: unable to start thread"

while(1):
	m.setSpeed(100)
	m.go()
	time.sleep(5)
	   
