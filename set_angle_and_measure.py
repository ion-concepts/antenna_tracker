#!/usr/bin/env python

import maestro
import time, math

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from optparse import OptionParser
import sys

X_AXIS = 0
Y_AXIS = 1
X_CENTER = 6010
Y_CENTER = 5984
TO_DEGREES = 2.7 #1100/360

SPEED = 1
ACCEL = 1



# Call this code with a radial angle.
# Antenna "turntable" is rotated to angle.
# Returns a uniqely named file with a stream of rssi values for this angle.

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-o", "--lo-offset", dest="lo_offset", type="eng_float", default=eng_notation.num_to_str(125e3),
        help="Set lo_offset frequency in Hz [default=%default]")
    parser.add_option("-f", "--rx_freq", dest="rx_freq", type="eng_float", default=eng_notation.num_to_str(3100.0),             
        help="Set receive frequency in MHz [default=%default]")
    parser.add_option("-g", "--rx-gain", dest="rx_gain", type="eng_float", default=eng_notation.num_to_str(50),
        help="Set rx_gain [default=%default]")
    parser.add_option("", "--usrp-addr", dest="usrp_addr", type="string", default="type=b200",
        help="Set usrp_addr [default=%default]")
    parser.add_option("-a", "--angle", dest="angle", type="eng_float", default=0.0,
        help="Set angle of turntable [default=%default]")
    parser.add_option("-c", "--rssi-count", dest="rssi_count", type="intx", default=1024,
        help="Count of RSSI values to capture [default=%default]")
    parser.add_option("-F", "--file_prefix", dest="file_prefix", type="string",
                      default="rssi_angle_",
        help="Set file prefix string [default=%default]")


    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."

    # Move the turntable
    def wait_for_stop(axis):
        while(servo.isMoving(axis)):
            pass

    angle = options.angle
    
    servo = maestro.Controller()
#    print dir(servo)
    servo.setAccel(X_AXIS, ACCEL)
    servo.setSpeed(X_AXIS, SPEED)
    print( X_CENTER+(angle*TO_DEGREES))
    servo.setTarget(X_AXIS, int(X_CENTER+(angle*TO_DEGREES)))  
    wait_for_stop(X_AXIS)
    print(servo.getPosition(X_AXIS))
    servo.close                 

    # Fire up the flow graph to grab RSSI burst.
 #   tb = get_rssi(lo_offset = options.lo_offset,
 #                     rx_gain = options.rx_gain,
#                      rx_freq = rx_freq*1e6,
#                      usrp_addr = options.usrp_addr,
#                      rssi_count = options.rssi_count,
#                      file_prefix = options.file_prefix
#                  )
#    tb.start()
#    tb.wait()
