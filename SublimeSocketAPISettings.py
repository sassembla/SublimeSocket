
#API for Input to ST2 through WebSocket

### COMMAND = COMMAND_NAME : JSON_EXPRESSION
### COMMANDS = COMMAND_NAME : JSON_EXPRESSION -> COMMAND_NAME : JSON_EXPRESSION -> ...

API_PREFIX = "sublimesocket"
API_PREFIX_SUB = "ss"

API_DEFINE_DELIM = "@"					# sublimesocket@commandA:{}->commandB:{}->commandC:[]->
API_CONCAT_DELIM = "->"					# concat commands. every commands run in sequential.
API_COMMAND_PARAMS_DELIM = ":"		# only first ":" will be evaluated as delimiter / each commnand.

API_RUNSETTING		= "runSetting"
RUNSETTING_FILEPATH	= "path"

API_INPUTIDENTITY = "inputIdentity"
API_KILLSERVER		=	"killServer"

API_KEYVALUESTORE	= "kvs"
KVS_SHOWALL				= "showAll"
KVS_SHOWVALUE			= "showValue"
KVS_REMOVEVALUE		= "removeValue"
KVS_CLEAR					= "clear"

API_DEFINEFILTER	= "defineFilter"
FILTER_PATTERNS		= "patterns"

API_FILTER				= "filter"
FILTER_NAME				= "name"
FILTER_SOURCE			= "source"
FILTER_RUNNABLE		= "runnable"


# ITERNAL_APIS/
API_I_SHOWSTATUS		= "showStatus"

API_I_SHOWLINE			= "showLine"
SHOWLINE_LINE				= "line"
SHOWLINE_MESSAGE		= "message"
# /ITERNAL_APIS

API_SETLISTENEREVENT	= "setListenerEvent"
LISTEN_EVENTS			= ["on_modified"] #list of acceptable-listen event names.

API_COLLECTVIEWS	= "collectViews"

API_DETECTVIEW		= "detectView"
DETECT_SOURCE			= "source"

API_SETTARGETVIEW	= "setTargetView"
VIEW_PATH					= "path"
VIEW_ID						= "viewId"
VIEW_BUFFERID			= "bufferId"
VIEW_BASENAME			= "basename"
VIEW_VNAME				= "vname"
VIEW_SELF					= "view"
VIEW_EVENTS_RENEW	= ["on_new", "on_clone", "on_modified", "ss_collect"] #list of acceptable-view renew event names.
VIEW_EVENTS_DEL		= ["on_close"] #list of acceptable-view del event names.
TARGETTED_VIEW		= "targettedView"

# API_RUNSHELL			= "runShell" # not so sweet

API_OUTPUTMESSAGE	= "outputMessage"
# OUTPUT_TARGET			= "target"
OUTPUT_MESSAGE		= "message"

API_TIMEREVENT		= "timerEvent"

API_EVAL					= "eval"


#Dictionaries for collection of "Views", "filters", "events"
DICT_VIEWS				= "DICT_VIEWS"
DICT_FILTERS			= "DICT_FILTERS"
DICT_EVENTLISTENERS	= "DICT_EVENTLISTENERS"
DICT_CURRENTTARGETVIEW	= "DICT_CURRENTTARGETVIEW"




