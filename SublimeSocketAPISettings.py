
#API for Input to ST2 through WebSocket

### COMMAND		=		COMMAND_NAME : JSON_EXPRESSION
### COMMANDS	=		COMMAND_NAME : JSON_EXPRESSION -> COMMAND_NAME : JSON_EXPRESSION -> ...
### COMMANDS	=		COMMAND_NAME + COMMAND_NAME : JSON_EXPRESSION -> COMMAND_NAME + COMMAND_NAME + COMMAND_NAME : JSON_EXPRESSION -> ...

API_PREFIX = "sublimesocket"
API_PREFIX_SUB = "ss"
API_DEFINE_DELIM = "@"					# sublimesocket@commandA:{}->commandB:{}->commandC:[]->
API_CONCAT_DELIM = "->"					# concat commands. every commands run in sequential.
API_OVERLAP_DELIM	= "+"					# overlap commands. share parameters with multiple APIs.	
API_COMMAND_PARAMS_DELIM = ":"		# only first ":" will be evaluated as delimiter / each commnand.

# SublimeSocket internal event definition
SS_EVENT_COLLECT	= "ss_collect"
SS_EVENT_ERROREMITTED	= "ss_errorEmitted"

# internal APIs/
API_I_SHOWSTATUSMESSAGE		= "showStatusMessage"
SHOWSTATUSMESSAGE_MESSAGE	= "message"

API_I_ERASEALLREGION	= "eraseAllRegion"

API_I_REACT					= "react"
# /internal APIs

# region identifier prefix
REGION_UUID_PREFIX = "ss_"

# public APIs
API_RUNSETTING		= "runSetting"
RUNSETTING_FILEPATH	= "path"

API_INPUTIDENTITY = "inputIdentity"
IDENTITY_ID				= "id"

API_KILLSERVER		=	"killServer"

API_SETREACTOR		= "setReactor"
REACTOR_TARGET		= "target"
REACTOR_EVENT			= "event"
REACTOR_SELECTORS	= "selectors"
REACTOR_INTERVAL	= "interval"
REACTOR_REPLACEFROMTO		= "replacefromto"

REACTIVE_INTERVAL_EVENT	= ["on_modified", "on_selection_modified"]
REACTIVE_ONEBYONE_EVENT = [SS_EVENT_ERROREMITTED]

API_KEYVALUESTORE	= "kvs"
KVS_SHOWALL				= "showAll"
KVS_SHOWVALUE			= "showValue"
KVS_REMOVEVALUE		= "removeValue"
KVS_CLEAR					= "clear"

API_DEFINEFILTER	= "defineFilter"
FILTER_PATTERNS		= "patterns"


API_FILTERING			= "filtering"
FILTER_NAME				= "name"
FILTER_SOURCE			= "source"
FILTER_SELECTORS	= "selectors"
FILTER_DEBUG			= "debug"

API_CONTAINSREGIONS	= "containsRegions"
CONTAINSREGIONS_VIEW	= "view"
CONTAINSREGIONS_TARGET	= "target"
CONTAINSREGIONS_EMIT	= "emit"
CONTAINSREGIONS_DEBUG	= "debug"

API_COLLECTVIEWS	= "collectViews"

API_DETECTVIEW		= "detectView"
DETECT_PATH				= "path"

API_SETTARGETVIEW	= "setTargetView"
VIEW_PATH					= "path"
VIEW_ID						= "viewId"
VIEW_BUFFERID			= "bufferId"
VIEW_BASENAME			= "basename"
VIEW_VNAME				= "vname"
VIEW_SELF					= "view"
VIEW_EVENTS_RENEW	= ["on_new", "on_clone", "on_load", "on_modified", SS_EVENT_COLLECT] #list of acceptable-view renew event names.
VIEW_EVENTS_DEL		= ["on_close"] #list of acceptable-view del event names.
TARGETTED_VIEW		= "targettedView"

API_RUNSHELL			= "runShell"
RUNSHELL_MAIN			= "main"
RUNSHELL_DEBUG		= "debug"
RUNSHELL_LIST_IGNORES = [RUNSHELL_MAIN, RUNSHELL_DEBUG]

API_BROADCASTMESSAGE	= "broadcastMessage"
API_OUTPUTMESSAGE	= "outputMessage"
OUTPUT_TARGET			= "target"
OUTPUT_MESSAGE		= "message"

API_SHOWATLOG			= "showAtLog"
LOG_MESSAGE				= "message"
LOG_prefix				= "ss:"

API_APPENDREGION	= "appendRegion"
APPENDREGION_VIEW	= "view"
APPENDREGION_VIEW_CURRENT = "current"
APPENDREGION_LINE	= "line"
APPENDREGION_MESSAGE	= "message"


API_TIMEREVENT		= "timerEvent"

API_EVAL					= "eval"


#Dictionaries for collection of "Views", "filters", "events"
DICT_VIEWS				= "DICT_VIEWS"
DICT_FILTERS			= "DICT_FILTERS"
DICT_REACTORS			= "DICT_REACTORS"
DICT_CURRENTTARGETVIEW	= "DICT_CURRENTTARGETVIEW"

SUBDICT_REGIONS		= "SUBDICT_REGIONS"
REGION_IDENTITY		= "identity"
REGION_SELF				= "region"
REGION_EVENT			= "event"
REGION_MESSAGE		= "message"
REGION_LINE				= "line"

SUBARRAY_DELETED_REGIONS		= "SUBARRAY_DELETED_REGIONS"


