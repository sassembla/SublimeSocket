# -*- coding: utf-8 -*-
import sublime, sublime_plugin

import socket, threading, string, time
from SublimeWSClient import *
from SublimeSocketAPI import *

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
		
		print 'SublimeSocket WebSocketServing started @ ', host, ':', port

		self.listening = True
		while self.listening:
			(conn, addr) = self.socket.accept()
			
			client = SublimeWSClient(self)
			self.clients.append(client)

			print 'Total Clients:', str(len(self.clients))
			
			threading.Thread(target = client.handle, args = (conn,addr)).start()
			
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

	## connect to KeyValueStore
	def setKV(self, key, value):
		self.kvs.setKeyValue(key, value)
		print "socket is ,,, ", self.socket

	def getV(self, key):
		value = self.kvs.get(key)
		print "val ==== ", value
		return value

	## input to sublime from server
	def controlSublime(self):
		print "will control sublime"

## key-value pool
class KVS:
	## set
	def setKeyValue(self, key, value):
		print "key_", key, ":value_", value

	## get
	def get(self, key):
		print "key_", key
		return ""















