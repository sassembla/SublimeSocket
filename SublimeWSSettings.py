#Protocole version	see-> http://tools.ietf.org/html/rfc6455
VERSION = 13

#Operation codes
OP_CONTINUATION = 0x0
OP_TEXT = 0x1
OP_BINARY = 0x2
OP_CLOSE = 0x8
OP_PING = 0x9
OP_PONG = 0xA

OPCODES = (OP_CONTINUATION, OP_TEXT, OP_BINARY, OP_CLOSE, OP_PING, OP_PONG)


#API for Input to ST2 through WebSocket
API_DEFINE_DELIM = "@"
API_PREFIX = "sublimesocket"
API_INPUTIDENTITY = "input/indetity:"


#API for Oputput from ST2 through WebSocket
API_KILLKEY = "killkey:"



#Closing frame status codes.
NORMAL_CLOSURE =  1000 # \x03\xe8
ENDPOINT_IS_GOING_AWAY =  1001 # \x03\xe9
PROTOCOL_ERROR =  1002 # \x03\xea
UNSUPPORTED_DATA_TYPE =  1003 # \x03\xeb
# NOT_AVAILABLE = 1005
# ABNORMAL_CLOSED = 1006
INVALID_PAYLOAD =  1007 # \x03\xef - INCONSISTENT DATA/TYPE
POLICY_VIOLATION =  1008 # \x03\xf0
MESSAGE_TOO_BIG =  1009 # \x03\xf1
EXTENSION_NOT_FOUND_ON_SERVER =  1010 # \x03\xf2
UNEXPECTED_CONDITION_ENCOUTERED_ON_SERVER =  1011 # \x03\xf3
# TLS_HANDSHAKE_ERROR = 1015

CLOSING_CODES = (NORMAL_CLOSURE, ENDPOINT_IS_GOING_AWAY, PROTOCOL_ERROR, UNSUPPORTED_DATA_TYPE, INVALID_PAYLOAD, POLICY_VIOLATION, MESSAGE_TOO_BIG, EXTENSION_NOT_FOUND_ON_SERVER, UNEXPECTED_CONDITION_ENCOUTERED_ON_SERVER)
