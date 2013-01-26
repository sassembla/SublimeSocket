# -*- coding: utf-8 -*-
import socket, threading, string, time
from SublimeWSClient import *

class SublimeWSServer:

	def __init__(self):
		self.clients = []
		self.s = ''
		self.listening = False

	def start(self, host, port):
		self.s = socket.socket()
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind((host,port))
		
		self.s.listen(1)
		
		print 'WebSocketServing ready @ ', host, ':', port

		self.listening = True
		while self.listening:
			(conn, addr) = self.s.accept()
			
			_client = SublimeWSClient(self)
			self.clients.append(_client)

			print 'Total Clients:', str(len(self.clients))
			
			threading.Thread(target = _client.handle, args = (conn,addr)).start()

	## Send a multicast frame
	# def send(self, bytes):
	# 	print '-- SEND MULTICAST ---', repr(bytes)
	# 	for _client in self.clients:
	# 		_client.send(bytes)
		

	## Stop all WSClients
	# def stop(self):
	# 	self.listening = False
	# 	while (len(self.clients)):
	# 		self.clients.pop()._SublimeWSController.kill()
	# 	self.s.close()
	# 	print '--- THAT''S ALL FOLKS ! ---'

	## Remove the client from clients list
	def remove(self, client):
		if client in self.clients:
			print 'client left:', repr(client.conn)
			self.clients.remove(client)














