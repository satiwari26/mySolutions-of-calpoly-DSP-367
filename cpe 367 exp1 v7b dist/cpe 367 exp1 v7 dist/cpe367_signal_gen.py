#!/usr/bin/python

import sys
import time

import base64
import random as random

import datetime
import time
import math

from cpe367_wav import cpe367_wav



	
############################################
############################################
# define routine for generating signal in WAV format
def gen_wav(fpath_wav_out):
	"""
	: this example generates a WAV file
	: output is accomplished via WAV files
	: return: True or False 
	"""
	
	# construct object for writing WAV file
	#  assign object a name, to facilitate status and error reporting
	wav_out = cpe367_wav('wav_out',fpath_wav_out)
		
	# setup configuration for output WAV
	num_channels = 1
	sample_width_8_16_bits = 16
	sample_rate_hz = 16000
	wav_out.set_wav_out_configuration(num_channels,sample_width_8_16_bits,sample_rate_hz)
		
	# open WAV output file
	ostat = wav_out.open_wav_out()
	if ostat == False:
		print('Cant open wav file for writing')
		return False
	
	
	###############################################################
	###############################################################
	# students - there is work to be done here

	# these parameters will need updating!
	# you may also wish to add more parameters

	num_samples = 32000
	w1 = 2 * math.pi * 2000 / sample_rate_hz
	A = 24575
	
	# students - well done!
	###############################################################
	###############################################################



	# generate each sample and output, one at a time
	for n in range(num_samples):
			


		###############################################################
		###############################################################
		# students - there is work to be done here
		
		# compute the current output value
		yout = A * math.cos(w1 * n + (math.pi/4))
		
		# students - well done!
		###############################################################
		###############################################################



		# convert to signed int
		yout = int(round(yout))
		
		# output current sample 
		ostat = wav_out.write_wav(yout)
		if ostat == False: break
	
	# close input and output files
	#  important to close output file - header is updated (with proper file size)
	wav_out.close_wav()
		
	return True





############################################
############################################
# define main program
def main():

	# check python version!
	major_version = int(sys.version[0])
	if major_version < 3:
		print('Sorry! must be run using python3.')
		print('Current version: ')
		print(sys.version)
		return False
		
	# set output file name
	# fpath_wav_out = sys.argv[1]
	fpath_wav_out = 'cos.wav'

	# let's do it!
	return gen_wav(fpath_wav_out)
	
			
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()
