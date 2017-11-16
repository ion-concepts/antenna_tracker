#!/usr/bin/env python

import maestro
import time

X_AXIS = 0
Y_AXIS = 1
X_CENTER = 5984
Y_CENTER = 5984

def wait_for_stop(axis):
    while(servo.isMoving(axis)):
        pass

servo = maestro.Controller()
servo.setSpeed(X_AXIS, 1)
servo.setSpeed(Y_AXIS, 1)
servo.setTarget(X_AXIS, X_CENTER)  #set servo to move to center position
wait_for_stop(X_AXIS)
servo.setTarget(Y_AXIS, Y_CENTER)  #set servo to move to center position
wait_for_stop(Y_AXIS)
servo.close
