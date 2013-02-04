# -*- coding: utf-8 -*-
import sublime, sublime_plugin

import socket, threading, string, time
from SublimeWSClient import *
from SublimeSocketAPI import *
import SublimeSocketAPISettings

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



	## input to sublime from server
	def fireKVStoredEvent(self, eventName):
		for key in SublimeSocketAPISettings.INTERVAL_DEPEND_APIS:
			if not isinstance(self.getV(key), dict):
				return

			if self.getV(key).has_key(eventName):

				# print "getV", self.getV(key)#{'on_modified': u'runShell2013/02/04 23:01:51'}
				eventKey = self.getV(key)[eventName]# array, [0] is API, others are parameters.

				# print "API_SET_KVSTOREEVENT", self.getV(SublimeSocketAPISettings.API_SET_KVSTOREEVENT)
				if self.getV(SublimeSocketAPISettings.API_SET_KVSTOREEVENT).has_key(eventKey):
					
					commandAndParams = self.getV(SublimeSocketAPISettings.API_SET_KVSTOREEVENT)[eventKey]
					# print "commandAndParams", commandAndParams
					self.api.runAPI(commandAndParams[0], commandAndParams[1:])	


	## connect to KeyValueStore
	def setKV(self, key, value):
		print "should update! if same key is on, already"
		self.kvs.setKeyValue(key, value)


	def getV(self, key):
		value = self.kvs.get(key)
		return value
		

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
		if not self.keyValueDict.has_key(key):
			print "key not found",key
			return ""
		return self.keyValueDict[key]

