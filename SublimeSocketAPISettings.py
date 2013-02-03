
#API for Input to ST2 through WebSocket
API_PREFIX = "sublimesocket"
API_PREFIX_SUB = "ss"

API_DEFINE_DELIM = "@"
API_CONCAT_DELIM = "->"
API_COMMAND_PARAMS_DELIM = ":"# only first ":" will be evaluated as delimiter.

API_INPUTIDENTITY = "inputIdentity"
API_KILLSERVER    = "killServer"
API_EVENTLISTEN		= "eventListen"
API_TIMEREVENT		= "timerEvent"

API_EVAL					= "eval"

API_TEST					= "test"


# list of apis that depends on WSServer's interval event
INTERVAL_DEPEND_APIS = [API_EVENTLISTEN]