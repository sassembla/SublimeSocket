# -*- coding: utf-8 -*-
import SublimeSocketAPISettings

from .WSEncoder import WSEncoder
from PythonSwitch import PythonSwitch

# Protocole version	see-> http://tools.ietf.org/html/rfc6455
VERSION = 13

# Operation codes
OP_CONTINUATION = 0x0
OP_TEXT = 0x1
OP_BINARY = 0x2
OP_CLOSE = 0x8
OP_PING = 0x9
OP_PONG = 0xA

OPCODES = (OP_CONTINUATION, OP_TEXT, OP_BINARY, OP_CLOSE, OP_PING, OP_PONG)

class WSController:
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

		encoder = WSEncoder()
 		# python-switch
		for case in PythonSwitch(ctrl['opcode']):
			if case(OP_PING):
				break

			if case(OP_PONG):
				break

			if case(OP_CLOSE):
				break
		
			if case(OP_TEXT):
				#check if API or not
				if (self.isApi(data)):
					
					self.client.server.call(data, self.client.clientId)

				else:
					print("data is not for sublimesocket. no 'ss@'header. data:", data)
				break

			if case(OP_CONTINUATION):
				# print "continuation...(not yet do anything)"
				break

			if case(OP_BINARY):
				# print "is binary", data
				# see msgpack branch
				break

			if case(): # default, could also just omit condition or 'if True'
				print("default,,, should not be")


	## Check API-adoptable or not
	def isApi(self, data):
		headerAndParam = data.split(SublimeSocketAPISettings.SSAPI_DEFINE_DELIM, 1)
		return headerAndParam[0] == SublimeSocketAPISettings.SSAPI_PREFIX or headerAndParam[0] == SublimeSocketAPISettings.SSAPI_PREFIX_SUB
		
	## Send a ping
	def ping(self):
		print('--- PING (CONTROLLER) ---')



