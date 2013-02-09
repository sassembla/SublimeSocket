# -*- coding: utf-8 -*-
import sublime, sublime_plugin

import socket, threading, string, time
from SublimeWSClient import *
from SublimeSocketAPI import *
import SublimeSocketAPISettings

import json

from PythonSwitch import *

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
		if self.isExistOnKVS(SublimeSocketAPISettings.API_DEFINEFILTER):
			filterDict = self.kvs.get(SublimeSocketAPISettings.API_DEFINEFILTER)
			if filterName in filterDict:
				return True
		return False
			

	## input to sublime from server
	def fireKVStoredEvent(self, eventName):
		for key in SublimeSocketAPISettings.INTERVAL_DEPEND_APIS:
			if not isinstance(self.getV(key), dict):
				return

			if self.getV(key).has_key(eventName):

				# print "getV", self.getV(key)#{'on_modified': u'runShell2013/02/04 23:01:51'}
				eventKey = self.getV(key)[eventName]# array, [0] is API, others are parameters.

				# print "API_SETEVENT", self.getV(SublimeSocketAPISettings.API_SETEVENT)
				if self.getV(SublimeSocketAPISettings.API_SETEVENT).has_key(eventKey):
					
					commandAndParams = self.getV(SublimeSocketAPISettings.API_SETEVENT)[eventKey]
					# print "commandAndParams", commandAndParams[1]

					self.api.runAPI(commandAndParams[0], commandAndParams[1])	


	## put key-value onto KeyValueStore
	def setKV(self, key, value):
		print "should update! if same key is on, already"
		self.kvs.setKeyValue(key, value)


	def getV(self, key):
		value = self.kvs.get(key)
		return value
	
	def isExistOnKVS(self, key):
		if self.kvs.get(key):
			print "isExistOnKVS true", self.kvs.get(key)
			return True
			
		else:
			print "isExistOnKVS false", self.kvs.get(key)
			return False


## key-value pool
class KVS:
	def __init__(self):
		self.keyValueDict = {}


	## set
	def setKeyValue(self, key, value):
		self.keyValueDict[key] = value
		return self.keyValueDict[key]

	## get
	def get(self, key):
		if self.keyValueDict.has_key(key):
			return self.keyValueDict[key]

