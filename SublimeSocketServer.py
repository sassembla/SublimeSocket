# -*- coding: utf-8 -*-

import uuid
import re
import time

from SublimeSocketAPI import SublimeSocketAPI
import SublimeSocketAPISettings

from KVS import KVS

# choose transfer method.
from protocols.WebSocket.WSServer import WSServer
from PythonSwitch import PythonSwitch


class SublimeSocketServer:
	def __init__(self):
		self.api = SublimeSocketAPI(self)
		self.kvs = KVS()

		self.transfer = None
		self.reserveRestart = None

		self.onConnectedTriggers = []

	# control server self.

	def resetServer(self):
		self.refreshKVS()
		self.teardownTransfer()

	def teardownServer(self):
		self.resetServer()
		# teardowned will call.
	
	def refreshKVS(self):
		self.clearAllKeysAndValues()

	def transferTeardowned(self, message):
		self.api.editorAPI.printMessage(message + "\n")
		self.api.editorAPI.statusMessage(message)

		self.transfer = None

		# run when restert reserved.
		if self.reserveRestart:
			self.setupTransfer(*self.reserveRestart)

			self.spinupTransfer()
			self.reserveRestart = None

	
	def transferNoticed(self, message):
		self.api.editorAPI.printMessage(message)

	def transferSpinupFailed(self, message):
		self.api.editorAPI.printMessage(message)
		self.api.editorAPI.statusMessage(message)

	def transferSpinupped(self, message):
		self.api.editorAPI.printMessage(message)
		self.api.editorAPI.statusMessage(message)

		# react to renew
		self.onTransferRenew()

	def transferConnected(self, clientId):
		if self.onConnectedTriggers:
			for funcDict in self.onConnectedTriggers:
				for _, func in funcDict.items():
					func()
		self.onConnectedTriggers = []


	# main API data incoming method.
	def transferInputted(self, data, clientId):
		apiData = data.split(SublimeSocketAPISettings.SSAPI_DEFINE_DELIM, 1)[1]
		self.api.parse(apiData, clientId)
		

	def showTransferInfo(self):
		if self.transfer:
			return self.transfer.info()

		else:
			return "no transfer running."



	# control transfer.

	def setupTransfer(self, transferMethod, params):
		if self.transfer:
			message = "SublimeSocket already running." + self.transfer.info()
			self.api.editorAPI.printMessage(message + "\n")
			self.api.editorAPI.statusMessage(message)
		
		else:
			if transferMethod in SublimeSocketAPISettings.TRANSFER_METHODS:
				
				for case in PythonSwitch(transferMethod):
					if case(SublimeSocketAPISettings.WEBSOCKET_SERVER):
						self.transfer = WSServer(self)
						self.transfer.setup(params)
						break


		self.currentTransferMethod = transferMethod

	def spinupTransfer(self):
		if self.transfer:
			self.transfer.spinup()

	def restartTransfer(self):
		if self.transfer:
			# reserve restart
			self.reserveRestart = self.transfer.currentArgs()
			self.teardownTransfer()
		else:
			self.transferSpinupFailed("no transfer running.")

	def teardownTransfer(self):
		if self.transfer:
			self.transfer.teardown()
		else:
			self.transferTeardowned("no transfer running.")

	def appendOnConnectedTriggers(self, func):
		for addedFunctionDict in self.onConnectedTriggers:
			if func.__name__ in addedFunctionDict.keys():
				print("duplicate trigger:"+str(func))
				return
			
		self.onConnectedTriggers.append({func.__name__:func})

	# message series
	
	def sendMessage(self, targetId, message):
		return self.transfer.sendMessage(targetId, message)

	def broadcastMessage(self, targetIds, message):
		return self.transfer.broadcastMessage(targetIds, message)



	# other series

	def onTransferRenew(self):
		settingCommands = self.api.editorAPI.loadSettings("onTransferRenew")
		for command in settingCommands:
			self.api.runAPI(command, None)






	# KVS bridge series

	def clearAllKeysAndValues(self):
		self.kvs.clear()


	def showAllKeysAndValues(self):
		everything = self.kvs.getAll()
		print("everything", everything)


	# views and KVS
	def viewsDict(self):
		viewsDict = self.kvs.get(SublimeSocketAPISettings.DICT_VIEWS)

		if viewsDict:
			return viewsDict
		
		return {}

	def updateViewsDict(self, viewsDict):
		self.kvs.setKeyValue(SublimeSocketAPISettings.DICT_VIEWS, viewsDict)



	# regions and KVS
	def storeRegion(self, path, identity, line, regionFrom, regionTo, message):
		regionsDict = self.regionsDict()
		
		if path in regionsDict:
			if identity in regionsDict[path]:
				pass
			else:
				regionsDict[path][identity] = {}
				regionsDict[path][identity][SublimeSocketAPISettings.REGION_LINE] = line
				regionsDict[path][identity][SublimeSocketAPISettings.REGION_FROM] = regionFrom
				regionsDict[path][identity][SublimeSocketAPISettings.REGION_TO] = regionTo
				regionsDict[path][identity][SublimeSocketAPISettings.REGION_MESSAGES] = []
		else:
			regionsDict[path] = {}
			regionsDict[path][identity] = {}
			regionsDict[path][identity][SublimeSocketAPISettings.REGION_LINE] = line
			regionsDict[path][identity][SublimeSocketAPISettings.REGION_FROM] = regionFrom
			regionsDict[path][identity][SublimeSocketAPISettings.REGION_TO] = regionTo
			regionsDict[path][identity][SublimeSocketAPISettings.REGION_MESSAGES] = []

		if not message in regionsDict[path][identity][SublimeSocketAPISettings.REGION_MESSAGES]:
			regionsDict[path][identity][SublimeSocketAPISettings.REGION_MESSAGES].insert(0, message)
		
			self.updateRegionsDict(regionsDict)

	def regionsDict(self):
		regionsDict = self.kvs.get(SublimeSocketAPISettings.DICT_REGIONS)

		if regionsDict:
			return regionsDict

		return {}

	def updateRegionsDict(self, regionsDict):
		self.kvs.setKeyValue(SublimeSocketAPISettings.DICT_REGIONS, regionsDict)

	def selectingRegionIds(self, path):
		regionsDict = self.kvs.get(SublimeSocketAPISettings.DICT_REGIONS)
		
		if path in regionsDict:
			selectingRegionIds = [regionId for regionId, regionDatas in regionsDict[path].items() if SublimeSocketAPISettings.REGION_ISSELECTING in regionDatas and regionDatas[SublimeSocketAPISettings.REGION_ISSELECTING] == 1]
			
			return selectingRegionIds

		return []

	def updateSelectingRegionIdsAndResetOthers(self, path, selectingRegionIds):
		regionsDict = self.kvs.get(SublimeSocketAPISettings.DICT_REGIONS)
		
		if path in regionsDict:
			regions = regionsDict[path]
			allRegionIds = list(regions)
			
			unselectedRegionIds = set(allRegionIds) - set(selectingRegionIds)

			for selectingRegionId in selectingRegionIds:
				regions[selectingRegionId][SublimeSocketAPISettings.REGION_ISSELECTING] = 1
			
			for unselectdRegionid in unselectedRegionIds:
				regions[unselectdRegionid][SublimeSocketAPISettings.REGION_ISSELECTING] = 0

	# reactor and KVS
	def reactorsDict(self):
		reactorsDict = self.kvs.get(SublimeSocketAPISettings.DICT_REACTORS)
		if reactorsDict:
			return reactorsDict

		return {}

	def updateReactorsDict(self, reactorsDict):
		self.kvs.setKeyValue(SublimeSocketAPISettings.DICT_REACTORS, reactorsDict)




	# reactorsLog and KVS
	def reactorsLogDict(self):
		reactorsLogDict = self.kvs.get(SublimeSocketAPISettings.DICT_REACTORSLOG)

		if reactorsLogDict:
			return reactorsLogDict

		return {}

	def updateReactorsLogDict(self, reactorsLogDict):
		self.kvs.setKeyValue(SublimeSocketAPISettings.DICT_REACTORSLOG, reactorsLogDict)




	# completions and KVS
	def completionsDict(self):
		completionsDict = self.kvs.get(SublimeSocketAPISettings.DICT_COMPLETIONS)
		if completionsDict:
			return completionsDict

		return {}

	def deleteCompletion(self, identity):
		completionsDict = self.kvs.get(SublimeSocketAPISettings.DICT_COMPLETIONS)
		del completionsDict[identity]
		self.updateCompletionsDict(completionsDict)

	def updateCompletionsDict(self, completionsDict):
		self.kvs.setKeyValue(SublimeSocketAPISettings.DICT_COMPLETIONS, completionsDict)



	# filters and KVS
	def filtersDict(self):
		filtersDict = self.kvs.get(SublimeSocketAPISettings.DICT_FILTERS)

		if filtersDict:
			return filtersDict

		return {}

	def updateFiltersDict(self, filtersDict):
		self.kvs.setKeyValue(SublimeSocketAPISettings.DICT_FILTERS, filtersDict)
	
