# -*- coding: utf-8 -*-
import SublimeWSSettings

from SublimeWSEncoder import *
from SublimeSocketAPI import *

class SublimeWSController:
	def __init__(self,client):
		self._client = client

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

		print '--- CONTROLLER ---', repr(self._client.conn)
		encoder = SublimeWSEncoder()

		# CONTROLS
		print "ctrl is ", ctrl['opcode']

 		# python-switch
		for case in switch(ctrl['opcode']):
			if case(SublimeWSSettings.OP_PING):
				print '--- PING FRAME ---', repr(self._client.conn)
				try:
					bytes = encoder.pong('Application data')
				except ValueError as error:
					self._client._server.remove(self._client)
					self.kill(1011, 'WSEncoder error: ' + str(error))
				else:
					self._client.send(bytes)

				break

			if case(SublimeWSSettings.OP_PONG):
				print '--- PONG FRAME ---', repr(self._client.conn)
				if len(data):
					print 'Pong frame datas:', str(data)

				break

			if case(SublimeWSSettings.OP_CLOSE):
				print '--- CLOSE FRAME ---', repr(self._client.conn)
				self._client._server.remove(self._client)
				# closing was initiated by server
				if self._client.hasStatus('CLOSING'):
					self._client.close()
				# closing was initiated by client
				if self._client.hasStatus('OPEN'):

					# close client.
					self._client.setStatus('CLOSING')
					
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
				print '--- TEXT FRAME ---', repr(self._client.conn)
				
				if (data.split(SublimeWSSettings.API_DEFINE_DELIM)[0] == SublimeWSSettings.API_PREFIX):
					api = SublimeSocketAPI()
					api.parse(data)

				break

			if case(SublimeWSSettings.OP_CONTINUATION):
				print '--- CONTINUATION FRAME ---', repr(self._client.conn)
				break

			if case(SublimeWSSettings.OP_BINARY):
				print '--- BINARY FRAME ---', repr(self._client.conn)
				break

			if case(): # default, could also just omit condition or 'if True'
				print "default,,, should not be"

	## Send a ping
	def ping(self):
		print '--- PING (CONTROLLER) ---'

	## Force to close the connection
	#  @param code Closing code according to RFC. Default is 1000 (NORMAL_CLOSURE).
	#  @param error Error message to append on closing frame. Default is empty.
	def kill(self, code=1000, error=''):
		print '--- KILL (CONTROLLER)  ---', repr(self._client.conn)
		if not self._client.hasStatus('CLOSED'):
			encoder = SublimeWSEncoder()
			data = struct.pack('!H', code)
			if len(error):
				print "エラーが出てる ", error
				data += error
			print '--- KILL FRAME ---', code, error, repr(self._client.conn)
			try:
				bytes = encoder.close(data)
			except ValueError as error:
				self._client.close()
			else:
				self._client.send(bytes)
				self._client.close()
