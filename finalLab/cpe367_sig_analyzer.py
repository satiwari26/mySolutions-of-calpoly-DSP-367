#!/usr/bin/env python

############################################
# this python wav class was written by dr fred depiero at cal poly
# distribution is unrestricted provided it is without charge and includes attribution

import sys
import json

import matplotlib.pyplot as plt
import numpy as np

class cpe367_sig_analyzer:
	
	
	############################################
	# constructor for signal history object
	def __init__(self,sig_name_list,sample_rate):
	
		self.sig_name_list = []
		for sig_name in sig_name_list: self.sig_name_list.append(sig_name)
		
		self.sample_rate = sample_rate
		
		self.buff = []
		self.desc = 'No description is available'
				
	
	
	
	############################################
	# plot a portion of the signal
	def plot(self,py_elem_list,stt_time = -1,end_time = -1):
		"""
		:stt_time,end_time: the time window for plot
		:return: T/F and print any error message
		"""
		
		px_elem = 'sample_sec'
		
		# setup first sample index
		if stt_time == -1:
			stt_indx = 0
		else:
			stt_indx = int(stt_time * self.sample_rate)
			
		# setup last sample index
		if end_time == -1:
			end_indx = len( self.buff ) - 1
		else:
			end_indx = int(end_time * self.sample_rate)
		
		# number of subplots
		num_subp = len(py_elem_list)
		
		# create each subplot
		plot_indx = 1
		for py_elem in py_elem_list:
		
			# convert format
			xpoints = []
			ypoints = []
			for indx in range(stt_indx,end_indx+1):
				x_val = self.buff[indx][px_elem]
				y_val = self.buff[indx][py_elem]
			
				xpoints.append(x_val)
				ypoints.append(y_val)
			
			plt.subplot(num_subp, 1, plot_indx)
			plot_indx += 1
			
			plt.plot(np.array(xpoints), np.array(ypoints))
			plt.grid()
			plt.ylabel(py_elem)

		# include label for horizontal axis last
		plt.xlabel("Time (Sec)")

		plt.show()

		return True

	


	############################################
	# set a description for this data set
	def set_desc(self,desc):
		"""
		:desc: a description
		:return: T/F and print any error message
		"""
		
		self.desc = desc
		
		return True
		
		
		
	############################################
	# get a description for this data set
	def get_desc(self):
		"""
		:desc: return the description
		:return: desc
		"""
				
		return self.desc
		
		
		
		
	############################################
	# set a description for this data set
	def print_desc(self):
		"""
		:desc: print the description
		:return: T/F and print any error message
		"""
		
		print(self.desc)
		
		return True
		
		
		
		
		
	############################################
	# assign a sample to the list
	def add(self,sig_name,sig_indx,sig_val):
		return self.set(sig_name,sig_indx,sig_val,add_flag = True)




	############################################
	# assign a sample to the list
	def set(self,sig_name,sig_indx,sig_val,add_flag = False):
		"""
		:correct_val: the correct value for the signal for this new sample
		:return: T/F and print any error message
		"""
				
		# check if buffer needs to be extended to accommodate this sample
		if sig_indx >= len(self.buff):
		
			for iii in range(len(self.buff),sig_indx+1):
				sig_dict = {}
				sig_dict['sample_index'] = iii
				sig_dict['sample_sec'] = sig_dict['sample_index'] / self.sample_rate

				for sn in self.sig_name_list: sig_dict[sn] = 0

				self.buff.append(sig_dict)
		
		# add this signal value within the set of signals
		if add_flag == True:
			self.buff[sig_indx][sig_name] += sig_val
		else:
			self.buff[sig_indx][sig_name] = sig_val

		return True



	############################################
	# get simple stats
	def get_mean(self,sig_name):
		"""
		:sig_name: name of the sample of interest
		:sig_indx: index of the sample of interest
		:return: mean
		"""
				
		sig_sum = 0
		for i in range( len(self.buff) ):
			sig_sum += self.buff[i][sig_name]
		
		# return this item
		return sig_sum / (len(self.buff) - 1)



	############################################
	# get a sample from the list
	def get(self,sig_name,sig_indx):
		"""
		:sig_name: name of the sample of interest
		:sig_indx: index of the sample of interest
		:return: T/F and print any error message
		"""
				
		# check if buffer needs to be extended to accommodate this sample
		if sig_indx >= len(self.buff) or sig_indx < 0:
			print('Unable to get '+str(sig_name)+' ['+str(sig_indx)+'] from buffer')
			return None
		
		# return this item
		return self.buff[sig_indx][sig_name]



	############################################
	# clear out the list
	def clear(self):
		"""
		:return: T/F and print any error message
		"""
		
		self.buff = []

		return True



	############################################
	# get length of internal buffer
	def get_len(self):
		"""
		:return: length
		"""
		
		return len(self.buff)



	############################################
	# save current data
	def save(self,fname):
		"""
		:fname: file name for JSON text file
		:return: T/F and print any error message
		"""
		
		json_obj = {}
		json_obj['buff'] = self.buff
		json_obj['desc'] = self.desc
		
		# buff_json_str = json.dumps(self.buff, ensure_ascii=True, indent=4)
		json_str = json.dumps(json_obj, ensure_ascii=True, indent=4)

		try:		
			f = open(fname, 'w')
			f.write(json_str)
			f.close()
			
		except IOError as e:
			print('Unable to save JSON: '+str(e))
			return False
		
		return True


	############################################
	# load current data then augment
	def load(self,fname):
		"""
		:fname: file name for JSON text file
		:return: T/F and print any error message
		"""
		
		try:
			self.clear()
			
			with open(fname, 'r') as json_file:  
				json_obj = json.load(json_file)
				
				for jjj in json_obj['buff']: self.buff.append(jjj)
				self.desc = json_obj['desc']
			
		except IOError as e:
			print('Unable to load JSON: '+str(e))
			return False
		
		# augment
		for bbb in range( len(self.buff) ):
			for sn in self.sig_name_list:
			
				if sn in self.buff[bbb]:
					print('Load aborted. Signal '+str()+' already present!')
					return False
					
				self.buff[bbb][sn] = 0

		return True


