#!/usr/bin/python

import sys
import time

import base64
import random as random

import datetime
import time

from cpe367_wav import cpe367_wav
from my_fifo import my_fifo


	
############################################
############################################
# define routine for implementing a digital filter
def process_wav(fpath_wav_in,fpath_wav_out):
	"""
	: this example does not implement an echo!
	: input and output is accomplished via WAV files
	: return: True or False 
	"""
	
	# construct objects for reading/writing WAV files
	#  assign each object a name, to facilitate status and error reporting
	wav_in = cpe367_wav('wav_in',fpath_wav_in)
	wav_out = cpe367_wav('wav_out',fpath_wav_out)
	
	# open wave input file
	ostat = wav_in.open_wav_in()
	if ostat == False:
		print('Cant open wav file for reading')
		return False
		
	# setup configuration for output WAV
	num_channels = 2
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
	# students - allocate your fifo, with an appropriate length (M)
	M = 9				# length 3 is not appropriate!
	#6757 samples to cover 4 seconds
	fifo = my_fifo(M)
 
	# students - allocate filter coefficients as needed, length (M)
	# students - these are not the correct filter coefficients
	#bk_list_left = [0,1,2,3,4,5,6,7,8]
	#bk_list_right =[8,7,6,5,4,3,2,1,0]
	i=0
	j=8
	###############################################################
	###############################################################
	count =0
	# process entire input signal
	yout_left =0
	yout_right=0
	xin = 0
	while xin != None:
		count = count+1
		# read next sample (assumes mono WAV file)
		#  returns None when file is exhausted
		xin = wav_in.read_wav()
		if xin == None: break
		
		###############################################################
		###############################################################
		# students - there is work to be done here!
		# update history with most recent input
		fifo.update(xin)
		# evaluate your difference equation	to yield the desired effect!
		#  this example just copies the mono input into the left and right channel
		if (count == 7111):
			#yout_left = fifo.get(i)
			i+=1
			if(i==9):
				i=0
			#yout_right = fifo.get(j)
			j-=j
			if(j==0):
				j=8
			count = 0	

		yout_left = fifo.get(i)
		yout_right = fifo.get(j)


		
		# students - well done!
		###############################################################
		###############################################################


		# convert to signed int
		yout_left = int(round(yout_left))
		yout_right = int(round(yout_right))
		
		# output current sample
		ostat = wav_out.write_wav_stereo(yout_left,yout_right)
		if ostat == False: break
	
	# close input and output files
	#  important to close output file - header is updated (with proper file size)
	wav_in.close_wav()
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
			
	# grab file names
	fpath_wav_in = 'joy.wav'
	fpath_wav_out = 'joy_no_change.wav'
	
	
	
	############################################
	############################################
	# test signal history
	#  feel free to comment this out, after verifying
		
	# allocate history
	M = 4
	fifo = my_fifo(M)

	# add some values to history
	fifo.update(1)
	fifo.update(2)
	fifo.update(3)
	fifo.update(4)
	
	# print out history in order from most recent to oldest
	print('signal history - test')
	for k in range(M):
		print('hist['+str(k)+']='+str(fifo.get(k)))

	############################################
	############################################
	


	# let's do it!
	return process_wav(fpath_wav_in,fpath_wav_out)
	
			
	
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()
