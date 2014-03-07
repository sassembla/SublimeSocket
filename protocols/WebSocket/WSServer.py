# -*- coding: utf-8 -*-

import os
import socket
import string
import threading
import uuid

from .WSClient import WSClient
from .WSEncoder import WSEncoder

import PythonSwitch
import SublimeSocketAPISettings


class WSServer:
	def __init__(self, server):
		self.methodName = SublimeSocketAPISettings.WEBSOCKET_SERVER
		self.clientIds = {}
		
		self.args = None

		
		self.socket = ''
		self.host = ''
		self.port = ''

		self.listening = False
		
		self.encoder = WSEncoder()

		self.sublimeSocketServer = server

	def info(self):
		message = "SublimeSocket WebSocketServing running @ " + str(self.host) + ':' + str(self.port)
		
		for clientId in self.clientIds:
			message = message + "\n	client:" + clientId
		return message
		

	def currentArgs(self):
		return (self.methodName, self.args)


	def setup(self, params):
		assert "host" in params and "port" in params, "WebSocketServer require 'host' and 'port' param."
		
		# set for restart.
		self.args = params

		self.host = params["host"]
		self.port = params["port"]


	def spinup(self):
		assert self.host and self.port, "WebSocketServer require set 'host' and 'port' param."
		self.socket = socket.socket()

		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		try:
			self.socket.bind((self.host, self.port))
		except socket.error as msg:
			reason = 'SublimeSocket WebSocketServing faild to spinup @ ' + str(self.host) + ':' + str(self.port) + " by " + str(msg)
			self.sublimeSocketServer.transferSpinupFailed(reason)
			return

		self.socket.listen(1)
		self.sublimeSocketServer.transferSpinupped('SublimeSocket WebSocketServing started @ ' + str(self.host) + ':' + str(self.port))


		self.listening = True
		while self.listening:
			try:
				# when teardown, causes close then "Software caused connection abort"
				(conn, addr) = self.socket.accept()

				identity = str(uuid.uuid4())

				# genereate new client
				client = WSClient(self, identity)
				
				self.clientIds[identity] = client

				threading.Thread(target = client.handle, args = (conn,addr)).start()
			except socket.error as msg:
				errorMsg = "SublimeSocket WebSocketServing crashed @ " + str(self.host) + ":" + str(self.port) + " reason:" + str(msg)
				self.sublimeSocketServer.transferNoticed(errorMsg)
			
		message = "SublimeSocket WebSocketServing closed @ " + str(self.host) + ":" + str(self.port)
		self.sublimeSocketServer.transferTeardowned(message)		

	## teardown the server
	def teardown(self):
		# close all WebSocket clients
		clientsList = self.clientIds.copy()
		
		for clientId in clientsList:
			client = self.clientIds[clientId]
			client.close()

		self.clientIds = []

		# stop receiving
		self.listening = False

		# force close. may cause "[Errno 53] Software caused connection abort".
		self.socket.close()



	## update specific client's id
	def updateClientId(self, clientId, newIdentity):
		client = self.clientIds[clientId]

		# del from list
		del self.clientIds[clientId]

		# update
		client.clientId = newIdentity
		self.clientIds[newIdentity] = client


	def thisClientIsDead(self, clientId):
		self.closeClient(clientId)
		

	# remove from Client dict
	def closeClient(self, clientId):
		client = self.clientIds[clientId]
		client.close()

		if clientId in self.clientIds:
			del self.clientIds[clientId]
	

	# call SublimeSocket server. transfering datas.
	def call(self, data, clientId):
		self.sublimeSocketServer.transferInputted(data, clientId)


	def sendMessage(self, targetId, message):
		if message:
			pass
		else:
			return (False, "no data to:"+targetId)
			
		if targetId in self.clientIds:
			client = self.clientIds[targetId]
			buf = self.encoder.text(message, mask=0)
			client.send(buf)
			return (True, "done")
			
		return (False, "no target found in:" + str(self.clientIds))


	def broadcastMessage(self, targetIds, message):
		buf = self.encoder.text(str(message), mask=0)
		
		clients = self.clientIds.values()

		targets = []

		# broadcast to specific clients.
		if targetIds:
			idAndClient = [(client.clientId, client) for client in clients]
			for targetId in targetIds:
				for clientId, client in idAndClient:
					if targetId == clientId:
						client.send(buf)
						targets.append(clientId)

		# broadcast
		else:
			for client in clients:
				client.send(buf)

				targets.append(client.clientId)

		return targets

		
