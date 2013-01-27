# -*- coding: utf-8 -*-
import SublimeWSSettings

from SublimeWSEncoder import *

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

		print '--- CONTROLLER ---', repr(self.client.conn)
		encoder = SublimeWSEncoder()

 		# python-switch
		for case in switch(ctrl['opcode']):
			if case(SublimeWSSettings.OP_PING):
				print '--- PING FRAME ---', repr(self.client.conn)
				try:
					bytes = encoder.pong('Application data')
				except ValueError as error:
					self.client.server.remove(self.client)
				else:
					self.client.send(bytes)

				break

			if case(SublimeWSSettings.OP_PONG):
				print '--- PONG FRAME ---', repr(self.client.conn)
				if len(data):
					print 'Pong frame datas:', str(data)

				break

			if case(SublimeWSSettings.OP_CLOSE):
				print '--- CLOSE FRAME ---', repr(self.client.conn)
				self.client.server.remove(self.client)
				# closing was initiated by server
				if self.client.hasStatus('CLOSING'):
					self.client.close()
				# closing was initiated by client
				if self.client.hasStatus('OPEN'):

					# close client.
					self.client.setStatus('CLOSING')
					
				# the two first bytes MUST contains the exit code, follow optionnaly with text data not shown to clients
				if len(data) >= 2:
					code, data = self.array_shift(data,2)
					status = ''
					if code in SublimeWSSettings.CLOSING_CODES:
						print 'Closing frame code:', code
					if len(data):
						print 'Closing frame data:', data

				break
		
			if case(SublimeWSSettings.OP_TEXT):
				print '--- TEXT FRAME ---', repr(self.client.conn)
				
				headerAndParam = data.split(SublimeWSSettings.API_DEFINE_DELIM)

				# run api or not
				if (headerAndParam[0] == SublimeWSSettings.API_PREFIX):
					self.client.server.callAPI(headerAndParam[1], self.client.clientId)

				break

			if case(SublimeWSSettings.OP_CONTINUATION):
				print '--- CONTINUATION FRAME ---', repr(self.client.conn)
				break

			if case(SublimeWSSettings.OP_BINARY):
				print '--- BINARY FRAME ---', repr(self.client.conn)
				break

			if case(): # default, could also just omit condition or 'if True'
				print "default,,, should not be"

	## Send a ping
	def ping(self):
		print '--- PING (CONTROLLER) ---'
