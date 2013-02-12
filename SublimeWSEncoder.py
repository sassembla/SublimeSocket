# -*- coding: utf-8 -*-
import struct, array, math, random
import SublimeWSSettings

class SublimeWSEncoder:

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


	## Shortcut to encode text
	#  @param data UTF-8 text to send
	#  @param fin bit which define if the frame is the last one. Default is 1.
	#  @param mask bit which define is datas must be masked or not. Default is 1.
	def text(self, data='', fin=1, mask=1):
		return self.encode(0x1, data, fin, mask)

	## Shortcut to encode binary datas
	#  @param data UTF-8 text to send
	#  @param fin bit which define if the frame is the last one. Default is 1.
	#  @param mask bit which define is datas must be masked or not. Default is 1.
	def binary(self, data='', fin=1, mask=1):
		return self.encode(0x2, data, fin, mask)

	## Shortcut to encode close frame
	#  @param data UTF-8 text to send
	#  @param fin bit which define if the frame is the last one. Default is 1.
	#  @param mask bit which define is datas must be masked or not. Default is 1.
	def close(self, data='', fin=1, mask=1):
		return self.encode(0x8, data, fin, mask)

	## Shortcut to encode ping frame
	#  @param data UTF-8 text to send
	#  @param fin bit which define if the frame is the last one. Default is 1.
	#  @param mask bit which define is datas must be masked or not. Default is 1.
	def ping(self, data='', fin=1, mask=1):
		return self.encode(0x9, data, fin, mask)

	## Shortcut to encode pong frame
	#  @param data UTF-8 text to send
	#  @param fin bit which define if the frame is the last one. Default is 1.
	#  @param mask bit which define is datas must be masked or not. Default is 1.
	def pong(self, data='', fin=1, mask=1):
		return self.encode(0xA, data, fin, mask)

	## Encoding function for all types
	#  @param opcode Operation code according to RFC
	#  @param data UTF-8 text to send
	#  @param fin bit which define if the frame is the last one. Default is 1.
	#  @param mask bit which define is datas must be masked or not. Default is 1.
	#  @param rsv1 reserved bit for future usage. Do not use. Default is 0.
	#  @param rsv2 reserved bit for future usage. Do not use. Default is 0.
	#  @param rsv3 reserved bit for future usage. Do not use. Default is 0.
	def encode(self, opcode=0x1, data='', fin=1, mask=1, rsv1=0, rsv2=0, rsv3=0):
		if not opcode in SublimeWSSettings.OPCODES:
			raise ValueError('Unknow opcode key.')

		if (opcode >= 0x8): # for control frames
			mask = 0x1
			fin = 0x1

		if (opcode == 0x1):
			# print 'before encode: part 1 ', data
			pass
		else:			
			# print 'before encode: part 2', repr(data)
			pass
			
		if opcode == 0x1:
			try:
			    data.encode('utf-8')
			except UnicodeError:
			    raise ValueError('Text datas MUST be UTF-8 encoded.')

		if isinstance(data, bytearray):
			data = str(data)
		
		if mask != 0x0 and mask != 0x1:
			raise ValueError('MASK bit parameter must be 0 or 1')
		if fin != 0x0 and fin != 0x1:
			raise ValueError('FIN bit parameter must be 0 or 1')
		if rsv1 != 0x0 and rsv1 != 0x1:
			raise ValueError('RSV1 bit parameter must be 0 or 1')
		if rsv2 != 0x0 and rsv2 != 0x1:
			raise ValueError('RSV2 bit parameter must be 0 or 1')
		if rsv3 != 0x0 and rsv3 != 0x1:
			raise ValueError('RSV3 bit parameter must be 0 or 1')

		if 0x3 <= opcode <= 0x7 or 0xB <= opcode:
			raise ValueError('Reserved opcode')

		bytes = struct.pack('!B', ((fin << 7) | (rsv1 << 6) | (rsv2 << 5) | (rsv3 << 4) | opcode))
		
		mask_key = ''
		if (mask):
			# build a random mask key (4 bytes string)
			for i in xrange(4):
				mask_key += chr(int(math.floor(random.random() * 256)))

		print 'mask_key:', repr(mask_key)

		length = len(data)

		if length == 0:
			raise ValueError('No data given.')
		
		#print 'data length:', str(length)
		if length < 126:
			bytes += chr((mask << 7) | length)
		elif length < (1 << 16): # 65536
			bytes += chr((mask << 7) | 0x7e) + struct.pack('!H', length)
		elif length < (1 << 63): # 9223372036854775808
			bytes += chr((mask << 7) | 0x7f) + struct.pack('!Q', length)
		else:
			raise ValueError('Frame too large')

		# print repr(bytes)
		# print 'data=', data

		ctrl = (fin, rsv1, rsv2, rsv3, opcode, mask_key, data)
		
		if (mask):
			bytes += mask_key
			bytes += self.mask(mask_key, str(data))
		else:
			bytes += data

		# print 'after encode:', repr(bytes)
		return bytes

	## Mask datas
	def mask(self, mask_key, bytes):
		# new byte[i] = old byte[i] XOR mask_key[i%4]
		m = array.array('B', mask_key)
		j = array.array('B', bytes)
		for i in xrange(len(j)):
			j[i] ^= m[i % 4]
		return j.tostring()

