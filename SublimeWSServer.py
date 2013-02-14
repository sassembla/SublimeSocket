# -*- coding: utf-8 -*-
import sublime, sublime_plugin

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

		self.listening = True
		while self.listening:
			(conn, addr) = self.socket.accept()
			
			client = SublimeWSClient(self)
			self.clients.append(client)

			print 'Total Clients:', str(len(self.clients))
			
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
			

	## input to sublime from server.
	# fire event in KVS, if exist.
	def fireKVStoredItem(self, eventName, eventParam=None):
		# event listener adopt
		if eventName in SublimeSocketAPISettings.LISTEN_EVENTS:
			print "eventName", eventName
		
		# # なんか、イベントの列挙にたいして応える側規定するのが正しい気がする、ミスった。
		# for key in SublimeSocketAPISettings.REACTABLE_APIS:
		# 	if not isinstance(self.getV(key), dict):
		# 		return

		# 	if self.getV(key).has_key(eventName):

		# 		# print "getV", self.getV(key) # {'on_modified': u'runShell2013/02/04 23:01:51'}
		# 		eventKey = self.getV(key)[eventName]# array, [0] is API, others are parameters.

		# 		# eventListener will react if set
		# 		if self.getV(SublimeSocketAPISettings.DICT_LISTENERS).has_key(eventKey):
					
		# 			commandAndParams = self.getV(SublimeSocketAPISettings.DICT_LISTENERS)[eventKey]
		# 			# print "commandAndParams", commandAndParams[1]

		# 			self.api.runAPI(commandAndParams[0], commandAndParams[1])	


		# 		# viewCollector will react
		# 		if self.getV(SublimeSocketAPISettings.DICT_VIEWS).has_key(eventKey):
		# 			pass

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
			print "isExistOnKVS true", self.kvs.get(key)
			return True
			
		else:
			print "isExistOnKVS false", self.kvs.get(key)
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
			print "overwritten:", key, "as:", value

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





