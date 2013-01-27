# -*- coding: utf-8 -*-
import SublimeWSSettings
import json

import difflib
from SublimeWSEncoder import *


## API Parse the action
class SublimeSocketAPI:
	def __init__(self, server, sublime):
		self.server = server
		self.sublime = sublime
		self.encoder = SublimeWSEncoder()

	def parse(self, data, client):
		commands = data.split('/')

		firstCommand = commands[0]# e.g		inputIdentity:{"id":"537d5da6-ce7d-42f0-387b-d9c606465dbb"}
		commandIdentityAndParams = firstCommand.split(':', 1)

		command = commandIdentityAndParams[0]
		params = json.loads(commandIdentityAndParams[1])

		if (command == SublimeWSSettings.API_INPUTIDENTITY):
			print "match,,,"
		else:
			s = difflib.SequenceMatcher(a=command, b=SublimeWSSettings.API_INPUTIDENTITY)
			for block in s.get_matching_blocks():
				print "match at a[%d] and b[%d] of length %d" % block
			
		# python-switch
		for case in switch(command):
			
			if case(SublimeWSSettings.API_INPUTIDENTITY):
				# callback to client as kill-id of myself
				clientId = params["id"]

				self.server.setKV("clientId", str(clientId))
				
				# bytes = self.encoder.text(str(self.clientId), mask=0)
				# client.send(bytes)

				break

			if case("kill"):
				# client.serverをなんとかすれば終了できる！！

				break
			if case():
				print "unknown command"
				break







class switch(object):
	def __init__(self, value):
		self.value = value
		self.fall = False

	def __iter__(self):
		"""Return the match method once, then stop"""
		yield self.match
		raise StopIteration

	def match(self, *args):
		"""Indicate whether or not to enter a case suite"""
		if self.fall or not args:
			return True
		elif self.value in args: # changed for v1.5, see below
			self.fall = True
			return True
		else:
			return False
	