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
peak_env697 = []
peak_env770 = []
#peak_env852 = []
peak_env1209 = []
peak_env1336 = []
#peak_env1477 = []
#peak_env1633 = []
#peak_env941 = []



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

	for k in range(s2.get_len()):
		peak_env697.append(0)
		peak_env770.append(0)
		#peak_env852.append(0)
		peak_env1209.append(0)
		peak_env1336.append(0)
		#peak_env1477.append(0)
		#peak_env1633.append(0)
		#peak_env941.append(0)

	r1 = 0.9
	b0 = 1-r1
	#freq =0
	a2 = r1*r1

	fifo1209 = my_fifo(3)
	fifo1336 = my_fifo(3)
	#fifo1477 = my_fifo(3)
	fifo697 = my_fifo(3)
	fifo770 = my_fifo(3)
	#fifo852 = my_fifo(3)
	#fifo1633 = my_fifo(3)
	#fifo941 = my_fifo(3)


	y1209 = []
	y1336 = []
	#y1477 = []
	#y1633 = []

	y697 = []
	y770 = []
	#y852 = []
	#y941 = []
	for i in range(s2.get_len()):
		y1209.append(0)
		y1336.append(0)
		#y1477.append(0)

		y697.append(0)
		y770.append(0)
		#y852.append(0)

	# process input	
	xin = 0
	count =0
	for n_curr in range(s2.get_len()):
		
		# read next input sample from the signal analyzer
		xin = s2.get('xin',n_curr)
		s2.set('sig_1',n_curr,xin)
		#symbol_val_det = 5

		#8 different filter operations
		y1209[n_curr] = b0*xin + (2*r1*np.cos(2*np.pi*1209/4000))*fifo1209.get(0) - a2*fifo1209.get(1)
		y1336[n_curr] = b0*xin + (2*r1*np.cos(2*np.pi*1336/4000))*fifo1336.get(0) - a2*fifo1336.get(1)
		#y1477[n_curr] = b0*xin + (2*r1*np.cos(2*np.pi*1477/4000))*fifo1477.get(0) - a2*fifo1477.get(1)
		#y1633[n_curr] = b0*xin + (2*r1*np.cos(2*np.pi*1633/4000))*fifo1477.get(0) - a2*fifo1477.get(1)

		y697[n_curr] = b0*xin + (2*r1*np.cos(2*np.pi*697/4000))*fifo697.get(0) - a2*fifo697.get(1)
		y770[n_curr] = b0*xin + (2*r1*np.cos(2*np.pi*770/4000))*fifo770.get(0) - a2*fifo770.get(1)
		#y852[n_curr] = b0*xin + (2*r1*np.cos(2*np.pi*852/4000))*fifo852.get(0) - a2*fifo852.get(1)
		#y941[n_curr] = b0*xin + (2*r1*np.cos(2*np.pi*941/4000))*fifo1477.get(0) - a2*fifo1477.get(1)


		#updating all the filter operation
		fifo1209.update(y1209[n_curr])
		fifo1336.update(y1336[n_curr])
		#fifo1477.update(y1477[n_curr])
		#fifo1633.update(y1477[n_curr])

		fifo697.update(y697[n_curr])
		fifo770.update(y770[n_curr])
		#fifo852.update(y852[n_curr])
		#fifo941.update(y852[n_curr])

		
		#peak_env697[n_curr] = np.max( np.abs(y697[]))/1024
		

		s2.set('sig_1209',n_curr,y1209[n_curr])
		s2.set('sig_1336',n_curr,y1336[n_curr])
		#s2.set('sig_1477',n_curr,y1477[n_curr])
		s2.set('sig_697',n_curr,y697[n_curr])
		s2.set('sig_770',n_curr,y770[n_curr])
		#s2.set('sig_852',n_curr,y852[n_curr])
		#s2.set('peak_envolp 697',n_curr,peak_env697[n_curr])

		#if((y1209[n_curr])>16 and (y697[n_curr])>16):
		#	symbol_val_det = 1
		#elif((y1209[n_curr])>16 and (y770[n_curr])>16):
		#	symbol_val_det = 4
		#elif((y1336[n_curr])>16 and (y697[n_curr])>16):
		#	symbol_val_det = 2
		#elif((y1336[n_curr])>16 and (y770[n_curr])>16):
		#	symbol_val_det = 5
		
		# save intermediate signals as needed, for plotting
		#  add signals, as desired!

		#s2.set('607 frequency',n_curr,xin)
		
		#s2.set('sig_2',n_curr,2 * xin)

		# save detected symbol
		#s2.set('symbol_det',n_curr,symbol_val_det)

		# get correct symbol (provided within the signal analyzer)
		#symbol_val = s2.get('symbol_val',n_curr)

		# compare detected signal to correct signal
		#symbol_val_err = 0
		#if symbol_val != symbol_val_det: symbol_val_err = 1
		
		# save error signal
		#s2.set('error',n_curr,symbol_val_err)
	
	envolopeDet(y697,peak_env697,s2)
	envolopeDet(y770,peak_env770,s2)
	envolopeDet(y1209,peak_env1209,s2)
	envolopeDet(y1336,peak_env1336,s2)
	#envolopeDet(y1477,peak_env1477,s2)
	#envolopeDet(y1633,peak_env1633,s2)
	#envolopeDet(y852,peak_env852,s2)
	#envolopeDet(y941,peak_env941,s2)

	for c in range(s2.get_len()):
		if(peak_env1209[c]>30 and peak_env697[c]>30):
			symbol_val_det = 1
		elif(peak_env1209[c]>30 and peak_env770[c]>30):
			symbol_val_det = 4
		#elif(peak_env1209[c]>30 and peak_env852[c]>30):
			#symbol_val_det = 7
		elif(peak_env1336[c]>30 and peak_env697[c]>30):
			symbol_val_det = 2
		elif(peak_env1336[c]>30 and peak_env770[c]>30):
			symbol_val_det = 5
			
		#else:
		#	symbol_val_det = 0

		#setting detected symbol value
		s2.set('symbol_det',c,symbol_val_det)
		#setting correct symbol value
		symbol_val = s2.get('symbol_val',c)
		s2.set('symbol_val',c,symbol_val)
		# compare detected signal to correct signal
		symbol_val_err = 0
		if symbol_val != symbol_val_det: symbol_val_err = 1
		
		# save error signal
		s2.set('error',c,symbol_val_err)

	# display mean of error signal
	err_mean = s2.get_mean('error')
	print('mean error = '+str( round(100 * err_mean,1) )+'%')

	for t in range(s2.get_len()):
		#plotting mag of dft after filtering it
		s2.set('envolope_697',t,peak_env697[t])
		s2.set('envolope_770',t,peak_env770[t])
		s2.set('envolope_1209',t,peak_env1209[t])
		s2.set('envolope_1336',t,peak_env1336[t])
		#s2.set('sig_1209',t,yout2[t])

		#symbol_val_det = 0

		# save detected symbol
		#s2.set('symbol_det',t,symbol_val_det)

		# get correct symbol (provided within the signal analyzer)
		# compare detected signal to correct signal
		#symbol_val_err = 0
		#if symbol_val != symbol_val_det: symbol_val_err = 1
		
		# save error signal
		#s2.set('error',t,symbol_val_err)
	
	# display mean of error signal
	#err_mean = s2.get_mean('error')
	#print('mean error = '+str( round(100 * err_mean,1) )+'%')
		
	# define which signals should be plotted
	#plot_sig_list = ['sig_1','sig_2','symbol_val','symbol_det','error']
	#plot_sig_list = ['sig_1209','sig_1336','sig_1477','sig_697','sig_770','sig_852','envolope_697','symbol_val']
	plot_sig_list = ['envolope_770','envolope_1209','envolope_1336','envolope_697','symbol_val','symbol_det','error']
	
	# plot results
	s2.plot(plot_sig_list)
	
	return True


def envolopeDet(yin,peakEnvo,s2):

	#finding max value in chucks of the value
	for p in range(0,s2.get_len(),10):
		chunk = yin[p:p+10]
		maxVal = max(np.abs(chunk))
		for j in range(len(chunk)):
			chunk[j] = maxVal
		peakEnvo[p:p+10] = chunk


#dft of the signal after applying filter to it
def dftMag(yout,s2):
	xk = []
	for s in range(s2.get_len()):
		xk.append(0.0)
	
	for l in range(s2.get_len()):
		for k in range(s2.get_len()):
			xk[l] = xk[l] + yout[k]*(np.cos((2*np.pi*l*k/(2*s2.get_len())) - (1j*np.sin(2*np.pi*l*k/(2*s2.get_len())))))

	#absolute value of the dft
	dftMag1 = np.abs(xk)

	return(dftMag1)
	#dftMag2 =[]
	#for s in range(2000):
	#	dftMag2.append(0)

	#x_comp = []
	#for t in range(s2.get_len()):
		#print(t)
	#	x_comp.append(t)

	#for k in range(2000):
	#	dftMag2[k] = dftMag1[k]

	#exact_freq = 0
	#freq_mag = 0
	#mag = 0

	#for p in range(s2.get_len()):
	#	freq_mag = freq_mag+(p*dftMag1[p])
	#	mag = mag+(dftMag1[p])
	
	#exact_freq = freq_mag/mag

	#print("weighted frequency is: " + str(exact_freq))

	#fig, ax = plt.subplots() 
	#ax.plot(x_comp, dftMag1) 
	#ax.set(xlabel='Frequency (Hz)', ylabel='Magnitude', title='tile 2E ') 
	#ax.grid() 
 
	#fig.savefig('image_file.png') 
	#plt.show() 
	
	
	
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
