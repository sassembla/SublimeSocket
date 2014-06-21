import os



# SublimeSocket API 

SS_HOST_REPLACE				= "SUBLIMESOCKET_HOST"
SS_PORT_REPLACE				= "SUBLIMESOCKET_PORT"
SS_VERSION_REPLACE			= "SUBLIMESOCKET_VERSION"
	
	
HTML_REPLACEABLE_KEYS		= [SS_HOST_REPLACE, SS_PORT_REPLACE, SS_VERSION_REPLACE]

# get folder name of this plugin.
MY_PLUGIN_PATHNAME			= os.path.split(os.path.dirname(os.path.realpath(__file__)))[1]
	
	
WEBSOCKET_SERVER			= "WebSocketServer"
TRANSFER_METHODS			= [WEBSOCKET_SERVER]
	
# KVS	
	
DICT_VIEWS					= "DICT_VIEWS"
VIEW_SELF					= "view"
VIEW_PATH					= "path"
VIEW_NAME					= "name"
VIEW_SELECTEDS				= "selecteds"
VIEW_ISEXIST				= "isExist"
	
	
DICT_COMPLETIONS			= "DICT_COMPLETIONS"
DICT_FILTERS				= "DICT_FILTERS"
DICT_REACTORS				= "DICT_REACTORS"
DICT_REACTORSLOG			= "DICT_REACTORS_LOG"
REACTORSLOG_LATEST			= "latest"

DICT_REGIONS				= "DICT_REGIONS"
REGION_IDENTITY				= "identity"
REGION_ISSELECTING			= "isSelecting"
REGION_FROM					= "from"
REGION_TO					= "to"
REGION_LINE					= "line"
REGION_MESSAGES				= "messages"
REGIONDATA_MESSAGE			= "message"


# region identifier prefix
REGION_UUID_PREFIX			= "ss_"



# API

SSAPI_PREFIX				= "sublimesocket"

SSAPI_PREFIX_SUB			= "ss"
SSAPI_DEFINE_DELIM			= "@"	# sublimesocket@commandA:{}->commandB:{}->commandC:[]->


SSAPI_VERSION				= "1.5.0"
SSSOCKET_VERSION			= 2	# for Sublime Text 2



# SublimeSocket internal event definition
SS_EVENT_COLLECT			= "ss_collect"
SS_EVENT_LOADING			= "ss_loading"
SS_EVENT_RENAMED			= "ss_renamed"



SS_FOUNDATION_NOVIEWFOUND	= "ss_f_noViewFound"
NOVIEWFOUND_NAME			= "name"
NOVIEWFOUND_MESSAGE			= "message"
NOVIEWFOUND_INJECTIONS		= [NOVIEWFOUND_NAME, NOVIEWFOUND_MESSAGE]

SS_FOUNDATION_VIEWEMIT		= "ss_f_viewemit"

SS_VIEWKEY_CURRENTVIEW		= "ss_viewkey_current"


# internal APIs/

INTERNAL_API_RUNTESTS		= "runTests"
RUNTESTS_PATH				= "path"

# /internal APIs



# public APIs
API_CONNECTEDCALL 			= "connectedCall"
# no injection, no key, no value.

API_VERSIONVERIFY			= "versionVerify"
VERSIONVERIFY_SOCKETVERSION	= "socketVersion"
VERSIONVERIFY_APIVERSION	= "apiVersion"
VERSIONVERIFY_CODE			= "code"
VERSIONVERIFY_MESSAGE		= "message"
VERSIONVERIFY_DRYRUN		= "dryrun"
VERSIONVERIFY_INJECTIONS = [VERSIONVERIFY_CODE, VERSIONVERIFY_MESSAGE]

VERIFICATION_CODE_VERIFIED_CLIENT_UPDATE			= 2
VERIFICATION_CODE_VERIFIED							= 1
VERIFICATION_CODE_REFUSED_DIFFERENT_SUBLIMESOCKET	= 0
VERIFICATION_CODE_REFUSED_SUBLIMESOCKET_UPDATE		= -1
VERIFICATION_CODE_REFUSED_CLIENT_UPDATE				= -2


API_ASSERTRESULT			= "assertResult"
ASSERTRESULT_CONTEXT		= "context"
ASSERTRESULT_CONTAINS		= "contains"
ASSERTRESULT_NOTCONTAINS	= "notcontains"
ASSERTRESULT_ISEMPTY		= "isempty"
ASSERTRESULT_ISNOTEMPTY		= "isnotempty"
ASSERTRESULT_ID				= "id"
ASSERTRESULT_DESCRIPTION	= "description"
ASSERTRESULT_DEBUG			= "debug"
ASSERTRESULT_VALUE_PASS		= "Pass:"
ASSERTRESULT_VALUE_FAIL		= "Fail:"
ASSERTRESULT_RESULT			= "result"
ASSERTRESULT_PASSEDORFAILED = "passedOrFailed"


API_AFTERASYNC				= "afterAsync"
AFTERASYNC_IDENTITY			= "identity"
AFTERASYNC_MS				= "ms"


API_WAIT					= "wait"
WAIT_MS						= "ms"


API_COUNTUP					= "countUp"
COUNTUP_LABEL				= "label"
COUNTUP_DEFAULT				= "default"
COUNTUP_COUNT				= "count"
COUNTUP_INJECTIONS			= [COUNTUP_LABEL, COUNTUP_COUNT]


API_RESETCOUNTS				= "resetCounts"
RESETCOUNTS_LABEL			= "label"
RESETCOUNTS_RESETTED		= "resetted"
RESETCOUNTS_INJECTIONS		= [RESETCOUNTS_RESETTED]


API_RUNSUSHIJSON			= "runSushiJSON"
RUNSUSHIJSON_PATH			= "path"
RUNSUSHIJSON_NAME			= "name"
RUNSUSHIJSON_LOGS			= "logs"
RUNSUSHIJSON_INJECTIONS		= [RUNSUSHIJSON_LOGS]
RUNSUSHIJSON_PREFIX_SUBLIMESOCKET_PATH = "SUBLIMESOCKET_PATH:"


API_CHANGEIDENTITY			= "changeIdentity"
CHANGEIDENTITY_FROM			= "from"
CHANGEIDENTITY_TO			= "to"
CHANGEIDENTITY_INJECTIONS	= [CHANGEIDENTITY_FROM, CHANGEIDENTITY_TO]

API_TEARDOWN				= "tearDown"

API_CREATEBUFFER			= "createBuffer"
CREATEBUFFER_NAME			= "name"
CREATEBUFFER_CONTENTS		= "contents"
CREATEBUFFER_INJECTIONS		= [CREATEBUFFER_NAME]

API_OPENFILE				= "openFile"
OPENFILE_PATH				= "path"
OPENFILE_NAME				= "name"
OPENFILE_INJECTIONS			= [OPENFILE_PATH, OPENFILE_NAME]

API_CLOSEFILE				= "closeFile"
CLOSEFILE_PATH				= "path"
CLOSEFILE_NAME				= "name"
CLOSEFILE_INJECTIONS		= [CLOSEFILE_PATH, CLOSEFILE_NAME]

API_CLOSEALLFILES			= "closeAllFiles"
CLOSEALLFILES_EXCEPTS		= "excepts"
CLOSEALLFILES_CLOSEDS		= "closeds"
CLOSEALLFILES_INJECTIONS	= [CLOSEALLFILES_CLOSEDS]

API_CLOSEALLBUFFER			= "closeAllBuffer"
CLOSEALLBUFFER_CLOSEDS		= "closeds"
CLOSEALLBUFFER_INJECTIONS	= [CLOSEALLBUFFER_CLOSEDS]

API_SETEVENTREACTOR			= "setEventReactor"
API_SETVIEWREACTOR			= "setViewReactor"

# must selective
SETREACTOR_REACT			= "react"
SETREACTOR_REACTORS			= "reactors"
SETREACTOR_DELAY			= "delay"
SETREACTOR_ACCEPTS			= "accepts"
SETREACTOR_INJECTIONS		= [SETREACTOR_REACT, SETREACTOR_DELAY]

REACTOR_VIEWKEY_VIEWSELF	= "view"
REACTOR_VIEWKEY_ID			= "viewId"
REACTOR_VIEWKEY_BUFFERID	= "bufferId"
REACTOR_VIEWKEY_PATH		= "path"
REACTOR_VIEWKEY_NAME		= "name"
REACTOR_VIEWKEY_VNAME		= "vname"
REACTOR_VIEWKEY_SELECTEDS	= "selecteds"
REACTOR_VIEWKEY_ISEXIST		= "isExist"
REACTOR_VIEWKEY_EMITIDENTITY= "identity"
REACTOR_VIEWKEY_INJECTIONS	= [REACTOR_VIEWKEY_EMITIDENTITY, REACTOR_VIEWKEY_VIEWSELF, REACTOR_VIEWKEY_SELECTEDS, REACTOR_VIEWKEY_PATH, REACTOR_VIEWKEY_NAME, REACTOR_VIEWKEY_ISEXIST]

REACTORTYPE_EVENT			= "event"
REACTORTYPE_VIEW			= "view"


API_RESETREACTORS			= "resetReactors"
RESETREACTORS_DELETEDS		= "deleteds"
RESETREACTORS_INJECTIONS	= [RESETREACTORS_DELETEDS]


API_VIEWEMIT				= "viewEmit"
VIEWEMIT_NAME				= "name"
VIEWEMIT_VIEW				= "view"
VIEWEMIT_DELAY				= "delay"
VIEWEMIT_VIEWSELF			= "view"
VIEWEMIT_BODY				= "body"
VIEWEMIT_PATH				= "path"
VIEWEMIT_MODIFIEDPATH		= "modifiedpath"
VIEWEMIT_ROWCOL				= "rowcol"
VIEWEMIT_INJECTIONS 		= [VIEWEMIT_BODY, VIEWEMIT_PATH, VIEWEMIT_NAME, VIEWEMIT_MODIFIEDPATH, VIEWEMIT_ROWCOL]


API_EVENTEMIT				= "eventEmit"
EVENTEMIT_EVENT				= "event"
EVENTEMIT_INJECTIONS		= [EVENTEMIT_EVENT]


REACTIVE_PREFIX_USERDEFINED_EVENT	= "event_"
REACTIVE_PREFIX_SUBLIMESOCKET_EVENT = "ss_f_"
REACTIVE_PREFIXIES					= [REACTIVE_PREFIX_USERDEFINED_EVENT, REACTIVE_PREFIX_SUBLIMESOCKET_EVENT]

REACTIVE_FOUNDATION_EVENT			= [SS_FOUNDATION_NOVIEWFOUND]
REACTIVE_CURRENT_COMPLETINGS		= "currentcompletings"




# view series

API_MODIFYVIEW				= "modifyView"
MODIFYVIEW_VIEW				= "view"
MODIFYVIEW_NAME				= "name"
MODIFYVIEW_PATH				= "path"
MODIFYVIEW_ADD				= "add"
MODIFYVIEW_TO				= "to"
MODIFYVIEW_LINE				= "line"
MODIFYVIEW_REDUCE			= "reduce"
MODIFYVIEW_INJECTIONS		= [MODIFYVIEW_PATH, MODIFYVIEW_NAME, MODIFYVIEW_LINE, MODIFYVIEW_TO]


"""
@apiGroup getViewSetting
@api {SushiJSON} getViewSetting:{JSON} get setting of the file.

@apiExample [example]
getViewSetting: {
    "name": "sample.txt",
    "selectors": [
        {
            "showAtLog<-indentationsize, usingspace": {
                "format": "size?:[indentationsize], is using tab?:[usingspace]"
            }
        }
    ]
}

@apiParam {String} name the target file's last part of file path or fullpath or parts.
@apiParam {Selectors(Optional)} selectors selectors.

@apiSuccess {String} indentationsize size of indentation tab.
@apiSuccess {Bool} usingspace using space for indentation or not.
"""
API_GETVIEWSETTING          = "getViewSetting"
GETVIEWSETTING_VIEW         = "view"
GETVIEWSETTING_NAME         = "name"
GETVIEWSETTING_PATH         = "path"
GETVIEWSETTING_INDENTATIONSIZE  = "indentationsize"
GETVIEWSETTING_USINGSPACE   = "usingspace"
GETVIEWSETTING_INJECTIONS   = [GETVIEWSETTING_INDENTATIONSIZE, GETVIEWSETTING_USINGSPACE]


"""
@apiGroup setSelection
@api {SushiJSON} setSelection:{JSON} set selection to the file.

@apiExample [example]
setSelection: {
    "name": "sample.txt",
    "selections": [
        {
            "from": 10,
            "to": 11
        }
    ]
}

@apiParam {String} name the target file's last part of file path or fullpath or parts.
@apiParam {Dictionary} selections pair of key-value of selecting regions. [from]:Int and [to]:Int
@apiParam {Selectors(Optional)} selectors selectors.

@apiSuccess {Event} ss_on_selection_modified_by_setselection the ss_on_selection_modified_by_setselection event will raise.

@apiSuccess {String} path selected file's path.
@apiSuccess {String} name selected file's name.
@apiSuccess {Array} selecteds the list of [from] and [to].
"""
API_SETSELECTION			= "setSelection"
SETSELECTION_VIEW			= "view"
SETSELECTION_NAME			= "name"
SETSELECTION_PATH			= "path"
SETSELECTION_SELECTIONS		= "selections"
SETSELECTION_FROM			= "from"
SETSELECTION_TO				= "to"
SETSELECTION_SELECTEDS		= "selecteds"
SETSELECTION_INJECTIONS		= [SETSELECTION_PATH, SETSELECTION_NAME, SETSELECTION_SELECTEDS]
SS_VIEW_ON_SELECTION_MODIFIED_BY_SETSELECTION = "ss_on_selection_modified_by_setselection"


API_CLEARSELECTION			= "clearSelection"
CLEARSELECTION_VIEW			= "view"
CLEARSELECTION_NAME			= "name"
CLEARSELECTION_PATH			= "path"
CLEARSELECTION_CLEARDS		= "cleards"
CLEARSELECTION_INJECTIONS	= [CLEARSELECTION_PATH, CLEARSELECTION_NAME, CLEARSELECTION_CLEARDS]


API_DEFINEFILTER				= "defineFilter"
DEFINEFILTER_FILTERS			= "filters"
DEFINEFILTER_PATTERNS			= "patterns"
DEFINEFILTER_NAME 				= "name"
DEFINEFILTER_DOTALL				= "dotall"
DEFINEFILTER_COMMENT			= "comments"
DEFINEFILTER_INJECTIONS			= [DEFINEFILTER_NAME, DEFINEFILTER_PATTERNS]


API_FILTERING					= "filtering"
FILTERING_NAME					= "name"
FILTERING_SOURCE				= "source"
FILTERING_DEBUG					= "debug"


API_SELECTEDREGIONS				= "selectedRegions"
SELECTEDREGIONS_SELECTEDS		= "selecteds"
SELECTEDREGIONS_ISEXACTLY		= "isexactly"
SELECTEDREGIONS_ISSAMELINE		= "issameline"
SELECTEDREGIONS_VIEW			= "view"
SELECTEDREGIONS_NAME			= "name"
SELECTEDREGIONS_PATH			= "path"
SELECTEDREGIONS_CROSSED			= "crossed"
SELECTEDREGIONS_ONLYONE			= "onlyone"
SELECTEDREGIONS_LINE			= "line"
SELECTEDREGIONS_FROM			= "from"
SELECTEDREGIONS_TO				= "to"
SELECTEDREGIONS_MESSAGES		= "messages"
SELECTEDREGIONS_INJECTIONS 		= [SELECTEDREGIONS_PATH, SELECTEDREGIONS_NAME, SELECTEDREGIONS_CROSSED, SELECTEDREGIONS_LINE, SELECTEDREGIONS_FROM, SELECTEDREGIONS_TO, SELECTEDREGIONS_MESSAGES]


API_COLLECTVIEWS				= "collectViews"
COLLECTVIEWS_COLLECTEDS			= "collecteds"
COLLECTVIEWS_INJECTIONS 		= [COLLECTVIEWS_COLLECTEDS]


API_APPENDREGION			= "appendRegion"
APPENDREGION_NAME			= "name"
APPENDREGION_VIEW			= "view"
APPENDREGION_PATH			= "path"
APPENDREGION_IDENTITY		= "identity"
APPENDREGION_LINE			= "line"
APPENDREGION_FROM			= "from"
APPENDREGION_TO				= "to"
APPENDREGION_MESSAGE		= "message"
APPENDREGION_CONDITION 		= "condition"
APPENDREGION_INJECTIONS		= [APPENDREGION_PATH, APPENDREGION_NAME, APPENDREGION_IDENTITY, APPENDREGION_LINE, APPENDREGION_FROM, APPENDREGION_TO, APPENDREGION_MESSAGE, APPENDREGION_CONDITION]


API_ERASEALLREGIONS			= "eraseAllRegions"
ERASEALLREGIONS_NAME		= "name"
ERASEALLREGIONS_DELETES		= "deletes"
ERASEALLREGIONS_INJECTIONS	= [ERASEALLREGIONS_DELETES]



# other series

API_RUNSHELL					= "runShell"
RUNSHELL_MAIN					= "main"
RUNSHELL_DELAY					= "delay"
RUNSHELL_DEBUG					= "debug"
RUNSHELL_LIST_IGNORES 			= [RUNSHELL_MAIN, RUNSHELL_DELAY, RUNSHELL_DEBUG]
RUNSHELL_REPLACE_SPACE			= "_"
RUNSHELL_REPLACE_RIGHTBRACE 	= ""
RUNSHELL_REPLACE_LEFTBRACE		= ""
RUNSHELL_REPLACE_SINGLEQUOTE 	= ""
RUNSHELL_REPLACE_At_s_At_s_At	= " "


API_BROADCASTMESSAGE		= "broadcastMessage"
BROADCASTMESSAGE_TARGETS	= "targets"
BROADCASTMESSAGE_FORMAT		= "format"
BROADCASTMESSAGE_MESSAGE	= "message"
BROADCASTMESSAGE_INJECTIONS	= [BROADCASTMESSAGE_TARGETS, BROADCASTMESSAGE_MESSAGE]


API_MONOCASTMESSAGE			= "monocastMessage"
MONOCASTMESSAGE_TARGET		= "target"
MONOCASTMESSAGE_FORMAT		= "format"
MONOCASTMESSAGE_MESSAGE		= "message"
MONOCASTMESSAGE_INJECTIONS	= [MONOCASTMESSAGE_TARGET, MONOCASTMESSAGE_MESSAGE]


API_SHOWSTATUSMESSAGE		= "showStatusMessage"
SHOWSTATUSMESSAGE_MESSAGE	= "message"
SHOWSTATUSMESSAGE_DEBUG		= "debug"


API_SHOWATLOG				= "showAtLog"
LOG_FORMAT					= "format"
LOG_MESSAGE					= "message"
LOG_prefix					= "ss:"


API_SHOWDIALOG				= "showDialog"
SHOWDIALOG_FORMAT			= "format"
SHOWDIALOG_MESSAGE			= "message"
SHOWDIALOG_INJECTIONS		= [SHOWDIALOG_MESSAGE]


API_SHOWTOOLTIP				= "showToolTip"
SHOWTOOLTIP_VIEW			= "view"
SHOWTOOLTIP_NAME			= "name"
SHOWTOOLTIP_PATH			= "path"
SHOWTOOLTIP_ONSELECTED		= "onselected"
SHOWTOOLTIP_ONCANCELLED		= "oncancelled"
SHOWTOOLTIP_FINALLY			= "finally"
SHOWTOOLTIP_SELECTEDTITLE	= "selectedtitle"
SHOWTOOLTIP_TITLES			= "titles"
SHOWTOOLTIP_INJECTIONS		= [SHOWTOOLTIP_PATH, SHOWTOOLTIP_NAME, SHOWTOOLTIP_TITLES, SHOWTOOLTIP_SELECTEDTITLE]


API_SCROLLTO				= "scrollTo"
SCROLLTO_VIEW				= "view"
SCROLLTO_NAME				= "name"
SCROLLTO_LINE				= "line"
SCROLLTO_COUNT				= "count"
SCROLLTO_INJECTIONS			= []


API_TRANSFORM				= "transform"
TRANSFORM_PATH				= "transformerpath"
TRANSFORM_CODE				= "code"
TRANSFORM_DEBUG				= "debug"


API_NOTIFY					= "notify"
NOTIFY_TITLE				= "title"
NOTIFY_MESSAGE				= "message"
NOTIFY_DEBUG				= "debug"
NOTIFY_INJECTIONS			= [NOTIFY_TITLE, NOTIFY_MESSAGE]


API_GETALLFILEPATH			= "getAllFilePath"
GETALLFILEPATH_ANCHOR		= "anchor"
GETALLFILEPATH_LIMIT		= "limit"
GETALLFILEPATH_BASEDIR		= "basedir"
GETALLFILEPATH_PATHS		= "paths"
GETALLFILEPATH_FULLPATHS	= "fullpaths"
GETALLFILEPATH_INJECTIONS	= [GETALLFILEPATH_BASEDIR, GETALLFILEPATH_PATHS, GETALLFILEPATH_FULLPATHS]

	
API_READFILE				= "readFile"
READFILE_ORIGINALPATH		= "originalpath"
READFILE_PATH				= "path"
READFILE_DATA				= "data"
READFILE_INJECTIONS			= [READFILE_ORIGINALPATH, READFILE_PATH, READFILE_DATA]

	
API_CANCELCOMPLETION		= "cancelCompletion"
CANCELCOMPLETION_VIEW		= "view"
CANCELCOMPLETION_NAME		= "name"
CANCELCOMPLETION_INJECTIONS = []


"""
@apiGroup runCompletion
@api {SushiJSON} runCompletion:{JSON} show completion candidate datas. 

@apiExample [example]
runCompletion: {
    "name": "completionTestView.txt",
    "completion": [
        {
            "HEAD": "DrawLine",
            "paramsTargetFmt": "(${1:start}, ${2:end}, ${3:color}, ${4:duration}, ${5:depthTest})",
            "return": "Void",
            "paramsTypeDef": "(Vector3,Vector3,Color,Single,Boolean)",
            "head": "DrawLine"
        }
    ],
    "formathead": "HEADparamsTypeDef\treturn",
    "formattail": "headparamsTargetFmt$0",
    "selectors": [
        {
            "showAtLog<-name": {
                "format": "[name]"
            }
        }
    ]
}

@apiParam {String} name the target file's last part of file path or fullpath or parts.
@apiParam {String} completion parts of completion string sources. Will become completion string.
@apiParam {String} formathead header part of completion string. constructed bt the contents of completion's key-value.
@apiParam {String} formattail footer part of completion string. constructed bt the contents of completion's key-value.
@apiParam {String(Optional)} pool identity of completion pool. use for pooling completion resource. Will show when 'show' parameter appended.
@apiParam {String(Optional)} show key identity of showing pooled completions. if identity & this 'show' param exist and has same value, show pooled completions.
@apiParam {Selectors(Optional)} selectors selectors.

@apiSuccess {String} path file's path.
@apiSuccess {String} name file's name.
"""	
API_RUNCOMPLETION			= "runCompletion"
RUNCOMPLETION_VIEW			= "view"
RUNCOMPLETION_PATH			= "path"
RUNCOMPLETION_NAME			= "name"
RUNCOMPLETION_COMPLETIONS	= "completion"
RUNCOMPLETION_FORMATHEAD	= "formathead"
RUNCOMPLETION_FORMATTAIL	= "formattail"
RUNCOMPLETION_POOL          = "pool"
RUNCOMPLETION_SHOW          = "show"
RUNCOMPLETION_INJECTIONS	= [RUNCOMPLETION_PATH, RUNCOMPLETION_NAME]


API_FORCELYSAVE				= "forcelySave"
FORCELYSAVE_VIEW			= "view"
FORCELYSAVE_PATH			= "path"
FORCELYSAVE_NAME			= "name"
FORCELYSAVE_INJECTIONS		= [FORCELYSAVE_PATH, FORCELYSAVE_NAME]


API_SETSUBLIMESOCKETWINDOWBASEPATH = "setSublimeSocketWindowBasePath"
SETSUBLIMESOCKETWINDOWBASEPATH_BASEPATH		= "basepath"
SETSUBLIMESOCKETWINDOWBASEPATH_BASENAME		= "basename"
SETSUBLIMESOCKETWINDOWBASEPATH_INJECTIONS	= [SETSUBLIMESOCKETWINDOWBASEPATH_BASEPATH, SETSUBLIMESOCKETWINDOWBASEPATH_BASENAME]


# definition of sublime's view events
REACTABLE_VIEW_ON_NEW				= "on_new"
REACTABLE_VIEW_ON_CLONE				= "on_clone"
REACTABLE_VIEW_ON_CLOSE				= "on_close"
REACTABLE_VIEW_ON_LOAD				= "on_load"
REACTABLE_VIEW_ON_MODIFIED			= "on_modified"
REACTABLE_VIEW_ON_QUERY_COMPLETIONS	= "on_query_completions"
REACTABLE_VIEW_ON_PRE_SAVE			= "on_pre_save"
REACTABLE_VIEW_ON_POST_SAVE			= "on_post_save"
REACTABLE_VIEW_ON_SELECTION_MODIFIED= "on_selection_modified"
REACTABLE_VIEW_SS_V_DECREASED		= "ss_v_decreased"
REACTABLE_VIEW_SS_V_INCREASED		= "ss_v_increased"


VIEW_EVENTS_RENEW			= [REACTABLE_VIEW_ON_POST_SAVE, REACTABLE_VIEW_ON_CLONE, REACTABLE_VIEW_ON_LOAD, SS_EVENT_COLLECT, SS_EVENT_LOADING, SS_EVENT_RENAMED] #list of acceptable-view renew event names.
VIEW_EVENTS_DEL				= [REACTABLE_VIEW_ON_CLOSE] #list of acceptable-view del event names.




