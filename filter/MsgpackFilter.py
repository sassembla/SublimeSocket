import datetime

import msgpack
from io import BytesIO

DEFINE_MESSAGEPACK_KEY = "mp"

class MsgpackFilter:
	
	def decode(self, packed_dict):
		return msgpack.unpackb(packed_dict, use_list=True)[DEFINE_MESSAGEPACK_KEY]

