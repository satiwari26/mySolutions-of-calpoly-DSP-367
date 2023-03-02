#!/usr/bin/python

import sys
import time

import base64
import random as random

import datetime
import time

from cpe367_wav import cpe367_wav
from my_fifo import my_fifo

import matplotlib.pyplot as plt 
import numpy as np
import math


	
############################################
############################################
# define routine for implementing a digital filter
def process_wav(fpath_wav_in):
	"""
	: this example does not implement an echo!
	: input and output is accomplished via WAV files
	: return: True or False 
	"""
	
	# construct objects for reading/writing WAV files
	#  assign each object a name, to facilitate status and error reporting
	wav_in = cpe367_wav('wav_in',fpath_wav_in)
	#wav_out = cpe367_wav('wav_out',fpath_wav_out)
	
	# open wave input file
	ostat = wav_in.open_wav_in()
	if ostat == False:
		print('Cant open wav file for reading')
		return False
		
	# setup configuration for output WAV
	
	#wav_out.set_wav_out_configuration(num_channels,sample_width_8_16_bits,sample_rate_hz)

	xin =[]
	xk =[]
	for i in range(4000):
		xin.append(0)
		xk.append(0)
	#xin stores the 4000 elements of the wave file

	for i in range(4000):
		xin[i] = wav_in.read_wav()

	xk = compute_mag(xin)

	#for s in range(4000):
		#print(xk[s])

	wav_in.close_wav()

	return True
		
def compute_mag(xin):
	xk =[]
	for i in range(4000):
		#xin.append(0)
		xk.append(0)

	#computing the DTF of my input wave
	for l in range(4000):
		for k in range(4000):
			xk[l] = xk[l] + xin[k]*(math.cos(2*math.pi*l*k/8000) - 1j*math.sin(2*math.pi*l*k/8000))

	xp = []
	for u in range(4000):
		xp.append(0)
	
	for q in range(4000):
		xp[q] = xk[q]/4000

	#computing the magnitude of the DFT array.		                          
	magnitude = np.abs(xp)
	plot_spectrum(magnitude)
	return magnitude

def plot_spectrum(xk):
	x_comp = []
	for p in range(4000):
		x_comp.append(0)

	for t in range(4000):
		#print(t)
		x_comp[t] = t

	fig, ax = plt.subplots() 
	ax.plot(x_comp, xk) 
	ax.set(xlabel='Frequency (Hz)', ylabel='Magnitude', title='cos_1khz_pulse_20msec ') 
	ax.grid() 
 
	fig.savefig('image_file.png') 
	plt.show() 




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
	fpath_wav_in = 'cos_1khz_pulse_20msec.wav'
	#fpath_wav_out = 'joy_short2_echo_FIR.wav'
	
	
	
	############################################
	############################################
	# test signal history
	#  feel free to comment this out, after verifying
		
	# allocate history
	#M = 4
	#fifo = my_fifo(M)

	# add some values to history
	#fifo.update(1)
	#fifo.update(2)
	#fifo.update(3)
	#fifo.update(4)
	
	# print out history in order from most recent to oldest
	#print('signal history - test')
	#for k in range(M):
	#	print('hist['+str(k)+']='+str(fifo.get(k)))

	############################################
	############################################
	


	# let's do it!
	return process_wav(fpath_wav_in)
	
			
	
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()