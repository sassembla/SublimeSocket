# -*- coding: utf-8 -*-
import SublimeWSSettings
import SublimeSocketAPI
from SublimeWSEncoder import *
import SublimeSocketAPISettings


class SublimeWSController:
	def __init__(self, client):
		self.client = client

	## Pop n bytes
	#  @param bytes Bytes to shift.
	#  @param n Number if bytes to shift.
	def array_shift(self, bytes, n):
		out = ''
		for num in range(0,n):
			out += bytes[num]
		return out, bytes[n:]

	## Handle incoming datas
	#  @param ctrl Control dictionnary for data.
	#  @param data Decoded data, text or binary.
	def run(self, ctrl, data):
		encoder = SublimeWSEncoder()
 		# python-switch
		for case in switch(ctrl['opcode']):
			if case(SublimeWSSettings.OP_PING):
				break

			if case(SublimeWSSettings.OP_PONG):
				break

			if case(SublimeWSSettings.OP_CLOSE):
				break
		
			if case(SublimeWSSettings.OP_TEXT):

				#check if API or not
				if (self.isApi(data)):
					headerAndParam = data.split(SublimeSocketAPI.API_DEFINE_DELIM)
					self.client.server.callAPI(headerAndParam[1], self.client.clientId)
				break

			if case(SublimeWSSettings.OP_CONTINUATION):
				print "continuation...(not yet do anything)"
				break

			if case(SublimeWSSettings.OP_BINARY):
				# see msgpack branch
				break

			if case(): # default, could also just omit condition or 'if True'
				print "default,,, should not be"


	## Check API-adoptable or not
	def isApi(self, data):
		headerAndParam = data.split(SublimeSocketAPI.API_DEFINE_DELIM)
		return headerAndParam[0] == SublimeSocketAPI.API_PREFIX or headerAndParam[0] == SublimeSocketAPI.API_PREFIX_SUB
		
	## Send a ping
	def ping(self):
		print '--- PING (CONTROLLER) ---'



