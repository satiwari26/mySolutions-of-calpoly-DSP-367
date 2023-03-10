#!/usr/bin/python

import sys
import time

import base64
import random as random

import datetime
import time
import math

import matplotlib.pyplot as plt
import numpy as np

#from cpe367_wav import cpe367_wav
from cpe367_sig_analyzer import cpe367_sig_analyzer
from my_fifo import my_fifo



#global list to store the dft input signals
#creating yout to store the new signal after running it through the filter
yout1 = []
yout2 = []
yout3 = []
yout4 = []

############################################
############################################
# define routine for detecting DTMF tones
def process_wav(fpath_sig_in):
	
		
	###############################
	# define list of signals to be displayed by and analyzer
	#  note that the signal analyzer already includes: 'symbol_val','symbol_det','error'
	more_sig_list = ['sig_1','sig_2']
	
	# sample rate is 4kHz
	fs = 4000
	
	# instantiate signal analyzer and load data
	s2 = cpe367_sig_analyzer(more_sig_list,fs)
	s2.load(fpath_sig_in)
	s2.print_desc()
	
	symbol_val_det = 0


	#initialize buffer sample
	bufferSamp = []
	for p in range(20):
		bufferSamp.append(0)
	
	sampleCount =0
	ncountReset =0 # find the peak in 20 samples times this will give us the index of where it is happening in the s2.length

	maxIndex1 =0
	maxIndex2 =0
	maxIndex3 = 0
	maxIndex4 = 0
	index1336 = 0
	index1209= 0
	index697 = 0
	index770 = 0
	# process input	
	xin = 0
	for n_curr in range(s2.get_len()):
		
		# read next input sample from the signal analyzer
		xin = s2.get('xin',n_curr)
		#s2.set('sig_1',n_curr,xin)
		#symbol_val_det = 5

		if (sampleCount ==9):
			maxIndex1 = bandPassSig(bufferSamp,1209,yout1)
			maxIndex2 = bandPassSig(bufferSamp,697,yout2) #call the filter function
			maxIndex3 = bandPassSig(bufferSamp,1336,yout3)
			maxIndex4 = bandPassSig(bufferSamp,770,yout4)
			sampleCount=0

			#print('reset count '+str(ncountReset))
			
			index1209 = index1209+10+maxIndex1 
			index697 = index697+10+maxIndex2
			index1336 = index1336+10+maxIndex3
			index770 = index770+10+maxIndex4

			print(str(index1209)+ " index1209")
			print(str(index697)+ " index697")
			print(str(index1336)+ " index1336")
		else:
			sampleCount = sampleCount+1
			bufferSamp[sampleCount] = xin

		########################
		# students: evaluate each filter and implement other processing blocks

		#split it into different function to perform the buffere operation

		#print(str(index1209)+ " index1209")
		#print(str(index697)+ " index697")
		#print(str(index1336)+ " index1336")


		if(np.abs(index1209-index1336) <=5):
			symbol_val_det = 2
		if(np.abs(index1209-index697) <=5):
			symbol_val_det  = 1
		########################
		# students: combine results from filtering stages
		#  and find (best guess of) symbol that is present at this sample time
		
		


		# save intermediate signals as needed, for plotting
		#  add signals, as desired!

		#s2.set('607 frequency',n_curr,xin)
		
		#s2.set('sig_2',n_curr,2 * xin)

		# save detected symbol
		s2.set('symbol_det',n_curr,symbol_val_det)

		# get correct symbol (provided within the signal analyzer)
		#symbol_val = s2.get('symbol_val',n_curr)

		# compare detected signal to correct signal
		#symbol_val_err = 0
		#if symbol_val != symbol_val_det: symbol_val_err = 1
		
		# save error signal
		#s2.set('error',n_curr,symbol_val_err)

	
	#absolute value of the dft

	for t in range(s2.get_len()):
		#plotting mag of dft after filtering it
		s2.set('sig_2',t,yout1[t])

		s2.set('sig_1',t,yout3[t])

		symbol_val_det = 0

		# save detected symbol
		#s2.set('symbol_det',t,symbol_val_det)

		# get correct symbol (provided within the signal analyzer)
		symbol_val = s2.get('symbol_val',t)

		# compare detected signal to correct signal
		symbol_val_err = 0
		if symbol_val != symbol_val_det: symbol_val_err = 1
		
		# save error signal
		s2.set('error',t,symbol_val_err)
	
	# display mean of error signal
	err_mean = s2.get_mean('error')
	print('mean error = '+str( round(100 * err_mean,1) )+'%')
		
	# define which signals should be plotted
	plot_sig_list = ['sig_1','sig_2','symbol_val','symbol_det','error']
	
	# plot results
	s2.plot(plot_sig_list)
	
	return True

#filter operation on the signal with certain buffer length
def bandPassSig(bufferSample,freq,youtG):
	#fifo class that will have the same length
	maxindex =0
	fifo1 = my_fifo(3)
	
	#initialize buff to store the ybuff_out
	yBuff = []
	for s in range(10):
		yBuff.append(0)

	# students: setup filters
	r1 = 0.9
	b0 = 1-r1
	#freq =0
	a2 = r1*r1

	#apply filter and update the samples
	for i in range(10):
		yBuff[i] = b0*bufferSample[i] + (-2*r1*np.cos(2*np.pi*freq/4000))*fifo1.get(0) + a2*fifo1.get(1)
		fifo1.update(yBuff[i])
	maxIndex = dftMag(yBuff,youtG)

	return maxIndex



#dft of the signal after applying filter to it
def dftMag(yout,youtG):
	xk = []
	maxVal = 0
	maxIndex =0
	for s in range(10):
		xk.append(0.0)
	
	for l in range(10):
		for k in range(10):
			xk[l] = xk[l] + yout[k]*(np.cos((2*np.pi*l*k/(20)) - (1j*np.sin(2*np.pi*l*k/20))))

	#absolute value of the dft
	dftMag1 = np.abs(xk)

	#global val storer func
	globalValStorer(dftMag1,youtG)

	for t in range(len(dftMag1)): #find the max peak and its index
		if(dftMag1[t]>maxVal):
			maxVal = dftMag1[t]
			maxIndex = t
			#print(str(maxVal)+' '+str(maxIndex))
	#print('returning max index' + str(maxIndex))
	return maxIndex

	

def globalValStorer(dftMag1,yout):
	#store it in the global variable
	for t in range(10):
		yout.append(dftMag1[t])
	
	
	
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
		
	# assign file name
	fpath_sig_in = 'dtmf_signals_slow.txt'
	# fpath_sig_in = 'dtmf_signals_fast.txt'
	
	
	# let's do it!
	return process_wav(fpath_sig_in)


	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()
