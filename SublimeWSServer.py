# -*- coding: utf-8 -*-
import sublime, sublime_plugin

import os

import socket, threading, string, time
from SublimeWSClient import SublimeWSClient
from SublimeSocketAPI import SublimeSocketAPI
import SublimeSocketAPISettings

import json

from PythonSwitch import PythonSwitch

SERVER_INTERVAL_SEC = 2000

class SublimeWSServer:

	def __init__(self):
		self.clients = []
		self.socket = ''
		self.listening = False
		self.kvs = KVS()
		self.api = SublimeSocketAPI(self)


	def start(self, host, port):
		self.socket = socket.socket()
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((host,port))
		
		self.socket.listen(0)
		
		print '\n', 'SublimeSocket WebSocketServing started @ ', host, ':', port, "\n"


		# start serverControlIntervals
		# sublime.set_timeout(lambda: self.intervals(), SERVER_INTERVAL_SEC)

		# load settings
		sublime.set_timeout(lambda: self.loadSettings(), 0)


		self.listening = True
		while self.listening:
			(conn, addr) = self.socket.accept()
			
			client = SublimeWSClient(self)
			self.clients.append(client)

			print 'Clients num:', str(len(self.clients))
			
			threading.Thread(target = client.handle, args = (conn,addr)).start()
			

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


	## api 
	def callAPI(self, apiData, clientId):
		currentClient = [client for client in self.clients if client.clientId == clientId][0]
		self.api.parse(apiData, currentClient)

		
	## kill server. with all connection(maybe some bugs include. will not be close immediately, at least 1 reload need,,)
	def killServerSelf(self):
		for client in self.clients:
			self.clients.remove(client)
			client.close()

		self.listening = False
		self.socket.close()		


	## return the filter has been defined or not
	def isFilterDefined(self, filterName):
		if self.isExistOnKVS(SublimeSocketAPISettings.DICT_FILTERS):
			filterDict = self.kvs.get(SublimeSocketAPISettings.DICT_FILTERS)
			if filterName in filterDict:
				return True
		return False
	
	
	## return the view has been defined or not
	def isViewDefined(self, viewParam):
		if not self.isExistOnKVS(SublimeSocketAPISettings.DICT_VIEWS):
			print "target view does not exist in KVS. :", viewParam
			return False

		# use file_name if path exists. (PATH)
		if viewParam.has_key(SublimeSocketAPISettings.VIEW_PATH):
			if viewParam[SublimeSocketAPISettings.VIEW_PATH] in self.kvs.get(SublimeSocketAPISettings.DICT_VIEWS):
				return True

		print "NO hit", viewParam
		return False

	## return current targetted view or None.
	def currentTargetView(self):
		if self.isExistOnKVS(SublimeSocketAPISettings.DICT_CURRENTTARGETVIEW):
			return self.getV(SublimeSocketAPISettings.DICT_CURRENTTARGETVIEW)[SublimeSocketAPISettings.VIEW_SELF]
		return None

	## return specific view instance from viewDict.
	def getViewInfo(self, viewParam):
		path = viewParam[SublimeSocketAPISettings.VIEW_PATH]
		viewInfo = self.getV(SublimeSocketAPISettings.DICT_VIEWS)[path]
		viewInfo[SublimeSocketAPISettings.VIEW_PATH] = path
		return viewInfo


	## collect current views
	def collectViews(self):
		for views in [window.views() for window in sublime.windows()]:
			for view in views:
				self.fireKVStoredItem(SublimeSocketAPISettings.SS_EVENT_COLLECT, view)

		
	## store region to viewDict-view in KVS
	def storeRegionToView(self, view, lineNum, comment, identity):
		key = view.file_name()
		specificViewDict = self.getV(SublimeSocketAPISettings.DICT_VIEWS)[key]

		region = {}
		region[SublimeSocketAPISettings.REGION_LINENUM] = lineNum
		region[SublimeSocketAPISettings.REGION_COMMENT] = comment
		
		if not specificViewDict.has_key(SublimeSocketAPISettings.SUBDICT_REGIONS):
			specificViewDict[SublimeSocketAPISettings.SUBDICT_REGIONS] = {}

		specificViewDict[SublimeSocketAPISettings.SUBDICT_REGIONS][identity] = region

	## delete all regions in all view 
	def deleteAllRegionsInAllView(self):
		# DICT_VIEWS の、　SUBDICT_REGIONS の、　key を合成する
		viewDict = self.getV(SublimeSocketAPISettings.DICT_VIEWS)

		def getIdentity(valueDict):
			if valueDict.has_key(SublimeSocketAPISettings.SUBDICT_REGIONS):
				regionsDict = valueDict[SublimeSocketAPISettings.SUBDICT_REGIONS]
				if regionsDict:
					return regionsDict.keys()

		identitiesWithNone = map(getIdentity, viewDict.values())
		# distinct "None"
		while None in identitiesWithNone: identitiesWithNone.remove(None)

		def expandLeft(before, next):
			# expand all list
			before.expand(next)
			return before
		
		identities = reduce(expandLeft, identitiesWithNone[1:], identitiesWithNone[0])
		return identities

	## input to sublime from server.
	# fire event in KVS, if exist.
	def fireKVStoredItem(self, eventName, eventParam=None):
		# print "fireKVStoredItem eventListen!", eventName,"eventParam",eventParam
		# event listener adopt
		if eventName in SublimeSocketAPISettings.LISTEN_EVENTS:
			if self.isExistOnKVS(SublimeSocketAPISettings.DICT_EVENTLISTENERS):
				commandAndParams = self.getV(SublimeSocketAPISettings.DICT_EVENTLISTENERS)[eventName].items()

				command = commandAndParams[0][0]
				params = commandAndParams[0][1]
				self.api.runAPI(command, params)	

		# viewCollector "renew" will react
		if eventName in SublimeSocketAPISettings.VIEW_EVENTS_RENEW:
			viewInstance = eventParam

			if viewInstance.is_scratch():
				# print "scratch buffer."
				pass
				
			elif not viewInstance.file_name():
				# print "no path"
				pass

			else:
				# print "open then add!!", eventParam
				viewDict = {}
				
				# update or append if exist.
				if self.isExistOnKVS(SublimeSocketAPISettings.DICT_VIEWS):
					viewDict = self.getV(SublimeSocketAPISettings.DICT_VIEWS)

				# create
				else:	
					pass

				filePath = viewInstance.file_name()

				viewInfo = {}
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
			viewInstance = eventParam

			viewDict = {}
			
			# get view-dictionary if exist.
			if self.isExistOnKVS(SublimeSocketAPISettings.DICT_VIEWS):
				viewDict = self.getV(SublimeSocketAPISettings.DICT_VIEWS)

			# create
			else:	
				return

			filePath = viewInstance.file_name()

			# delete
			if viewDict.has_key(filePath):
				del viewDict[filePath]
				self.setKV(SublimeSocketAPISettings.DICT_VIEWS, viewDict)



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
				print "param is", param
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


	## 
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





