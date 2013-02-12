
#API for Input to ST2 through WebSocket

### COMMAND = COMMAND_NAME : JSON_EXPRESSION
### COMMANDS = COMMAND_NAME : JSON_EXPRESSION -> COMMAND_NAME : JSON_EXPRESSION -> ...

API_PREFIX = "sublimesocket"
API_PREFIX_SUB = "ss"

API_DEFINE_DELIM = "@"					# sublimesocket@commandA:{}->commandB:{}->commandC:[]->
API_CONCAT_DELIM = "->"					# concat commands. every commands run in sequential.
API_COMMAND_PARAMS_DELIM = ":"		# only first ":" will be evaluated as delimiter / each commnand.

API_RUNSETTING		= "runSetting"
RUNSETTING_FILEPATH	= "filePath"

API_INPUTIDENTITY = "inputIdentity"
API_KILLSERVER		=	"killServer"

API_KEYVALUESTORE	= "kvs"
KVS_SHOWALL				= "showAll"
KVS_SHOWVALUE			= "showValue"
KVS_REMOVEVALUE		= "removeValue"
KVS_CLEAR					= "clear"

API_DEFINEFILTER	= "defineFilter"
FILTER_PATTERNS		= "filterPatterns"

API_FILTER				= "filter"
FILTER_NAME				= "filterName"
FILTER_SOURCE			= "filterSource"
FILTER_RUNNABLE_DELIM	= "filterRunnable_"

API_EVENTLISTEN		= "eventListen"
LISTEN_EVENTS			= ["on_modified"]

API_SETEVENT			= "setEvent"

# API_RUNSHELL			= "runShell" # not so sweet

API_OUTPUTMESSAGE	= "outputMessage"
OUTPUT_TARGET			= "target"
OUTPUT_MESSAGE		= "message"

API_TIMEREVENT		= "timerEvent"

API_EVAL					= "eval"


# list of apis that depends on WSServer's interval event
INTERVAL_DEPEND_APIS = [API_EVENTLISTEN]
