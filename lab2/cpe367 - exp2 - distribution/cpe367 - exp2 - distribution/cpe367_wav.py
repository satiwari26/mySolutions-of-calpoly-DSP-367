#!/usr/bin/env python

############################################
# this python wav class was written by dr fred depiero at cal poly
# distribution is unrestricted provided it is without charge and includes attribution

import sys
import json

import wave
import struct

class cpe367_wav:
	
	
	############################################
	# constructor for WAV object
	def __init__(self,sig_name,fpath):
	
		self.sig_name = sig_name
		self.fpath = fpath
		self.wf = None
		self.write_mode = False
		
		self.num_channels = -1
		self.width_bits = -1
		self.sample_rate_hz = -1
		self.num_samples = -1
		self.num_read = -1
		
		self.debug_iter = 0
	
	
	
	
	############################################
	# open wav file for reading
	def open_wav_in(self):
		"""
		:self.fpath: path to file
		:return: T/F with an error or status message
		"""

		# verify that a file isnt already open
		if self.wf != None:
			print('('+str(self.sig_name)+') WAV Error: File already open')
			return False

		# attempt to open file for reading
		try:

			self.wf = wave.open(self.fpath,'rb')

			print('('+str(self.sig_name)+') WAV file opened for reading')
			print('('+str(self.sig_name)+') Sample width: '+str(8 * self.wf.getsampwidth()) +' bits' )
			print('('+str(self.sig_name)+') Number of channels: '+str(self.wf.getnchannels()) )
			print('('+str(self.sig_name)+') Sample rate: '+str(self.wf.getframerate()) +' Hz')
			print('('+str(self.sig_name)+') Number of frames: '+str(self.wf.getnframes()) )
			
			self.num_channels = self.wf.getnchannels()
			self.width_bits = 8 * self.wf.getsampwidth()
			self.sample_rate_hz = self.wf.getframerate()
			self.num_samples = self.wf.getnframes()
			self.num_read = 0

		except IOError as e:
			print('('+str(self.sig_name)+') Error opening file: '+str(e))
			return False
		
		except wave.Error as e:
			print('('+str(self.sig_name)+') Error opening wave: '+str(e))
			return False
			
		except:
			print('('+str(self.sig_name)+') Error: '+str( sys.exc_info() ))
			return False
		
		return True




	############################################
	# read from wav file - wrapper for mono
	def read_wav(self):
		"""
		: read next sample - as int
		: if WAV file is stereo convert to mono
		: return None when file is exhausted

		:self.fpath: path to file
		:return: int or None
		"""
		
		stereo_ret = self.read_wav_stereo()
		if stereo_ret == None: return None
		
		self.num_read += 1

		ret = (stereo_ret[0] + stereo_ret[1]) / 2
		return int(ret)
		
					
						

	############################################
	# read from wav file
	def read_wav_stereo(self):
		"""
		: read next sample - as list with stereo pair of ints
		: return a list of length two for stereo
		: if WAV file is mono then same value is returned for both channels
		: return None when file is exhausted

		:return: list of ints, length 2, or None
		"""
						
		# verify that a file isnt already open
		if self.wf == None:
			print('('+str(self.sig_name)+') WAV Error: File not open - unable to read')
			return None

		# verify that this wav object was opened for write
		if self.write_mode == True:
			print('('+str(self.sig_name)+') WAV Error: File not open for read')
			return None
		
		# attempt to read
		ret_val = None
		try:
			val_bytes = self.wf.readframes(1)
			
			# if nothing is returned, then EOF
			if len(val_bytes) == 0: return None
									
			val_lft_int = 0
			val_rgt_int = 0

			# read mono sample
			if self.num_channels == 1:
			
				# handle 8 bit unsigned data
				if self.width_bits == 8:
					# val_lft_int = int.from_bytes(val_bytes, byteorder='little', signed=False)
					val_list = list(val_bytes)
					val_lft_int = val_list[0]
					val_rgt_int = val_list[0]
				
				# handle 16 bit signed data
				elif self.width_bits == 16:
					val_tuple = struct.unpack("<h", val_bytes)
					val_lft_int = val_tuple[0]
					val_rgt_int = val_tuple[0]

				else:
					print('('+str(self.sig_name)+') Error: Cant read '+str(self.width_bits)+' bit mono WAV')
			
			# read stereo pair of samples
			else:
								
				# handle 8 bit unsigned data
				if self.width_bits == 8:
					val_list = list(val_bytes)
					val_lft_int = val_list[0]
					val_rgt_int = val_list[1]
			
				# handle 16 bit signed data
				elif self.width_bits == 16:
					val_tuple = struct.unpack("<h", val_bytes[0:2])
					val_lft_int = val_tuple[0]
					
					val_tuple = struct.unpack("<h", val_bytes[2:4])
					val_rgt_int = val_tuple[0]

				else:
					print('('+str(self.sig_name)+') Error: Cant read '+str(self.width_bits)+' bit stereo WAV')

			ret_val = [val_lft_int, val_rgt_int]
			
		except IOError as e:
			print('('+str(self.sig_name)+') Error reading file: '+str(e))
			return None
			
		except wave.Error as e:
			print('('+str(self.sig_name)+') Error reading wave: '+str(e))
			return None
			
		except:
			print('('+str(self.sig_name)+') Error: '+str( sys.exc_info() ))
			return None
		
		return ret_val




	############################################
	# set configuration of WAV file
	def set_wav_out_configuration(self,num_channels,sample_width_8_16,sample_rate_hz):
		"""
		:num_channels: number of channels for output WAV file (1,2) for (mono,stereo)
		:sample_width_8_16: width of each sample in bits. 16 bit is signed, 8 bit is unsigned
		:sample_rate_hz: sample rate in Hz
		:return: T/F with any error message
		"""

		# verify that a file isnt already open
		if self.wf != None:
			print('('+str(self.sig_name)+') WAV Error: File already open - cant configure')
			return False

		self.num_channels = num_channels
		self.width_bits = sample_width_8_16
		self.sample_rate_hz = sample_rate_hz

		return True



	############################################
	# copy configuration of WAV file from another WAV object
	def copy_wav_out_configuration(self,wav_src):
		"""
		:wav_src: another similar object, to copy 
		:return: T/F with any error message
		"""

		# verify that a file isnt already open
		if self.wf != None:
			print('('+str(self.sig_name)+') WAV Error: File already open - cant configure')
			return False

		self.num_channels = wav_src.num_channels
		self.width_bits = wav_src.width_bits
		self.sample_rate_hz = wav_src.sample_rate_hz

		return True



	############################################
	# open wav file for writing
	def open_wav_out(self):
		"""
		:self.fpath: path to file
		:return: T/F with any error message
		"""

		# verify that a file isnt already open
		if self.wf != None:
			print('('+str(self.sig_name)+') WAV Error: File already open')
			return False

		# attempt to open file for writing
		try:

			self.wf = wave.open(self.fpath,'wb')
			
			# attempt to set demographics
			self.wf.setnchannels(self.num_channels)
			self.wf.setsampwidth( int(self.width_bits / 8) )
			self.wf.setframerate(self.sample_rate_hz)
			self.wf.setnframes(1)

			print('('+str(self.sig_name)+') WAV file opened for writing')
			print('('+str(self.sig_name)+') Sample width: '+str(8 * self.wf.getsampwidth()) +' bits' )
			print('('+str(self.sig_name)+') Number of channels: '+str(self.wf.getnchannels()) )
			print('('+str(self.sig_name)+') Sample rate: '+str(self.wf.getframerate()) +' Hz')
			# print('('+str(self.sig_name)+') Number of frames: '+str(self.wf.getnframes()) )
			
			self.num_channels = self.wf.getnchannels()
			self.width_bits = 8 * self.wf.getsampwidth()
			self.sample_rate_hz = self.wf.getframerate()
			self.write_mode = True
			
		except IOError as e:
			print('('+str(self.sig_name)+') Error opening file: '+str(e))
			return False
		
		except wave.Error as e:
			print('('+str(self.sig_name)+') Error opening wave: '+str(e))
			return False
			
		except:
			# print('('+str(self.sig_name)+') Error: '+str( sys.exc_info()[0] ))
			print('('+str(self.sig_name)+') Error: '+str( sys.exc_info() ))
			return False
		
		return True



	############################################
	# write to wav file - wrapper for mono
	def write_wav(self,left_int,write_raw = True):
		"""
		: write next sample - mono. clip as needed

		:left_int: sample value for write
		:write_raw: flag that skips update of header that would adjust number of samples in file.
						skipping header update provides faster write. header updated on close!
		:return: T/F with any error message
		"""
	
		return self.write_wav_stereo(left_int,left_int,write_raw)
	
	
	
	
	############################################
	# write to wav file
	def write_wav_stereo(self,left_int,right_int,write_raw = True):
		"""
		: write next sample - as stereo pair. clip as needed
		: if WAV file is mono then LEFT value is used for write

		:left_int,right_int: sample values for write
		:write_raw: flag that skips update of header that would adjust number of samples in file.
						skipping header update provides faster write. header updated on close!
		:return: T/F with any error message
		"""
						
		# verify that a file isnt already open
		if self.wf == None:
			print('('+str(self.sig_name)+') WAV Error: File not open - unable to write')
			return False
		
		# verify that this wav object was opened for write
		if self.write_mode == False:
			print('('+str(self.sig_name)+') WAV Error: File not open for write')
			return False
		
		
		# clip if needed
		clipped = False
		if self.width_bits == 8:
			
			if left_int >= 256:
				clipped = True
				left_int = 255
				
			if right_int >= 256:
				clipped = True
				right_int = 255
				
			if left_int < 0:
				clipped = True
				left_int = 0
				
			if right_int < 0:
				clipped = True
				right_int = 0

		# clip if needed
		else:
			
			if left_int > 32767:
				clipped = True
				left_int = 32767
				
			if right_int > 32767:
				clipped = True
				right_int = 32767
				
			if left_int < -32768:
				clipped = True
				left_int = -32768
				
			if right_int < -32768:
				clipped = True
				right_int = -32768
		
		# warn if clipping occurs - vomiting all these warnings is annoying, HaHa!
		if clipped:
			print('('+str(self.sig_name)+') Warning: Data clipped during write operation')
			
		
		# attempt to write
		try:
			
			# prep byte-like object for write
			w_bytes = None
			
			# output mono
			if self.num_channels == 1:
			
				if self.width_bits == 8:
					# w_bytes = left_int.to_bytes(1, byteorder='little', signed=False)
					w_bytes = left_int.to_bytes(1, byteorder='little', signed=False)
				
				# convert to int 
				#  little endian appears to be appropriate for WAV standard
				elif self.width_bits == 16:
					w_bytes = left_int.to_bytes(2, byteorder='little', signed=True)
				
				else:
					print('('+str(self.sig_name)+') Error: Cant write '+str(self.width_bits)+' bit mono')
			
			# output stereo
			else:
								
				if self.width_bits == 8:

					w_bytes = bytes([left_int, right_int])
			
				# convert to int			
				elif self.width_bits == 16:
					
					w_bytes = bytearray(4)
					
					# little endian, LSB first, MSB second, left then right
					w_bytes[0] =  left_int & 0x0000FF
					w_bytes[1] = (left_int & 0x00FF00) >> 8

					w_bytes[2] =  right_int & 0x0000FF
					w_bytes[3] = (right_int & 0x00FF00) >> 8

				else:
					print('('+str(self.sig_name)+') Error: Cant write '+str(self.width_bits)+' bit stereo')
			
			# attempt write
			if w_bytes != None:
			
				# write raw or polished, as directed
				if write_raw == True: self.wf.writeframesraw(w_bytes)
				else: self.wf.writeframes(w_bytes)
			
		except IOError as e:
			print('('+str(self.sig_name)+') Error writing file: '+str(e))
			return False
			
		except wave.Error as e:
			print('('+str(self.sig_name)+') Error writing wave: '+str(e))
			return False
			
		except:
			print('('+str(self.sig_name)+') Error writing: '+str( sys.exc_info() ))
			quit()
			return False
		
		return True




	############################################
	# close wav file after either reading or writing
	def close_wav(self):
		"""
		writes a zero sample at end of file and updates header with proper file length
		:return: T/F with any error message
		"""

		# verify that a file isnt already open
		if self.wf == None:
			print('('+str(self.sig_name)+') WAV Error: File already closed (or never opened)')
			return False

		# write zeros and reconcile number of frames (if this is an output WAV file)
		if self.write_mode == True:
					
			# attempt to write
			try:
				w_bytes = bytearray(0)
				self.wf.writeframes(w_bytes)
			
			except IOError as e:
				print('('+str(self.sig_name)+') I/O error while closing with header update: '+str(e))
				return False
			
			except wave.Error as e:
				print('('+str(self.sig_name)+') wave error while closing with header update: '+str(e))
				return False
			
			except:
				print('('+str(self.sig_name)+') Error while closing with header update: '+str( sys.exc_info() ))
				return False
				
		
		# close it
		self.wf.close()
		
		# flags
		self.wf = None
		
		self.num_channels = -1
		self.width_bits = -1
		self.sample_rate_hz = -1

		self.write_mode = False

		return True



