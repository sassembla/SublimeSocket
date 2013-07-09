# -*- coding: utf-8 -*-
import sublime, sublime_plugin

import os

import socket, threading, string, time
from SublimeWSClient import SublimeWSClient
from SublimeSocketAPI import SublimeSocketAPI
import SublimeSocketAPISettings

import json
import uuid

import re

from PythonSwitch import PythonSwitch

SERVER_INTERVAL_SEC = 2000

class SublimeWSServer:

	def __init__(self):
		self.clients = {}
		
		self.socket = ''
		self.host = ''
		self.port = ''

		self.listening = False
		self.kvs = KVS()
		self.api = SublimeSocketAPI(self)
		self.temporaryEventDict = {}

		self.deletedRegionIdPool = []
		self.viewSize = -1


	def start(self, host, port):
		self.host = host
		self.port = port
		self.socket = socket.socket()

		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		try:
			self.socket.bind((host,port))
		except socket.error, msg:
			print "error", msg[1]
			return 1

		self.socket.listen(1)
		
		serverStartMessage = 'SublimeSocket WebSocketServing started @ ' + str(host) + ':' + str(port)
		print '\n', serverStartMessage, "\n"
		sublime.set_timeout(lambda: sublime.status_message(serverStartMessage), 0)

		# start serverControlIntervals
		# sublime.set_timeout(lambda: self.intervals(), SERVER_INTERVAL_SEC)

		# load settings
		sublime.set_timeout(lambda: self.loadSettings(), 0)


		self.listening = True
		while self.listening:
			(conn, addr) = self.socket.accept()

			if self.listening is None:
				return 0
			
			identity = str(uuid.uuid4())

			# genereate new client
			client = SublimeWSClient(self, identity)
			
			self.clients[identity] = client

			threading.Thread(target = client.handle, args = (conn,addr)).start()
				
		return 0


	## interval
	def intervals(self):
		# check KVS for "eventListen", and the other APIs.
		
		for key in SublimeSocketAPISettings.INTERVAL_DEPEND_APIS:
			pass
			# self.api.runOnInterval(self.getV(key))

		# sublime.set_timeout(lambda: sublime.status_message("params:\n".join(debugArray)), 0)
		
		# loop
		sublime.set_timeout(lambda: self.intervals(), SERVER_INTERVAL_SEC)
		

	## load settings and run in mainThread
	def loadSettings(self):
		settingCommands = sublime.load_settings("SublimeSocket.sublime-settings").get('loadSettings')
		for command in settingCommands:
			self.api.runAPI(command)

	## update specific client's id
	def updateClientId(self, client, params):
		assert client, "updateClientId requre 'client should not be None'"
		assert params.has_key(SublimeSocketAPISettings.IDENTITY_ID), "updateClientId requre 'id' param"

		newIdentity = params[SublimeSocketAPISettings.IDENTITY_ID]

		currentClient = self.clients[client.clientId]

		# del from list
		self.deleteClientId(currentClient.clientId)

		# update
		client.clientId = newIdentity
		self.clients[newIdentity] = client	

	# remove from Client dict
	def deleteClientId(self, clientId):
		if self.clients.has_key(clientId):
			del self.clients[clientId]
		else:
			print "ss: server don't know about client:", clientId

	## api 
	def callAPI(self, apiData, clientId):
		currentClient = [client for client in self.clients.values() if client.clientId == clientId][0]
		
		self.api.parse(apiData, currentClient)

		
	## tearDown the server
	def tearDown(self):
		for clientId in self.clients:
			client = self.clients[clientId]
			client.close()

		self.clients = None

		# no mean?
		self.socket.close()
		
		# stop receiving
		self.listening = False
		

		self.kvs.clear()
		
		serverTearDownMessage = 'SublimeSocket WebSocketServing tearDown @ ' + str(self.host) + ':' + str(self.port)
		print '\n', serverTearDownMessage, "\n"
		sublime.set_timeout(lambda: sublime.status_message(serverTearDownMessage), 0)


	## return the filter has been defined or not
	def isFilterDefined(self, filterName):
		if self.isExistOnKVS(SublimeSocketAPISettings.DICT_FILTERS):
			filterDict = self.kvs.get(SublimeSocketAPISettings.DICT_FILTERS)
			if filterName in filterDict:
				return True
		return False

	## collect current views
	def collectViews(self):
		for views in [window.views() for window in sublime.windows()]:
			for view in views:
				self.fireKVStoredItem(SublimeSocketAPISettings.SS_EVENT_COLLECT, 
					{SublimeSocketAPISettings.VIEW_SELF:view}
				)
	
	## store region to viewDict-view in KVS
	def storeRegionToView(self, view, identity, region, line, message):
		key = view.file_name()
		specificViewDict = self.getV(SublimeSocketAPISettings.DICT_VIEWS)[key]

		regionDict = {}
		regionDict[SublimeSocketAPISettings.REGION_LINE] = line
		regionDict[SublimeSocketAPISettings.REGION_MESSAGE] = message
		regionDict[SublimeSocketAPISettings.REGION_SELF] = region
		
		# generate SUBDICT_REGIONS if not exist yet.
		if not specificViewDict.has_key(SublimeSocketAPISettings.SUBDICT_REGIONS):
			specificViewDict[SublimeSocketAPISettings.SUBDICT_REGIONS] = {}
			specificViewDict[SublimeSocketAPISettings.SUBARRAY_DELETED_REGIONS] = {}

		specificViewDict[SublimeSocketAPISettings.SUBDICT_REGIONS][identity] = regionDict


	## delete all regions in all view 
	def deleteAllRegionsInAllView(self):
		viewDict = self.getV(SublimeSocketAPISettings.DICT_VIEWS)
		
		def eraseAllRegionsAtViewDict(viewDictValue):
			if viewDictValue.has_key(SublimeSocketAPISettings.SUBDICT_REGIONS):
				viewInstance = viewDictValue[SublimeSocketAPISettings.VIEW_SELF]
				regionsDict = viewDictValue[SublimeSocketAPISettings.SUBDICT_REGIONS]
				
				if regionsDict:
					for regionIdentity in regionsDict.keys():
						viewInstance.erase_regions(regionIdentity)
						viewDictValue[SublimeSocketAPISettings.SUBARRAY_DELETED_REGIONS][regionIdentity] = 1
						
						del regionsDict[regionIdentity]

				[viewInstance.erase_regions(regionIdentity) for regionIdentity in viewDictValue[SublimeSocketAPISettings.SUBARRAY_DELETED_REGIONS].keys()]
				
		if viewDict:
			map(eraseAllRegionsAtViewDict, viewDict.values())

	## generate thread per selector. or add
	def setOrAddReactor(self, params, client):
		target = params[SublimeSocketAPISettings.REACTOR_TARGET]
		event = params[SublimeSocketAPISettings.REACTOR_EVENT]
		selectorsArray = params[SublimeSocketAPISettings.REACTOR_SELECTORS]

		if event in SublimeSocketAPISettings.REACTIVE_RESERVED_INTERVAL_EVENT:
			assert params.has_key(SublimeSocketAPISettings.REACTOR_INTERVAL), "this type of event require 'interval' param."

		# check event kind
		# delete when set the reactor of the event.
		if event in self.temporaryEventDict:
			del self.temporaryEventDict[event]
		
		# set default interval
		interval = 0
		if SublimeSocketAPISettings.REACTOR_INTERVAL in params:
			interval = params[SublimeSocketAPISettings.REACTOR_INTERVAL]

		reactorsDict = {}
		if self.isExistOnKVS(SublimeSocketAPISettings.DICT_REACTORS):
			reactorsDict = self.getV(SublimeSocketAPISettings.DICT_REACTORS)

		reactDict = {}
		reactDict[SublimeSocketAPISettings.REACTOR_SELECTORS] = selectorsArray
		reactDict[SublimeSocketAPISettings.REACTOR_INTERVAL] = interval

		if SublimeSocketAPISettings.REACTOR_REPLACEFROMTO in params:
			reactDict[SublimeSocketAPISettings.REACTOR_REPLACEFROMTO] = params[SublimeSocketAPISettings.REACTOR_REPLACEFROMTO]

		# already set or not-> spawn dictionary for event.
		if event in reactorsDict:
			pass
		else:
			reactorsDict[event] = {}
		
		# store reactor			
		reactorsDict[event][target] = reactDict
		self.setKV(SublimeSocketAPISettings.DICT_REACTORS, reactorsDict)
		
		if 0 < interval:
			# spawn event-loop for event execution
			sublime.set_timeout(lambda: self.eventIntervals(target, event, selectorsArray, interval), interval)


	## interval execution for event
	def eventIntervals(self, target, event, selectorsArray, interval):

		reactorsDict = self.getV(SublimeSocketAPISettings.DICT_REACTORS)

		# return if empty
		if not reactorsDict:
			return

		# if exist, continue
		if not reactorsDict.has_key(event):
			return

		if not reactorsDict[event].has_key(target):
			return

		if reactorsDict[event][target]:
			
			reactorDict = reactorsDict[event][target]

			if self.temporaryEventDict.has_key(event):
				# get latest event
				eventParam = self.temporaryEventDict[event]
				
				# consume event
				del self.temporaryEventDict[event]

				# run all selector
				self.runAllSelector(reactorDict, selectorsArray, eventParam)

			# continue
			sublime.set_timeout(lambda: self.eventIntervals(target, event, selectorsArray, interval), interval)


	# run user-defined event.
	def runOrSetUserDefinedEvent(self, eventName, eventParam, reactorsDict):
		# emit now or set to fire with interval
		if reactorsDict.has_key(SublimeSocketAPISettings.REACTOR_INTERVAL):
			self.temporaryEventDict[eventName] = eventParam
			return

		# emit now
		target = eventParam[SublimeSocketAPISettings.REACTOR_TARGET]
		reactDict = reactorsDict[eventName][target]
		
		selector = reactDict[SublimeSocketAPISettings.REACTOR_SELECTORS]

		self.runAllSelector(reactDict, selector, eventParam)

	def runAllSelector(self, reactorDict, selectorsArray, eventParam):
		def runForeachAPI(selector):
			# {u'broadcastMessage': {u'message': u"text's been modified!"}}

			command = selector.keys()[0]
			params = selector[command]

			# print "params", params, "command", command

			# replace parameters if key 'replace' exist
			if reactorDict.has_key(SublimeSocketAPISettings.REACTOR_REPLACEFROMTO):
				for fromKey in reactorDict[SublimeSocketAPISettings.REACTOR_REPLACEFROMTO].keys():
					toKey = reactorDict[SublimeSocketAPISettings.REACTOR_REPLACEFROMTO][fromKey]
					
					# replace or append
					params[toKey] = eventParam[fromKey]

			self.api.runAPI(command, params)

		[runForeachAPI(selector) for selector in selectorsArray]



	## emit event if params matches the regions that sink in view
	def containsRegions(self, params):
		if self.isExistOnKVS(SublimeSocketAPISettings.DICT_VIEWS):
			
			viewDict = self.getV(SublimeSocketAPISettings.DICT_VIEWS)

			assert params.has_key(SublimeSocketAPISettings.CONTAINSREGIONS_VIEW), "containsRegions require 'view' param"
			assert params.has_key(SublimeSocketAPISettings.CONTAINSREGIONS_TARGET), "containsRegions require 'target' param"
			assert params.has_key(SublimeSocketAPISettings.CONTAINSREGIONS_EMIT), "containsRegions require 'emit' param"


			# specify regions that are selected.
			viewInstance = params[SublimeSocketAPISettings.CONTAINSREGIONS_VIEW]
			viewId = viewInstance.file_name()

			# return if view not exist(include ST's console)
			if not viewDict.has_key(viewId):
				return

			viewInfoDict = viewDict[viewId]
			if viewInfoDict.has_key(SublimeSocketAPISettings.SUBDICT_REGIONS):
				regionsDicts = viewInfoDict[SublimeSocketAPISettings.SUBDICT_REGIONS]

				selectedRegionSet = viewInstance.sel()
				
				# identity
				def isRegionMatchInDict(dictKey):
					currentRegion = regionsDicts[dictKey][SublimeSocketAPISettings.REGION_SELF]
					if selectedRegionSet.contains(currentRegion):
						return dictKey
				

				regionIdentitiesListWithNone = [isRegionMatchInDict(key) for key in regionsDicts.keys()]

				# collect if exist
				regionIdentitiesList = [val for val in regionIdentitiesListWithNone if val]
				

				target = params[SublimeSocketAPISettings.CONTAINSREGIONS_TARGET]
				emit = params[SublimeSocketAPISettings.CONTAINSREGIONS_EMIT]
				
				# emit event of regions
				def emitRegionMatchEvent(key):
					regionInfo = regionsDicts[key]

					# append target
					regionInfo[SublimeSocketAPISettings.REACTOR_TARGET] = target
					self.fireKVStoredItem(emit, regionInfo)
					
					if params.has_key(SublimeSocketAPISettings.CONTAINSREGIONS_DEBUG):
						debug = params[SublimeSocketAPISettings.CONTAINSREGIONS_DEBUG]
						if debug:
							message = regionInfo[SublimeSocketAPISettings.APPENDREGION_MESSAGE]

							messageDict = {}
							messageDict[SublimeSocketAPISettings.SHOWSTATUSMESSAGE_MESSAGE] = message
							self.api.runAPI(SublimeSocketAPISettings.API_I_SHOWSTATUSMESSAGE, messageDict)
							self.api.printout(message)

				[emitRegionMatchEvent(region) for region in regionIdentitiesList]
				

	## show current status & connectionIds
	def showCurrentStatusAndConnections(self):
		print "ss: server host:", self.host, "	port:", self.port
		
		print "ss: connections:"
		for client in self.clients:
			print "	", client


	## input to sublime from server.
	# fire event in KVS, if exist.
	def fireKVStoredItem(self, eventName, eventParam=None):
		# print "fireKVStoredItem eventListen!", eventName,"eventParam",eventParam

		# event listener adopt
		if eventName in SublimeSocketAPISettings.REACTIVE_RESERVED_INTERVAL_EVENT:
			# store data to temporary.
			self.temporaryEventDict[eventName] = eventParam


		# run when the event occured adopt. start with specific "user-defined" event identity that defined as REACTIVE_PREFIX_USERDEFINED_EVENT.
		if eventName.startswith(SublimeSocketAPISettings.REACTIVE_PREFIX_USERDEFINED_EVENT):
			reactorsDict = self.getV(SublimeSocketAPISettings.DICT_REACTORS)
			
			# if exist, continue
			if eventName in reactorsDict:
				# interval-set or not
				self.runOrSetUserDefinedEvent(eventName, eventParam, reactorsDict)


		# run when the foundation-event occured adopt
		if eventName in SublimeSocketAPISettings.REACTIVE_FOUNDATION_EVENT:
			# emit now if exist
			reactorsDict = self.getV(SublimeSocketAPISettings.DICT_REACTORS)
			
			# if exist, continue
			if eventName in reactorsDict:
				self.runFoundationEvent(eventName, eventParam, reactorsDict)


		# viewCollector "renew" will react
		if eventName in SublimeSocketAPISettings.VIEW_EVENTS_RENEW:
			viewInstance = eventParam[SublimeSocketAPISettings.VIEW_SELF]

			if viewInstance.is_scratch():
				# print "scratch buffer."
				pass
				
			elif not viewInstance.file_name():
				# print "no path"
				pass

			else:
				viewDict = {}
				
				# update or append if exist.
				if self.isExistOnKVS(SublimeSocketAPISettings.DICT_VIEWS):
					viewDict = self.getV(SublimeSocketAPISettings.DICT_VIEWS)

				# create
				else:	
					pass

				filePath = viewInstance.file_name()

				viewInfo = {}
				if filePath in viewDict:
					viewInfo = viewDict[filePath]	

				viewInfo[SublimeSocketAPISettings.VIEW_ID] = viewInstance.id()
				viewInfo[SublimeSocketAPISettings.VIEW_BUFFERID] = viewInstance.buffer_id()
				viewInfo[SublimeSocketAPISettings.VIEW_BASENAME] = os.path.basename(viewInstance.file_name())
				viewInfo[SublimeSocketAPISettings.VIEW_VNAME] = viewInstance.name()
				viewInfo[SublimeSocketAPISettings.VIEW_SELF] = viewInstance
				
				# add
				viewDict[filePath] = viewInfo
				self.setKV(SublimeSocketAPISettings.DICT_VIEWS, viewDict)


		# viewCollector "del" will react
		if eventName in SublimeSocketAPISettings.VIEW_EVENTS_DEL:
			viewInstance = eventParam[SublimeSocketAPISettings.VIEW_SELF]

			viewDict = {}
			
			# get view-dictionary if exist.
			if self.isExistOnKVS(SublimeSocketAPISettings.DICT_VIEWS):
				viewDict = self.getV(SublimeSocketAPISettings.DICT_VIEWS)

			# create
			else:	
				return

			filePath = viewInstance.file_name()

			# delete
			if filePath in viewDict:
				del viewDict[filePath]
				self.setKV(SublimeSocketAPISettings.DICT_VIEWS, viewDict)

		# completion triggers will react
		if eventName in SublimeSocketAPISettings.VIEW_EVENTS_COMPLETION:
			# get filter key-values array
			completionkeywordsArray = self.getV(SublimeSocketAPISettings.DICT_COMPLETIONS)
			if 0 < len(completionkeywordsArray):
				self.runCompletionOrNot(completionkeywordsArray, eventParam)


	def runFoundationEvent(self, eventName, eventParam, reactorsDict):
		for case in PythonSwitch(eventName):
			if case(SublimeSocketAPISettings.SS_FOUNDATION_NOVIEWFOUND):
				reactDict = reactorsDict[eventName][SublimeSocketAPISettings.FOUNDATIONREACTOR_TARGET_DEFAULT]
			
				selector = reactDict[SublimeSocketAPISettings.REACTOR_SELECTORS]

				self.runAllSelector(reactDict, selector, eventParam)
				break

			if case(SublimeSocketAPISettings.SS_FOUNDATION_RUNWITHBUFFER):
				
				for currentDict in reactorsDict[eventName]:
					# get data from view-buffer
					bodyView = eventParam[SublimeSocketAPISettings.F_RUNWITHBUFFER_VIEW]

					currentRegion = sublime.Region(0, 0)

					# continue until size not changed.
					before = -1
					count = 1

					while True:
						if currentRegion.b == before:
							break

						before = currentRegion.b
						currentRegion = bodyView.word(sublime.Region(0, SublimeSocketAPISettings.SIZE_OF_BUFFER * count))

						count = count + 1

					body = bodyView.substr(bodyView.word(currentRegion))
					path = bodyView.file_name()

					reactDict = reactorsDict[eventName][currentDict]

					# append 'body' 'path' param from buffer
					eventParam[SublimeSocketAPISettings.F_RUNWITHBUFFER_BODY] = body
					eventParam[SublimeSocketAPISettings.F_RUNWITHBUFFER_PATH] = path

					selector = reactDict[SublimeSocketAPISettings.REACTOR_SELECTORS]
					
					self.runAllSelector(reactDict, selector, eventParam)

				break
				
			if case():
				print "unknown foundation api", command
				break

	def runCompletionOrNot (self, completionDefines, eventParam):
		view = eventParam[SublimeSocketAPISettings.VIEW_SELF]
				
		currentSize = view.size()
		compare = self.viewSize
		self.viewSize = currentSize

		if compare < currentSize:
			pass
		else:# not gain.
			return

		# pick up first selection only
		if 1 < len(view.sel()):
			return

		sel = view.sel()[0]

		# latest input
		enteredText = view.substr(sublime.Region(sel.a-1, sel.b))
		
		for completion in completionDefines:
			if enteredText in  completion[SublimeSocketAPISettings.DEFINECOMPLETIONTRIGGERS_KEYWORDS]:
				print("bingo!", enteredText)
				# トリガーが引けた。これを編集可能にすること。
				# 補完のトリガーを引く。で、受けを作る。
				# ここまででこの補完を実行する事が確定したので、completionInfoを使ってviewから情報を抜き出して、selectorに放り込む
				# ひゃー、大仕事。
				
				
	## KVSControl
	def KVSControl(self, subCommandAndParam):
		if 1 < len(subCommandAndParam):
			return "KVSControl: too many subCommands. please set only one subCommnad."

		subCommnad = subCommandAndParam.keys()[0]
		param = subCommandAndParam.values()[0]

		# python-switch
		for case in PythonSwitch(subCommnad):
			if case(SublimeSocketAPISettings.KVS_SHOWALL):
				return self.showAll()
				break

			if case(SublimeSocketAPISettings.KVS_SHOWVALUE):
				return self.showValue(param)
				break

			if case(SublimeSocketAPISettings.KVS_REMOVEVALUE):
				return self.remove(param)
				break
				
			if case(SublimeSocketAPISettings.KVS_CLEAR):
				return self.clear()
				break

			if case():
				print "unknown KVS subcommand"
				break


	## return view dict
	def viewDict(self):
		return self.kvs.get(SublimeSocketAPISettings.DICT_VIEWS)


	## put key-value onto KeyValueStore
	def setKV(self, key, value):
		self.kvs.setKeyValue(key, value)


	## return None or object
	def getV(self, key):
		value = self.kvs.get(key)
		return value

	
	## exist or not. return bool
	def isExistOnKVS(self, key):
		if self.kvs.get(key):
			# print "isExistOnKVS true", self.kvs.get(key)
			return True
			
		else:
			# print "isExistOnKVS false", self.kvs.get(key)
			return False

	## return all key-value as string
	def showAll(self):
		if self.kvs.isEmpty():
			return "No Keys - Values. empty."

		v = self.kvs.items()
		printKV = []
		for kvTuple in v:
			kvsStr = str(kvTuple[0]) + " : " + str(kvTuple[1])+ "	/	"
			printKV.append(kvsStr)
		
		return "".join(printKV)


	## return single key-value as string
	def showValue(self, key):
		if not self.kvs.get(key):
			return str(False)
		
		kv = key + " : " + self.kvs.get(key)
		return str(kv)


	## clear all KVS contents
	def clear(self):
		self.kvs.clear()
		return str(True)
		

	def remove(self, key):
		result = self.kvs.remove(key)
		return str(result)

## key-value pool
class KVS:
	def __init__(self):
		self.keyValueDict = {}


	## empty or not
	def isEmpty(self):
		if 0 == len(self.keyValueDict):
			return True
		else:
			return False

		
	## set (override if exist already)
	def setKeyValue(self, key, value):
		if self.keyValueDict.has_key(key):
			# print "overwritten:", key, "as:", value
			pass

		self.keyValueDict[key] = value
		return self.keyValueDict[key]


	## get value for key
	def get(self, key):
		if self.keyValueDict.has_key(key):
			return self.keyValueDict[key]


	## get all key-value
	def items(self):
		return self.keyValueDict.items()


	## remove key-value
	def remove(self, key):
		if self.get(key):
			del self.keyValueDict[key]
			return True
		else:
			print "no '", key, "' key exists in KVS."
			return False


	## remove all keys and values
	def clear(self):
		self.keyValueDict.clear()
		return True

