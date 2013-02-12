# -*- coding: utf-8 -*-
import struct, array
import SublimeWSSettings

from PythonSwitch import PythonSwitch

class SublimeWSDecoder:

	## Decode on the fly data from SublimeWSClient
	#  @param client WebSocket Client - we use the read() function to get data bytes
	def decode(self, client):
		#0                   1                   2                   3
		#0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
		#+-+-+-+-+-------+-+-------------+-------------------------------+
		#|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
		#|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
		#|N|V|V|V|       |S|             |   (if payload len==126/127)   |
		#| |1|2|3|       |K|             |                               |
		#+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
		#|     Extended payload length continued, if payload len == 127  |
		#+ - - - - - - - - - - - - - - - +-------------------------------+
		#|                               |Masking-key, if MASK set to 1  |
		#+-------------------------------+-------------------------------+
		#| Masking-key (continued)       |          Payload Data         |
		#+-------------------------------- - - - - - - - - - - - - - - - +
		#:                     Payload Data continued ...                :
		#+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
		#|                     Payload Data continued ...                |

		# OPCODES USED FOR ERRORS:
		# 1002: PROTOCOL_ERROR
		# 1003: UNSUPPORTED_DATA_TYPE
		# 1007: INVALID_PAYLOAD
		# 1011: UNEXPECTED_CONDITION_ENCOUTERED_ON_SERVER

		# decode first byte
		b = client.read(1)
		if not len(b):
			raise ValueError(1011, 'Reading first byte failed.')
		b1 = ord(b)
		fin = b1 >> 7 & 1
		rsv1 = b1 >> 6 & 1
		rsv2 = b1 >> 5 & 1
		rsv3 = b1 >> 4 & 1
		opcode = b1 & 0xf

		# decode second byte
		b = client.read(1)
		if not len(b):
			raise ValueError(1011, 'Reading second byte failed.')
		b2 = ord(b)
		mask = b2 >> 7 & 1
		if mask != 0x1:
			raise ValueError(1002, 'Client datas MUST be masked.')

		# decode data length (without mask size)
		length = b2 & 0x7f

		# RFC : If length is 126, the following 2 bytes must be interpreted as a 16-bit unsigned integer
		# are the payload length
		if length == 0x7e:
			b = client.read(2)
			if not len(b):
				raise ValueError(1011, 'Reading length failed.')
			length_bytes = b
			length = struct.unpack("!H", length_bytes)[0]

		# RFC : If length is 127, the following 8 bytes must be interpreted as a 64-bit unsigned integer (the
	    # most significant bit MUST be 0) are the payload length
		elif length == 0x7f:
			b = client.read(8)
			if not len(b):
				raise ValueError(1011, 'Reading length failed.')
			length_bytes = b
			length = struct.unpack("!Q", length_bytes)[0]

		# decode mask key
		mask_key = client.read(4)
		if not len(mask_key):
			raise ValueError(1011, 'Reading mask key failed.')
		
		data = client.read(length)
		
		# python-switch
		for case in PythonSwitch(opcode):
			if case(SublimeWSSettings.OP_PING):
				break

			if case(SublimeWSSettings.OP_PONG):
				break

			if case(SublimeWSSettings.OP_CLOSE):
				break
		
			if case(SublimeWSSettings.OP_TEXT):
				try:
					if not len(data):
						raise ValueError(1011, 'Reading data failed.')
			
					data = self.unmask(mask_key, str(data))
					data = data.decode('utf-8')
				except UnicodeError:
				  raise ValueError(1003, 'Client text datas MUST be UTF-8 encoded.')
				break

			if case(SublimeWSSettings.OP_CONTINUATION):
				break

			if case(SublimeWSSettings.OP_BINARY):
				# unmask
				data = self.unmask(mask_key, str(data))
				break

			if case(): # default, could also just omit condition or 'if True'
				print "default,,, should not be"


		ctrl = {
			'fin': fin,
			'opcode': opcode,
			'rsv1': rsv1,
			'rsv2': rsv2,
			'rsv3': rsv3,
		}
		
		return ctrl, data

	## Unmask datas
	#  @param mask_key Mask key (always 4 bytes long)
	#  @param bytes Data bytes to unmask
	def unmask(self, mask_key, bytes):
		# new byte[i] = old byte[i] XOR mask_key[i%4]
		m = array.array('B', mask_key)
		j = array.array('B', bytes)
		for i in xrange(len(j)):
			j[i] ^= m[i % 4]
		return j.tostring()

