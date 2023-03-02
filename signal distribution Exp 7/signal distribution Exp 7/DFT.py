import sys
import time

import base64
import random as random

import datetime
import time
import math
import numpy as np
import matplotlib.pyplot as plt 

from cpe367_wav import cpe367_wav
from my_fifo import my_fifo

yOUT = []
for k in range(8000):
	yOUT.append(0)
	
############################################
############################################
# define routine for implementing a digital filter
def process_wav(fpath_wav_out):
	"""
	: this example does not implement an echo!
	: input and output is accomplished via WAV files
	: return: True or False 
	"""
	

	wav_out = cpe367_wav('wav_out',fpath_wav_out)
		
	# setup configuration for output WAV
	num_channels = 1
	sample_width_8_16_bits = 16
	sample_rate_hz = 8000
	wav_out.set_wav_out_configuration(num_channels,sample_width_8_16_bits,sample_rate_hz)
	# open WAV output file
	ostat = wav_out.open_wav_out()
	if ostat == False:
		print('Cant open wav file for writing')
		return False
	# process entire input signal
	yout = 0
	count = 0
	while count < 8000:
		yout = 8000*math.cos(0.25*math.pi*count)*math.exp(-(count)/1600)
		yOUT[count] = yout
		count = count + 1

		# convert to signed int
		yout = int(round(yout))
		
		# output current sample
		ostat = wav_out.write_wav(yout)
		if ostat == False: break
	# close output files
	# important to close output file - header is updated (with proper file size)
	compute_mag(yOUT)
	wav_out.close_wav()
	
	
	#N = 4000
	#freqs = np.fft.rfftfreq(N, d=1/8000)
	#dft = np.fft.rfft(yout, N)
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
	plot_spectrum(magnitude)
	return magnitude

def plot_spectrum(xin):
	x_comp = []
	for p in range(2000):
		x_comp.append(0)

	for t in range(2000):
		#print(t)
		x_comp[t] = t

	fig, ax = plt.subplots() 
	ax.plot(x_comp, xin) 
	ax.set(xlabel='Frequency (Hz)', ylabel='Counts', title='Cool Plot! ') 
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
	fpath_wav_out = 'no_name.wav'
	
	return process_wav(fpath_wav_out)

if __name__ == '__main__':
	
	main()
	quit()