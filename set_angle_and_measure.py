#!/usr/bin/env python

import maestro
import time, math

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sys

X_AXIS = 0
Y_AXIS = 1
X_CENTER = 6010
Y_CENTER = 5984
TO_DEGREES = 2.7 #1100/360

SPEED = 1
ACCEL = 1



class uhd_power_measure(gr.top_block):

    def __init__(self, lo_offset, rx_gain, rx_freq, usrp_addr, measurement_interval, file_name):
        gr.top_block.__init__(self, "UHD Power Measure")

        ##################################################
        # Parameters
        ##################################################
        self.args = args=''

        ##################################################
        # Variables
        ##################################################
        self.trans_width = trans_width = 0.25e6
        self.samp_rate = samp_rate = 10
        self.filt_stop_freq = filt_stop_freq = 1e6
        self.filt_start_freq = filt_start_freq = -1e6
        self.atten = atten = 50
        self.taps = taps = firdes.complex_band_pass_2(1, samp_rate*1e6, filt_start_freq, filt_stop_freq, trans_width, atten)
        self.rx_gain = rx_gain 
        self.rx_freq = rx_freq 
        self.measurement_interval = measurement_interval
        self.ant = ant = "RX2"

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_1 = uhd.usrp_source(
        	",".join((args, "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		otw_format='sc16',
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_1.set_clock_source('gpsdo', 0)
        self.uhd_usrp_source_1.set_samp_rate(samp_rate*1e6)
        self.uhd_usrp_source_1.set_center_freq(rx_freq*1e6, 0)
        self.uhd_usrp_source_1.set_gain(rx_gain, 0)
        self.uhd_usrp_source_1.set_antenna(ant, 0)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(0.001, 1)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (taps), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, int(measurement_interval*samp_rate*1e6))
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, samp_rate*1000000)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, file_name, True)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.single_pole_iir_filter_xx_0, 0))
#        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_nlog10_ff_0, 0))
 #       self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_head_0, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))
#        self.connect((self.uhd_usrp_source_1, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.uhd_usrp_source_1, 0),  (self.blocks_head_0, 0))
        self.connect((self.blocks_head_0, 0), (self.fft_filter_xxx_0, 0))
     
    def get_args(self):
        return self.args

    def set_args(self, args):
        self.args = args

    def get_trans_width(self):
        return self.trans_width

    def set_trans_width(self, trans_width):
        self.trans_width = trans_width
        self.set_taps(firdes.complex_band_pass_2(1, self.samp_rate*1e6, self.filt_start_freq, self.filt_stop_freq, self.trans_width, self.atten))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_taps(firdes.complex_band_pass_2(1, self.samp_rate*1e6, self.filt_start_freq, self.filt_stop_freq, self.trans_width, self.atten))
        self.uhd_usrp_source_1.set_samp_rate(self.samp_rate*1e6)
        self.blocks_keep_one_in_n_0.set_n(int(self.measurement_interval*self.samp_rate*1e6))

    def get_filt_stop_freq(self):
        return self.filt_stop_freq

    def set_filt_stop_freq(self, filt_stop_freq):
        self.filt_stop_freq = filt_stop_freq
        self.set_taps(firdes.complex_band_pass_2(1, self.samp_rate*1e6, self.filt_start_freq, self.filt_stop_freq, self.trans_width, self.atten))

    def get_filt_start_freq(self):
        return self.filt_start_freq

    def set_filt_start_freq(self, filt_start_freq):
        self.filt_start_freq = filt_start_freq
        self.set_taps(firdes.complex_band_pass_2(1, self.samp_rate*1e6, self.filt_start_freq, self.filt_stop_freq, self.trans_width, self.atten))

    def get_atten(self):
        return self.atten

    def set_atten(self, atten):
        self.atten = atten
        self.set_taps(firdes.complex_band_pass_2(1, self.samp_rate*1e6, self.filt_start_freq, self.filt_stop_freq, self.trans_width, self.atten))

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.fft_filter_xxx_0.set_taps((self.taps))

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_1.set_gain(self.rx_gain, 0)


    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.uhd_usrp_source_1.set_center_freq(self.rx_freq*1e6, 0)

    def get_measurement_interval(self):
        return self.measurement_interval

    def set_measurement_interval(self, measurement_interval):
        self.measurement_interval = measurement_interval
        self.blocks_keep_one_in_n_0.set_n(int(self.measurement_interval*self.samp_rate*1e6))

    def get_ant(self):
        return self.ant

    def set_ant(self, ant):
        self.ant = ant
        self.uhd_usrp_source_1.set_antenna(self.ant, 0)

# Call this code with a radial angle.
# Antenna "turntable" is rotated to angle.
# Returns a uniqely named file with a stream of rssi values for this angle.

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-o", "--lo-offset", dest="lo_offset", type="eng_float", default=eng_notation.num_to_str(125e3),
        help="Set lo_offset frequency in Hz [default=%default]")
    parser.add_option("-f", "--rx_freq", dest="rx_freq", type="eng_float", default=eng_notation.num_to_str(3178.0),             
        help="Set receive frequency in MHz [default=%default]")
    parser.add_option("-g", "--rx-gain", dest="rx_gain", type="eng_float", default=eng_notation.num_to_str(50),
        help="Set rx_gain [default=%default]")
    parser.add_option("", "--usrp-addr", dest="usrp_addr", type="string", default="type=b200",
        help="Set usrp_addr [default=%default]")
    parser.add_option("-a", "--angle", dest="angle", type="eng_float", default=0.0,
        help="Set angle of turntable [default=%default]")
    parser.add_option("-c", "--rssi-count", dest="measurement_interval", type="intx", default=0.9,
        help="Count of RSSI values to capture [default=%default]")
    parser.add_option("-F", "--file_name", dest="file_name", type="string",
                      default="rssi.f32",
        help="Set file name [default=%default]")


    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."

    # Move the turntable
    def wait_for_stop(axis):
        while(servo.isMoving(axis)):
            pass

    angle = options.angle
    
    servo = maestro.Controller()
    servo.setAccel(X_AXIS, ACCEL)
    servo.setSpeed(X_AXIS, SPEED)
    print( X_CENTER+(angle*TO_DEGREES))
    servo.setTarget(X_AXIS, int(X_CENTER+(angle*TO_DEGREES)))  
    wait_for_stop(X_AXIS)
    print(servo.getPosition(X_AXIS))
    servo.close                 

    # Fire up the flow graph to grab RSSI burst.
    tb = uhd_power_measure(lo_offset = options.lo_offset,
                      rx_gain = options.rx_gain,
                      rx_freq = options.rx_freq,
                      usrp_addr = options.usrp_addr,
                      measurement_interval = options.measurement_interval,
                      file_name = options.file_name
                  )
    tb.start()
    tb.wait()
