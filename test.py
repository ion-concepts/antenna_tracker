#!/usr/bin/env python

import maestro
import time, math

X_AXIS = 0
Y_AXIS = 1
X_CENTER = 5984
Y_CENTER = 5984

SPEED = 1

def wait_for_stop(axis):
    while(servo.isMoving(axis)):
        pass
    #time.sleep(math.log10(SPEED) + 2)

servo = maestro.Controller()
print dir(servo)

#print "Y Min: ", servo.getMin(Y_AXIS)
#print "Y Max: ", servo.getMax(Y_AXIS)
#print "X Min: ", servo.getMin(X_AXIS)
#print "X Max: ", servo.getMax(X_AXIS)

servo.setAccel(X_AXIS, 1)
servo.setSpeed(X_AXIS, SPEED)

servo.setTarget(X_AXIS, X_CENTER)  #set servo to move to center position
wait_for_stop(X_AXIS)

for x in xrange(X_CENTER, X_CENTER+1000):
    servo.setTarget(X_AXIS, x) # full rotation
    wait_for_stop(X_AXIS)
    
#servo.setTarget(X_AXIS, 7000) # full rotation
#wait_for_stop(X_AXIS)

#for i in xrange(4):
#    servo.setTarget(X_AXIS, 6300)
#    wait_for_stop(X_AXIS)
#    servo.setTarget(X_AXIS, 5700)
#    wait_for_stop(X_AXIS)

servo.setTarget(X_AXIS, X_CENTER)
wait_for_stop(X_AXIS)
servo.close
