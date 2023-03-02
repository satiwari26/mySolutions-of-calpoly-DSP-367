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

	for l in range(4000):
		for k in range(4000):
			xk[l] = xk[l] + xin[k]*(math.cos(2*math.pi*l*k/8000) - 1j*math.sin(2*math.pi*l*k/8000))

	xp = []
	for u in range(2000):
		xp.append(0)
	
	for q in range(2000):
		xp[q] = xk[q]/2000
		                          
	magnitude = np.abs(xp)
	max_mag =0
	max_freq = 0
	
	#max peak of the wav file#
	# for p in range(4000):
	# 	if(max_mag<magnitude[p]):
	# 		max_mag = magnitude[p]
	# 		max_freq = p
	# print('Peak-mag: '+str(max_mag))
	# print('max_freq: '+str(max_freq))

	#Second_mag(magnitude,max_mag)
	plot_spectrum(magnitude)
	return magnitude

def Second_mag(xk,max_mag):
	right_mag = []
	#right_freq = []
	for k in range(4000):
		right_mag.append(0)
		#right_freq.append(0)
	for s in range(4000):
		if(xk[s]>=(max_mag/2)):
			right_mag[s] = xk[s]
			#right_freq[s] = s
	calculate_f(right_mag)
    #plot_spectrum(right_mag)



###########calculating f_zero value############
def calculate_f(right_mag):
	sum_freq_mag =0
	sum_mag = 0
	#f_zero =0
	for p in range(4000):
		if(right_mag !=0):
			sum_freq_mag = sum_freq_mag+(p*right_mag[p])
			sum_mag = sum_mag+right_mag[p]
	
	f_zero = (sum_freq_mag)/(sum_mag)
	print('weighted-average: '+str(f_zero))
	calc_air_gap(f_zero)
	

def calc_air_gap(f_zero):
	length = 343/(2*f_zero)
	length_inch = length*39.3701
	print('length in meter: '+ str(length))
	print('length in inches: '+ str(length_inch))


###############code for my plot############

def plot_spectrum(xk):
	x_comp = []
	for p in range(2000):
		x_comp.append(0)

	for t in range(2000):
		#print(t)
		x_comp[t] = t

	fig, ax = plt.subplots() 
	ax.plot(x_comp, xk) 
	ax.set(xlabel='Frequency (Hz)', ylabel='Magnitude', title='tile 2E ') 
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
	fpath_wav_in = 'tile2e.wav'
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