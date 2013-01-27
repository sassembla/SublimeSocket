# -*- coding: utf-8 -*-
import SublimeWSSettings
import json

import difflib
from SublimeWSEncoder import *

#API for Input to ST2 through WebSocket
API_DEFINE_DELIM = "@"
API_PREFIX = "sublimesocket"

API_INPUTIDENTITY = "inputIdentity"
API_KILLSERVER    = "killServer"


## API Parse the action
class SublimeSocketAPI:
	def __init__(self, server, sublime):
		self.server = server
		self.sublime = sublime
		self.encoder = SublimeWSEncoder()

	def parse(self, data, client):
		commands = data.split('>')

    # command and param  e.g		inputIdentity:{"id":"537d5da6-ce7d-42f0-387b-d9c606465dbb"}

		for commandIdentityAndParams in commands :
			command_params = commandIdentityAndParams.split(':', 1)
			command = command_params[0]

			params = ''
			if 1 < len(command_params):
				params = json.loads(command_params[1])

      # ネストとかする前提で、順にパースする
      # python-switch
			for case in switch(command):
				if case(API_INPUTIDENTITY):
					# callback to client as kill-id of myself
					clientId = params["id"]

					self.server.setKV("clientId", str(clientId))
					break

				if case(API_KILLSERVER):
					client.close()
					self.server.killServerSelf()
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
	