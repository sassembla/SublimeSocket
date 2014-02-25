# -*- coding: utf-8 -*-

import json
import subprocess
import threading
import shlex
import os
import time
import re
import uuid
import sys
import io
import copy

from functools import reduce
from PythonSwitch import PythonSwitch

# choice editorApi by platform.
from editorAPIs.SublimeText.EditorAPI import EditorAPI

import SublimeSocketAPISettings

from parserImpl import SushiJSON
from parserImpl.SushiJSON import SushiJSONParser
from parserImpl.SushiJSON import SushiJSONTestParser

## API Parse the action
class SublimeSocketAPI:
	def __init__(self, server):
		self.server = server

		self.editorAPI = EditorAPI()
		self.globalResults = []

		self.asyncDict = {}
		self.counts = {}

		self.setSublimeSocketWindowBasePath({})


	## initialize results as the part of globalResults.
	def addResultContext(self, resultIdentity):
		self.globalResults[resultIdentity] = []

	def setResultsParams(self, contextKey, apiFunc, value):
		if self.globalResults and contextKey in self.globalResults:
			self.globalResults[contextKey].append({apiFunc.__name__:value})
		
	def resultBody(self, contextIdentity):
		return self.globalResults[contextIdentity]

	def resultContextKeys(self, params):
		return list(self.globalResults)




	## Parse the API command
	def parse(self, data, clientId=None):
		runnable = SushiJSONParser.parseStraight(data)

		if runnable:
			for commandSource, paramsSource in runnable:
				command, params = SushiJSONParser.composeParams(commandSource, paramsSource, None)
				self.runAPI(command, params, clientId)
		

	## run the specified API with JSON parameters. Dict or Array of JSON.
	def runAPI(self, command, params, clientId=None):
			
  		# python-switch
		for case in PythonSwitch(command):
			if case(SublimeSocketAPISettings.API_CONNECTEDCALL):
				self.server.transferConnected(clientId)
				break

			if case(SushiJSON.SETTESTBEFOREAFTER_BEFORESELECTORS):
				SushiJSONParser.runSelectors(
					params,
					[],
					[],
					self.runAPI
				)
				break
				
			if case(SushiJSON.SETTESTBEFOREAFTER_AFTERSELECTORS):
				SushiJSONParser.runSelectors(
					params,
					[],
					[],
					self.runAPI
				)
				break

			if case(SublimeSocketAPISettings.API_CHANGEIDENTITY):
				self.changeIdentity(params, clientId)
				break

			if case(SublimeSocketAPISettings.API_ASSERTRESULT):
				self.assertResult(params)
				break

			if case(SublimeSocketAPISettings.API_AFTERASYNC):
				self.afterAsync(params)
				break

			if case(SublimeSocketAPISettings.API_WAIT):
				self.wait(params)
				break

			if case(SublimeSocketAPISettings.API_COUNTUP):
				self.countUp(params)
				break			

			if case(SublimeSocketAPISettings.API_RESETCOUNTS):
				self.resetCounts(params)
				break

			if case(SublimeSocketAPISettings.API_RUNSUSHIJSON):
				self.runSushiJSON(params)
				break

			if case(SublimeSocketAPISettings.API_TEARDOWN):
				self.server.tearDown()
				break

			if case(SublimeSocketAPISettings.API_CREATEBUFFER):
				self.createBuffer(params)
				break

			if case(SublimeSocketAPISettings.API_OPENFILE):
				self.openFile(params)
				break

			if case(SublimeSocketAPISettings.API_CLOSEFILE):
				self.closeFile(params)
				break

			if case(SublimeSocketAPISettings.API_CLOSEALLBUFFER):
				self.closeAllBuffer(params)
				break

			if case(SublimeSocketAPISettings.API_SELECTEDREGIONS):
				self.selectedRegions(params)
				break

			if case(SublimeSocketAPISettings.API_COLLECTVIEWS):
				self.collectViews(params)
				break
				
			if case(SublimeSocketAPISettings.API_DEFINEFILTER):
				self.defineFilter(params)
				break

			if case(SublimeSocketAPISettings.API_FILTERING):
				self.filtering(params)
				break

			if case(SublimeSocketAPISettings.API_SETEVENTREACTOR):
				self.setEventReactor(params)
				break
				
			if case(SublimeSocketAPISettings.API_SETVIEWREACTOR):
				self.setViewReactor(params)
				break

			if case(SublimeSocketAPISettings.API_RESETREACTORS):
				self.resetReactors(params)
				break

			if case(SublimeSocketAPISettings.API_VIEWEMIT):
				self.viewEmit(params)
				break

			if case(SublimeSocketAPISettings.API_MODIFYVIEW):
				self.modifyView(params)
				break

			if case(SublimeSocketAPISettings.API_SETSELECTION):
				self.setSelection(params)
				break

			if case(SublimeSocketAPISettings.API_CLEARSELECTION):
				self.clearSelection(params)
				break

			if case(SublimeSocketAPISettings.API_RUNSHELL):
				self.runShell(params)
				break

			if case(SublimeSocketAPISettings.API_BROADCASTMESSAGE):
				self.broadcastMessage(params)
				break

			if case(SublimeSocketAPISettings.API_MONOCASTMESSAGE):
				self.monocastMessage(params)
				break

			if case(SublimeSocketAPISettings.API_SHOWATLOG):
				self.showAtLog(params)
				break

			if case(SublimeSocketAPISettings.API_SHOWDIALOG):
				self.showDialog(params)
				break

			if case(SublimeSocketAPISettings.API_SHOWTOOLTIP):
				self.showToolTip(params)
				break

			if case(SublimeSocketAPISettings.API_SCROLLTO):
				self.scrollTo(params)
				break

			if case(SublimeSocketAPISettings.API_TRANSFORM):
				self.transform(params)
				break

			if case(SublimeSocketAPISettings.API_APPENDREGION):
				self.appendRegion(params)
				break

			if case(SublimeSocketAPISettings.API_NOTIFY):
				self.notify(params)
				break

			if case(SublimeSocketAPISettings.API_GETALLFILEPATH):
				self.getAllFilePath(params)
				break

			if case(SublimeSocketAPISettings.API_READFILE):
				self.readFile(params)
				break

			if case(SublimeSocketAPISettings.API_EVENTEMIT):
				self.eventEmit(params)
				break

			if case(SublimeSocketAPISettings.API_CANCELCOMPLETION):
				self.cancelCompletion(params)
				break

			if case(SublimeSocketAPISettings.API_RUNCOMPLETION):
				self.runCompletion(params)
				break

			if case(SublimeSocketAPISettings.API_FORCELYSAVE):
				self.forcelySave(params)
				break

			if case(SublimeSocketAPISettings.API_SETSUBLIMESOCKETWINDOWBASEPATH):
				self.setSublimeSocketWindowBasePath(params)
				break

			if case(SublimeSocketAPISettings.API_SHOWSTATUSMESSAGE):
				self.showStatusMessage(params)
				break

			if case(SublimeSocketAPISettings.API_ERASEALLREGIONS):
				self.eraseAllRegions(params)
				break

			if case (SublimeSocketAPISettings.API_VERSIONVERIFY):
				self.versionVerify(params, clientId)
				break

			if case():
				self.editorAPI.printMessage("unknown command "+ command + " /")
				break


	def runReactor(self, reactorType, params, eventParams):
		if SushiJSON.SUSHIJSON_KEYWORD_INJECTS in params:
			pass
		else:
			params[SushiJSON.SUSHIJSON_KEYWORD_INJECTS] = {}

		for case in PythonSwitch(reactorType):
			if case(SublimeSocketAPISettings.REACTORTYPE_EVENT):
				if SublimeSocketAPISettings.SETREACTOR_ACCEPTS in params:
					
					# forcely inject
					for key in params[SublimeSocketAPISettings.SETREACTOR_ACCEPTS]:
						# set key: key for generating injection map.
						if key in params[SushiJSON.SUSHIJSON_KEYWORD_INJECTS]:
							pass
						else:
							params[SushiJSON.SUSHIJSON_KEYWORD_INJECTS][key] = key
				
				break

			if case(SublimeSocketAPISettings.REACTORTYPE_VIEW):
				
				# forcely inject
				for key in SublimeSocketAPISettings.REACTOR_VIEWKEY_INJECTIONS:
					# set key: key for generating injection map.
					if key in params[SushiJSON.SUSHIJSON_KEYWORD_INJECTS]:
						pass
					else:
						params[SushiJSON.SUSHIJSON_KEYWORD_INJECTS][key] = key
				
				break


		keys = []
		values = []
		for key, val in eventParams.items():
			keys.append(key)
			values.append(val)

		SushiJSONParser.runSelectors(
			params, 
			keys, 
			values,
			self.runAPI
		)

		
	def runFoundationEvent(self, eventName, eventParam, reactors):
		for case in PythonSwitch(eventName):
			if case(SublimeSocketAPISettings.SS_FOUNDATION_NOVIEWFOUND):
				self.foundation_noViewFound(reactors, eventParam)
				break


	def foundation_noViewFound(self, reactDicts, eventParam):
		for target in list(reactDicts):
			params = reactDicts[target]	
			assert SublimeSocketAPISettings.NOVIEWFOUND_NAME in eventParam, "ss_f_noviewfound require 'name' param."
			assert SublimeSocketAPISettings.NOVIEWFOUND_MESSAGE in eventParam, "ss_f_noviewfound require 'message' param."

			name = eventParam[SublimeSocketAPISettings.NOVIEWFOUND_NAME]
			message = eventParam[SublimeSocketAPISettings.NOVIEWFOUND_MESSAGE]

			SushiJSONParser.runSelectors(
				params, 
				SublimeSocketAPISettings.NOVIEWFOUND_INJECTIONS, 
				[name, message],
				self.runAPI
			)


	def afterAsync(self, params):
		assert SublimeSocketAPISettings.AFTERASYNC_IDENTITY in params, "afterAsync require 'identity' param."
		assert SublimeSocketAPISettings.AFTERASYNC_MS in params, "afterAsync require 'ms' param."

		assert SushiJSON.SUSHIJSON_KEYWORD_SELECTORS in params, "afterAsync require 'selectors' param."

		currentParams = params
		identity = params[SublimeSocketAPISettings.AFTERASYNC_IDENTITY]
		ms = params[SublimeSocketAPISettings.AFTERASYNC_MS]
		
		msNum = int(ms)

		def afterWait(asyncedIdentity, runtimeIdentity):
			if identity != asyncedIdentity:
				return

			if identity in self.asyncDict:
				if runtimeIdentity == self.asyncDict[identity]["runtimeIdentity"]:
					SushiJSONParser.runSelectors(
						currentParams, 
						currentParams.keys(),
						currentParams.values(),
						self.runAPI
					)

				else:
					self.editorAPI.printMessage("updated by new same-identity afterAsync:"+identity)

		runtimeIdentity = str(uuid.uuid4())
		self.asyncDict[identity] = {"runtimeIdentity":runtimeIdentity}

		threading.Timer(msNum*0.001, afterWait, [identity, runtimeIdentity]).start()


	def wait(self, params):
		assert SublimeSocketAPISettings.WAIT_MS in params, "wait require 'ms' param."

		waitMS = params[SublimeSocketAPISettings.WAIT_MS]
		waitMSNum = int(waitMS)

		time.sleep(waitMSNum*0.001)


	## count up specified labelled param.
	def countUp(self, params):
		assert SublimeSocketAPISettings.COUNTUP_LABEL in params, "countUp requre 'label' param."
		assert SublimeSocketAPISettings.COUNTUP_DEFAULT in params, "countUp requre 'default' param."

		label = params[SublimeSocketAPISettings.COUNTUP_LABEL]

		if label in self.counts:
			self.counts[label] = self.counts[label] + 1

		else:
			self.counts[label] = params[SublimeSocketAPISettings.COUNTUP_DEFAULT]

		count = self.counts[label]

		SushiJSONParser.runSelectors(
			params, 
			SublimeSocketAPISettings.COUNTUP_INJECTIONS,
			[label, count],
			self.runAPI
		)

		


	def resetCounts(self, params):
		resetted = []
		if SublimeSocketAPISettings.RESETCOUNTS_LABEL in params:
			target = params[SublimeSocketAPISettings.RESETCOUNTS_LABEL]
			if target in self.counts:
				del self.counts[target]
				resetted.append(target)
		else:
			resetted = list(self.counts)
			self.counts = {}

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.RESETCOUNTS_INJECTIONS,
			[resetted],
			self.runAPI
		)

		
	## run specific setting.txt file or data on API.
	def runSushiJSON(self, params):
		assert SublimeSocketAPISettings.RUNSUSHIJSON_PATH in params or SublimeSocketAPISettings.RUNSUSHIJSON_DATA in params, "runSushiJSON require 'path' or 'data' params."
		
		if SublimeSocketAPISettings.RUNSUSHIJSON_PATH in params:
			filePath = params[SublimeSocketAPISettings.RUNSUSHIJSON_PATH]

			# check contains PREFIX or not
			replacedFilePath = self.getKeywordBasedPath(filePath, 
				SublimeSocketAPISettings.RUNSUSHIJSON_PREFIX_SUBLIMESOCKET_PATH,
				self.editorAPI.packagePath()+ "/"+SublimeSocketAPISettings.MY_PLUGIN_PATHNAME+"/")

			self.editorAPI.printMessage("runSetting:" + replacedFilePath)
			
			with open(replacedFilePath, encoding='utf8') as f:
				setting = f.read()
			
			# remove //comment line
			removeCommented_setting = re.sub(r'//.*', r'', setting)
			
			# remove spaces
			removeSpaces_setting = re.sub(r'(?m)^\s+', '', removeCommented_setting)
			
			# remove CRLF
			removeCRLF_setting = removeSpaces_setting.replace("\n", "")
			
			data = removeCRLF_setting

		elif SublimeSocketAPISettings.RUNSUSHIJSON_DATA in params:
			data = params[SublimeSocketAPISettings.RUNSUSHIJSON_DATA]


		contextIdentity = str(self.runSushiJSON.__name__) + ":" + str(uuid.uuid4())
		# add context
		self.addResultContext(contextIdentity)

		def run(currentCommand, currentParams):
			self.runAPI(currentCommand, currentParams)

		[run(currentCommand, currentParams) for currentCommand, currentParams in SushiJSONParser.parseSushiJSON(data)]


		logsSource = self.resultBody(contextIdentity)

		# drip "showAtLog" result only.
		logs = [logKeyAndBody[self.showAtLog.__name__]["output"] for logKeyAndBody in logsSource if self.showAtLog.__name__ in logKeyAndBody]
		
		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.RUNSUSHIJSON_INJECTIONS,
			[logs],
			self.runAPI
		)


	## run shellScript
	# params is array that will be evaluated as commandline parameters.
	def runShell(self, params):
		assert SublimeSocketAPISettings.RUNSHELL_MAIN in params, "runShell require 'main' param."

		if SublimeSocketAPISettings.RUNSHELL_DELAY in params:
			delay = params[SublimeSocketAPISettings.RUNSHELL_DELAY]
			del params[SublimeSocketAPISettings.RUNSHELL_DELAY]
			
			if type(delay) is str:
				delay = int(delay)
				
			self.editorAPI.runAfterDelay(self.runShell(params), delay)
			return

		main = params[SublimeSocketAPISettings.RUNSHELL_MAIN]
		
		def genKeyValuePair(key):
			val = ""


			def replaceValParts(val):
				val = val.replace(" ", SublimeSocketAPISettings.RUNSHELL_REPLACE_SPACE);
				val = val.replace("(", SublimeSocketAPISettings.RUNSHELL_REPLACE_RIGHTBRACE);
				val = val.replace(")", SublimeSocketAPISettings.RUNSHELL_REPLACE_LEFTBRACE);
				val = val.replace("'", SublimeSocketAPISettings.RUNSHELL_REPLACE_SINGLEQUOTE);
				val = val.replace("`", SublimeSocketAPISettings.RUNSHELL_REPLACE_SINGLEQUOTE);
				val = val.replace("@s@s@", SublimeSocketAPISettings.RUNSHELL_REPLACE_At_s_At_s_At);


				# check contains PREFIX or not
				val = self.getKeywordBasedPath(val, 
					SublimeSocketAPISettings.RUNSUSHIJSON_PREFIX_SUBLIMESOCKET_PATH,
					self.editorAPI.packagePath() + "/"+SublimeSocketAPISettings.MY_PLUGIN_PATHNAME+"/")

				if " " in val:
					val = "\"" + val + "\""
					
				return val

			if type(params[key]) == list:

				replaced = [replaceValParts(v) for v in params[key]]
				val = ' '.join(replaced)
			else:
				val = replaceValParts(str(params[key]))


			if len(val) is 0:
				return key

			if len(key) is 0:
				return val

			return key + ' ' + val

		kvPairArray = [genKeyValuePair(key) for key in params.keys() if key not in SublimeSocketAPISettings.RUNSHELL_LIST_IGNORES]
		kvPairArray.insert(0, main) 

		runnable = ' '.join(kvPairArray)
		debugFlag = False

		if SublimeSocketAPISettings.RUNSHELL_DEBUG in params:
			debugFlag = params[SublimeSocketAPISettings.RUNSHELL_DEBUG]

		if debugFlag:
			self.showAtLog({"message":runnable})
		
		if len(runnable):
			subprocess.call(runnable, shell=True)
			
			

	## emit message to all clients.
	def broadcastMessage(self, params):
		if SublimeSocketAPISettings.BROADCASTMESSAGE_FORMAT in params:
			currentParams = self.formattingMessageParameters(params, SublimeSocketAPISettings.BROADCASTMESSAGE_FORMAT, SublimeSocketAPISettings.BROADCASTMESSAGE_MESSAGE)
			self.broadcastMessage(currentParams)
			return

		assert SublimeSocketAPISettings.BROADCASTMESSAGE_MESSAGE in params, "broadcastMessage require 'message' param."
		
		message = params[SublimeSocketAPISettings.BROADCASTMESSAGE_MESSAGE]

		sendedTargetIds = []

		if SublimeSocketAPISettings.BROADCASTMESSAGE_TARGETS in params:
			sendedTargetIds = self.server.broadcastMessage(params[SublimeSocketAPISettings.BROADCASTMESSAGE_TARGETS], message)
		else:
			sendedTargetIds = self.server.broadcastMessage([], message)
		
		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.BROADCASTMESSAGE_INJECTIONS,
			[sendedTargetIds, message],
			self.runAPI
		)
		
	

	## send message to the specific client.
	def monocastMessage(self, params):
		if SublimeSocketAPISettings.MONOCASTMESSAGE_FORMAT in params:
			currentParams = self.formattingMessageParameters(params, SublimeSocketAPISettings.MONOCASTMESSAGE_FORMAT, SublimeSocketAPISettings.MONOCASTMESSAGE_MESSAGE)
			self.monocastMessage(currentParams)
			return

		assert SublimeSocketAPISettings.MONOCASTMESSAGE_TARGET in params, "monocastMessage require 'target' param."
		assert SublimeSocketAPISettings.MONOCASTMESSAGE_MESSAGE in params, "monocastMessage require 'message' param."
		
		target = params[SublimeSocketAPISettings.MONOCASTMESSAGE_TARGET]
		message = params[SublimeSocketAPISettings.MONOCASTMESSAGE_MESSAGE]
		
		succeeded, reason = self.server.sendMessage(target, message)

		if succeeded:
			SushiJSONParser.runSelectors(
				params,
				SublimeSocketAPISettings.MONOCASTMESSAGE_INJECTIONS,
				[target, message],
				self.runAPI
			)

		else:
			self.editorAPI.printMessage("monocastMessage failed. target: " + target + " " + reason)
			
	
	def showAtLog(self, params):
		if SublimeSocketAPISettings.LOG_FORMAT in params:
			currentParams = self.formattingMessageParameters(params, SublimeSocketAPISettings.LOG_FORMAT, SublimeSocketAPISettings.LOG_MESSAGE)
			self.showAtLog(currentParams)
			return

		assert SublimeSocketAPISettings.LOG_MESSAGE in params, "showAtLog require 'message' param."
		message = params[SublimeSocketAPISettings.LOG_MESSAGE]
		self.editorAPI.printMessage(message)

		# write message to all contexts.
		contextKeys = self.resultContextKeys(params)
		for contextKey in contextKeys:
			self.setResultsParams(contextKey, self.showAtLog, {"output":message})


	def showDialog(self, params):
		if SublimeSocketAPISettings.SHOWDIALOG_FORMAT in params:
			currentParams = self.formattingMessageParameters(params, SublimeSocketAPISettings.SHOWDIALOG_FORMAT, SublimeSocketAPISettings.SHOWDIALOG_MESSAGE)
			self.showDialog(currentParams)
			return

		assert SublimeSocketAPISettings.SHOWDIALOG_MESSAGE in params, "showDialog require 'message' param."
		message = params[SublimeSocketAPISettings.LOG_MESSAGE]

		self.editorAPI.showMessageDialog(message)

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.SHOWDIALOG_INJECTIONS,
			[message],
			self.runAPI
		)


	def showToolTip(self, params):
		assert SublimeSocketAPISettings.SHOWTOOLTIP_ONSELECTED in params, "showToolTip require 'onselected' params."
		selects = params[SublimeSocketAPISettings.SHOWTOOLTIP_ONSELECTED]

		if selects:
			pass
		else:
			return

		assert SublimeSocketAPISettings.SHOWTOOLTIP_ONCANCELLED in params, "showToolTip require 'oncancelled' param."
		cancelled = params[SublimeSocketAPISettings.SHOWTOOLTIP_ONCANCELLED]
		
		finallyBlock = []
		if SublimeSocketAPISettings.SHOWTOOLTIP_FINALLY in params:
			finallyBlock = params[SublimeSocketAPISettings.SHOWTOOLTIP_FINALLY]


		(view, path, name) = self.internal_getViewAndPathFromViewOrName(params, SublimeSocketAPISettings.SHOWTOOLTIP_VIEW, SublimeSocketAPISettings.SHOWTOOLTIP_NAME)
		if view == None:
			return

		def getItemKey(item):
			itemList = list(item)
			assert len(itemList) == 1, "multiple items found in one items. not valid. at:"+str(item)
			key = itemList[0]
			return key

		tooltipTitles = [getItemKey(item) for item in selects]

		selectedTitle = "not yet"

		# run after the tooltip selected or cancelled.
		def toolTipClosed(index):
			selectedTitle = "cancelled"
			
			if -1 < index:
				if index < len(selects):
					selectedTitle = tooltipTitles[index]

					itemDict = selects[index]
					key = list(itemDict)[0]

					# rename from "onselected" to "selector".
					selectorInsideParams = params
					selectorInsideParams[SushiJSON.SUSHIJSON_KEYWORD_SELECTORS] = itemDict[key]
					
					SushiJSONParser.runSelectors(
						selectorInsideParams, 
						SublimeSocketAPISettings.SHOWTOOLTIP_INJECTIONS, 
						[path, name, tooltipTitles, selectedTitle],
						self.runAPI
					)
			else:
				# rename from "cancelled" to "selector".
				selectorInsideParams = params
				selectorInsideParams[SushiJSON.SUSHIJSON_KEYWORD_SELECTORS] = cancelled
				
				SushiJSONParser.runSelectors(
					selectorInsideParams, 
					SublimeSocketAPISettings.SHOWTOOLTIP_INJECTIONS, 
					[path, name, tooltipTitles, selectedTitle],
					self.runAPI
				)


			if finallyBlock:
				# rename from "finally" to "selector".
				selectorInsideParams = params
				selectorInsideParams[SushiJSON.SUSHIJSON_KEYWORD_SELECTORS] = finallyBlock

				SushiJSONParser.runSelectors(
					selectorInsideParams, 
					SublimeSocketAPISettings.SHOWTOOLTIP_INJECTIONS, 
					[path, name, tooltipTitles, selectedTitle],
					self.runAPI
				)
		
		# run before lock
		SushiJSONParser.runSelectors(
			params, 
			SublimeSocketAPISettings.SHOWTOOLTIP_INJECTIONS, 
			[path, name, tooltipTitles, selectedTitle],
			self.runAPI
		)

		self.editorAPI.showPopupMenu(view, tooltipTitles, toolTipClosed)


	def scrollTo(self, params):
		assert SublimeSocketAPISettings.SCROLLTO_LINE in params or SublimeSocketAPISettings.SCROLLTO_COUNT in params, "scrollTo require 'line' or 'count' params."
			
		if SublimeSocketAPISettings.SCROLLTO_LINE in params and SublimeSocketAPISettings.SCROLLTO_COUNT in params:
			del params[SublimeSocketAPISettings.SCROLLTO_COUNT]

		(view, _, _) = self.internal_getViewAndPathFromViewOrName(params, SublimeSocketAPISettings.SCROLLTO_VIEW, SublimeSocketAPISettings.SCROLLTO_NAME)
		if view == None:
			return

		if SublimeSocketAPISettings.SCROLLTO_LINE in params:
			line = int(params[SublimeSocketAPISettings.SCROLLTO_LINE])
			count = 0

		elif SublimeSocketAPISettings.SCROLLTO_COUNT in params:
			line = None
			count = int(params[SublimeSocketAPISettings.SCROLLTO_COUNT])
			

		self.editorAPI.scrollTo(view, line, count)
		
		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.SCROLLTO_INJECTIONS,
			[],
			self.runAPI
		)

		


	def transform(self, params):
		assert SushiJSON.SUSHIJSON_KEYWORD_SELECTORS in params, "transform require 'selectors' param."

		code = None

		if SublimeSocketAPISettings.TRANSFORM_PATH in params:
			transformerPath = params[SublimeSocketAPISettings.TRANSFORM_PATH]
			transformerName = self.getKeywordBasedPath(transformerPath, 
				SublimeSocketAPISettings.RUNSUSHIJSON_PREFIX_SUBLIMESOCKET_PATH,
				self.editorAPI.packagePath() + "/"+SublimeSocketAPISettings.MY_PLUGIN_PATHNAME+"/")

			assert os.path.exists(transformerName), "transformerpath not exist at:"+transformerName

			with open(transformerName, encoding='utf8') as f:
				code = compile(f.read(), transformerName, "exec")

		elif SublimeSocketAPISettings.TRANSFORM_CODE in params:
			transformerCode = params[SublimeSocketAPISettings.TRANSFORM_CODE]
			transformerName = "load transformer from api. not file."

			code = compile(transformerCode, "", "exec")

		else:
			assert False, "no resource found for transform. transform require 'transformerpath' or 'source' params."

		assert code, "no transformer generated. failed to generate from:"+transformerName

		debug = False
		if SublimeSocketAPISettings.TRANSFORM_DEBUG in params:
			debug = params[SublimeSocketAPISettings.TRANSFORM_DEBUG]
		
		if debug:
			print("transformer's path or code:"+transformerName)


		selectors = params[SushiJSON.SUSHIJSON_KEYWORD_SELECTORS]
		
		inputs = params.copy()
		
		start = str(uuid.uuid4())
		delim = str(uuid.uuid4())
		keyHeader = "key:"
		valHeader = "val:"
		
		result = []

		before = sys.stdout
		try:
			def output(self, paramDict):
				print(start)
				iterated = False
				for key, val in paramDict.items():
					if iterated:
						print(delim)

					print(keyHeader+key)

					# convert to JSON
					jsonVal = json.dumps(val)
				
					print(valHeader+jsonVal)

					iterated = True
			
			# set stdout
			sys.stdout = TransformerStream(result)
		
			# run transformer.py DSL.
			exec(code, {"inputs":params, "keys":list(params), "output":"output"}, None)

			
		except Exception as e:
			print("failed to run transform:"+str(e))
		finally:
			# reset stdout.
			sys.stdout = before

		if debug:
			print("unfixed result:"+str(result))
		
		def composeResultList(keyOrValueOrDelim):
			if keyOrValueOrDelim.startswith(keyHeader):
				key = keyOrValueOrDelim[len(keyHeader):]
				assert key, "no key found error in transform. output(parametersDict) key is None or something wrong."
				return key

			elif keyOrValueOrDelim.startswith(valHeader):
				jsonVal = keyOrValueOrDelim[len(valHeader):]
				assert jsonVal, "no value found error in transform. output(parametersDict) value is None or something wrong."

				# re-pack to value, list, dict.
				val = json.loads(jsonVal)
				return val

		
		naturalResultList = [s for s in result if s != "\n" and s != delim]
		
		if start in naturalResultList:
			pass
		else:
			assert False, "at:" + transformerName + " failed to get result. reason:"+str(naturalResultList)
		
		index = naturalResultList.index(start)+1 #next to start

		resultList = [composeResultList(s) for s in naturalResultList[index:]]
		resultParam = dict(zip(resultList[0::2], resultList[1::2]))

		if debug:
			print("resultParam:"+str(resultParam))
		

		keys = []
		values = []
		for key, val in resultParam.items():
			keys.append(key)
			values.append(val)

		SushiJSONParser.runSelectors(
			params, 
			keys, 
			values,
			self.runAPI
		)




	def runTests(self, params, clientId):
		assert SublimeSocketAPISettings.RUNTESTS_PATH in params, "runTests require 'path' param."

		def runInMainThread():

			filePath = params[SublimeSocketAPISettings.RUNTESTS_PATH]
			
			# check contains PREFIX of path or not
			filePath = self.getKeywordBasedPath(filePath, 
				SublimeSocketAPISettings.RUNSUSHIJSON_PREFIX_SUBLIMESOCKET_PATH,
				self.editorAPI.packagePath() + "/"+SublimeSocketAPISettings.MY_PLUGIN_PATHNAME+"/")
			
			data = ""
			with open(filePath) as f:
				data = f.read()

			
			# load test delimited scripts.
			testCases = SushiJSONTestParser.parseTestSuite(data)
			
			def countTestResult(assertResultBody):
				currentPassedCount = 0
				currentFailedCount = 0

				if SublimeSocketAPISettings.ASSERTRESULT_PASSEDORFAILED in assertResultBody:							
					if SublimeSocketAPISettings.ASSERTRESULT_VALUE_PASS in assertResultBody[SublimeSocketAPISettings.ASSERTRESULT_PASSEDORFAILED]:
						currentPassedCount = 1
						
					else:
						currentFailedCount = 1

				result = assertResultBody[SublimeSocketAPISettings.ASSERTRESULT_RESULT]
				self.server.broadcastMessage([], result)

				return (currentPassedCount, currentFailedCount)
			
			def runTestCase(testCase, counts):
				# reset globalResults
				self.globalResults = {}

				testSuitesIdentity = "test:"+str(uuid.uuid4())

				self.addResultContext(testSuitesIdentity)

				for testCommand, testParams in testCase:
					command, params = SushiJSONParser.composeParams(testCommand, testParams, None)

					self.runAPI(command, params, clientId)

				# reduce results
				for results in self.globalResults[testSuitesIdentity]:
					counted = [countTestResult(body) for apiName, body in results.items() if apiName == self.assertResult.__name__ and body]
					
					for passed, failed in counted:
						counts["passed"] = counts["passed"] + passed
						counts["failed"] = counts["failed"] + failed

			counts = {"passed":0, "failed": 0}
			[runTestCase(testCase, counts) for testCase in testCases]

			passedCount = counts["passed"]
			failedCount = counts["failed"]

			# count ASSERTRESULT_VALUE_PASS or ASSERTRESULT_VALUE_FAIL
			totalResultMessage = "TOTAL:" + str(passedCount + failedCount) + " passed:" + str(passedCount) + " failed:" + str(failedCount)
			self.server.broadcastMessage([], totalResultMessage)

		self.editorAPI.runAfterDelay(lambda: runInMainThread(), 0)

	## assertions
	def assertResult(self, params):
		currentResultContextKeys = self.resultContextKeys(params)

		currentResultContextKey = None
		
		for currentResultContextKeyCandidate in currentResultContextKeys:
			if currentResultContextKeyCandidate.startswith("test:"):
				currentResultContextKey = currentResultContextKeyCandidate

		assert currentResultContextKey, "failed to get test result context."
		
		assert SublimeSocketAPISettings.ASSERTRESULT_ID in params, "assertResult require 'id' param."
		assert SublimeSocketAPISettings.ASSERTRESULT_DESCRIPTION in params, "assertResult require 'description' param."
		
		identity = params[SublimeSocketAPISettings.ASSERTRESULT_ID]
		

		debug = False

		if SublimeSocketAPISettings.ASSERTRESULT_DEBUG in params:
			debug = params[SublimeSocketAPISettings.ASSERTRESULT_DEBUG]
		

			
		# load results for check
		resultBodies = self.resultBody(currentResultContextKey)
		if debug:
			self.editorAPI.printMessage("\nassertResult:\nid:" + identity + "\nresultBodies:" + str(resultBodies) + "\n:assertResult\n")


		assertionIdentity = params[SublimeSocketAPISettings.ASSERTRESULT_ID]
		message = params[SublimeSocketAPISettings.ASSERTRESULT_DESCRIPTION]
		
		

		def setAssertionResult(passedOrFailed, assertionIdentity, message):

			def assertionMessage(assertType, currentIdentity, currentMessage):
				return assertType + " " + currentIdentity + " : " + currentMessage

			resultMessage = assertionMessage(passedOrFailed,
								assertionIdentity, 
								message)
			
			self.setResultsParams(currentResultContextKey, self.assertResult, {SublimeSocketAPISettings.ASSERTRESULT_RESULT:resultMessage, SublimeSocketAPISettings.ASSERTRESULT_PASSEDORFAILED:passedOrFailed})			

		# contains
		if SublimeSocketAPISettings.ASSERTRESULT_CONTAINS in params:
			currentDict = params[SublimeSocketAPISettings.ASSERTRESULT_CONTAINS]
			if debug:
				self.editorAPI.printMessage("start assertResult 'contains' in " + identity + " " + str(resultBodies))

			# match
			for key in currentDict:
				for result in resultBodies:
					apiName = list(result)[0]
					resultBody = result[apiName]

					if apiName == key:
						assertValue = currentDict[key]
						assertTarget = resultBody
						if debug:
							self.editorAPI.printMessage("expected:" + str(assertValue) + "\n" + "actual:" + str(assertTarget) + "\n")

						
						if assertValue == assertTarget:
							setAssertionResult(SublimeSocketAPISettings.ASSERTRESULT_VALUE_PASS,
								assertionIdentity, 
								key + ":" + str(assertValue) + " in " + str(resultBody))
							return

			# fail
			if debug:
				self.editorAPI.printMessage("failed assertResult 'contains' in " + identity)

			setAssertionResult(SublimeSocketAPISettings.ASSERTRESULT_VALUE_FAIL,
				assertionIdentity, 
				message)
			return


		# not contains
		if SublimeSocketAPISettings.ASSERTRESULT_NOTCONTAINS in params:
			currentDict = params[SublimeSocketAPISettings.ASSERTRESULT_NOTCONTAINS]
			if debug:
				self.editorAPI.printMessage("start assertResult 'not contains' in " + identity + " " + str(resultBodies))

			# match
			for key in currentDict:
				for result in resultBodies:
					apiName = list(result)[0]
					resultBody = result[apiName]

					if apiName == key:
						assertValue = currentDict[key]
						assertTarget = resultBody
						
						if assertValue == assertTarget:
							if debug:
								self.editorAPI.printMessage("failed assertResult 'not contains' in " + identity)

							setAssertionResult(SublimeSocketAPISettings.ASSERTRESULT_VALUE_FAIL,
								assertionIdentity, 
								key + ":" + str(assertValue) + " in " + str(resultBody))
							return

			# pass
			setAssertionResult(SublimeSocketAPISettings.ASSERTRESULT_VALUE_PASS,
								assertionIdentity, 
								message)
			return


		# # is empty or not
		# elif SublimeSocketAPISettings.ASSERTRESULT_ISEMPTY in params:
		# 	if debug:
		# 		self.editorAPI.printMessage("start assertResult 'isempty' in " + identity + " " + str(resultBodies))

		# 	# match
		# 	if not resultBodies:
		# 		setAssertionResult(SublimeSocketAPISettings.ASSERTRESULT_VALUE_PASS,
		# 			assertionIdentity, 
		# 			"is empty.")
		# 		return

		# 	# fail
		# 	if debug:
		# 		self.editorAPI.printMessage("failed assertResult 'empty' in " + identity)

		# 	setAssertionResult(SublimeSocketAPISettings.ASSERTRESULT_VALUE_FAIL,
		# 		assertionIdentity, 
		# 		message)
		# 	return

			

		# is not empty or empty
		elif SublimeSocketAPISettings.ASSERTRESULT_ISNOTEMPTY in params:
			if debug:
				self.editorAPI.printMessage("start assertResult 'isnotempty' in " + identity + str(resultBodies))

			targetAPIKey = params[SublimeSocketAPISettings.ASSERTRESULT_ISNOTEMPTY]
			
			for result in resultBodies:
				apiName = list(result)[0]
				
				if apiName == targetAPIKey:
					setAssertionResult(SublimeSocketAPISettings.ASSERTRESULT_VALUE_PASS,
						assertionIdentity, 
						"is not empty.")
					return

			# fail
			if debug:
				self.editorAPI.printMessage("failed assertResult 'isnotempty' in " + identity)

			setAssertionResult(SublimeSocketAPISettings.ASSERTRESULT_VALUE_FAIL,
				assertionIdentity, 
				message)
			return
			
		if debug:
				self.editorAPI.printMessage("assertion aborted in assertResult API. " + message + " " + identity)

		setAssertionResult(SublimeSocketAPISettings.ASSERTRESULT_VALUE_FAIL,
			assertionIdentity,
			"assertion aborted in assertResult API.")
		return
		
	
	## change identity of client.
	def changeIdentity(self, params, currentClientIdentity):
		assert SublimeSocketAPISettings.CHANGEIDENTITY_TO in params, "updateClientId requre 'to' param"
		
		currentIdentityCandicate = currentClientIdentity

		if SublimeSocketAPISettings.CHANGEIDENTITY_FROM in params:
			currentIdentityCandicate = params[SublimeSocketAPISettings.CHANGEIDENTITY_FROM]

		newIdentity = params[SublimeSocketAPISettings.CHANGEIDENTITY_TO]

		self.server.transfer.updateClientId(currentIdentityCandicate, newIdentity)

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.CHANGEIDENTITY_INJECTIONS,
			[currentIdentityCandicate, newIdentity],
			self.runAPI
		)

		

	## create buffer then set contents if exist.
	def createBuffer(self, params):
		assert SublimeSocketAPISettings.CREATEBUFFER_NAME in params, "createBuffer require 'name' param"
		
		name = params[SublimeSocketAPISettings.CREATEBUFFER_NAME]

		if self.editorAPI.isBuffer(name):
			pass
		else:
			result = "failed to create buffer "+ name +" because of the file is already exists."
			
			return


		# renew event will run, but the view will not store KVS because of no-name view.
		view = self.editorAPI.openFile(name)

		# buffer generated then set name and store to KVS.
		message = "buffer "+ name +" created."
		status = message

		self.editorAPI.setNameToView(view, name)
		
		# restore to KVS with name
		viewParams = self.editorAPI.generateSublimeViewInfo(
			view,
			SublimeSocketAPISettings.VIEW_SELF,
			SublimeSocketAPISettings.VIEW_ID,
			SublimeSocketAPISettings.VIEW_BUFFERID,
			SublimeSocketAPISettings.VIEW_PATH,
			SublimeSocketAPISettings.VIEW_NAME,
			SublimeSocketAPISettings.VIEW_VNAME,
			SublimeSocketAPISettings.VIEW_SELECTEDS,
			SublimeSocketAPISettings.VIEW_ISEXIST
		)

		emitIdentity = str(uuid.uuid4())
		viewParams[SublimeSocketAPISettings.REACTOR_VIEWKEY_EMITIDENTITY] = emitIdentity

		self.fireReactor(
			SublimeSocketAPISettings.REACTORTYPE_VIEW,
			SublimeSocketAPISettings.SS_EVENT_RENAMED, 
			viewParams
		)

		# if "contents" exist, set contents to buffer.
		if SublimeSocketAPISettings.CREATEBUFFER_CONTENTS in params:
			contents = params[SublimeSocketAPISettings.CREATEBUFFER_CONTENTS]
			self.editorAPI.runCommandOnView('insert_text', {'string': contents})
		
		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.CREATEBUFFER_INJECTIONS,
			[name, status],
			self.runAPI
		)

		
		
	
	## open file
	def openFile(self, params):
		assert SublimeSocketAPISettings.OPENFILE_PATH in params, "openFile require 'path' key."
		original_path = params[SublimeSocketAPISettings.OPENFILE_PATH]
		path = original_path

		path = self.getKeywordBasedPath(path, 
			SublimeSocketAPISettings.RUNSUSHIJSON_PREFIX_SUBLIMESOCKET_PATH,
			self.editorAPI.packagePath() + "/"+SublimeSocketAPISettings.MY_PLUGIN_PATHNAME+"/")

		name = os.path.basename(path)

		if self.editorAPI.isBuffer(path):
			message = "file " + original_path + " is not exist."
			self.editorAPI.printMessage(message)

		else:
			view = self.editorAPI.openFile(path)
		
			message = "file " + original_path + " is opened."
			self.editorAPI.printMessage(message)
			
			viewParams = self.editorAPI.generateSublimeViewInfo(
							view,
							SublimeSocketAPISettings.VIEW_SELF,
							SublimeSocketAPISettings.VIEW_ID,
							SublimeSocketAPISettings.VIEW_BUFFERID,
							SublimeSocketAPISettings.VIEW_PATH,
							SublimeSocketAPISettings.VIEW_NAME,
							SublimeSocketAPISettings.VIEW_VNAME,
							SublimeSocketAPISettings.VIEW_SELECTEDS,
							SublimeSocketAPISettings.VIEW_ISEXIST
						)

			emitIdentity = str(uuid.uuid4())
			viewParams[SublimeSocketAPISettings.REACTOR_VIEWKEY_EMITIDENTITY] = emitIdentity

			self.fireReactor(
				SublimeSocketAPISettings.REACTORTYPE_VIEW,
				SublimeSocketAPISettings.SS_EVENT_LOADING, 
				viewParams
			)

			SushiJSONParser.runSelectors(
				params,
				SublimeSocketAPISettings.OPENFILE_INJECTIONS,
				[path, name],
				self.runAPI
			)

		
	
	## close file. if specified -> close the file. if not specified -> close current file.
	def closeFile(self, params):
		assert SublimeSocketAPISettings.CLOSEFILE_NAME in params, "closeFile require 'name' param."
		
		name = params[SublimeSocketAPISettings.CLOSEFILE_NAME]
		(view, name) = self.internal_detectViewInstance(name)
		
		path = self.internal_detectViewPath(view)

		self.editorAPI.closeView(view)
		
		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.CLOSEFILE_INJECTIONS,
			[path, name],
			self.runAPI
		)

	def closeAllBuffer(self, params):
		closeds = []

		def close(window):
			for view in self.editorAPI.viewsOfWindow(window):
				path = self.internal_detectViewPath(view)
				if self.editorAPI.isBuffer(path):
					closeds.append(path)

					self.editorAPI.closeView(view)

		[close(window) for window in self.editorAPI.windows()]

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.CLOSEALLBUFFER_INJECTIONS,
			[closeds],
			self.runAPI
		)

		

	# run selected regions.
	def selectedRegions(self, params):
		assert SublimeSocketAPISettings.SELECTEDREGIONS_SELECTEDS in params, "selectedRegions require 'selecteds' param."
		
		(view, path, name) = self.internal_getViewAndPathFromViewOrName(params, SublimeSocketAPISettings.SELECTEDREGIONS_VIEW, SublimeSocketAPISettings.SELECTEDREGIONS_NAME)
		if view == None:
			return

		isExactly = True
		if SublimeSocketAPISettings.SELECTEDREGIONS_ISEXACTLY in params:
			isExactly = params[SublimeSocketAPISettings.SELECTEDREGIONS_ISEXACTLY]

		isSameLine = False
		if SublimeSocketAPISettings.SELECTEDREGIONS_ISSAMELINE in params:
			isSameLine = params[SublimeSocketAPISettings.SELECTEDREGIONS_ISSAMELINE]

		selecteds = params[SublimeSocketAPISettings.SELECTEDREGIONS_SELECTEDS]
		regionsDict = self.server.regionsDict()
		
		# run selector if selected region contains 
		if path in regionsDict:
			# if already sekected, no event running.
			currentSelectedRegionIdsSet = self.server.selectingRegionIds(path)

			regionsDictOfThisView = regionsDict[path]

			# search each region identity
			def isRegionSelected(regionData):
				regionFrom = regionData[SublimeSocketAPISettings.REGION_FROM]
				regionTo = regionData[SublimeSocketAPISettings.REGION_TO]
				region = self.editorAPI.generateRegion(regionFrom, regionTo)

				if self.editorAPI.isRegionContained(region, selecteds, isExactly, isSameLine):
					return True
				return False

			latestContainedRegionIdentities = [regionIdentity for regionIdentity, regionData in regionsDictOfThisView.items() if isRegionSelected(regionData)]
			# run each region's each regionDatas.
			for containedRegionId in latestContainedRegionIdentities:
				if containedRegionId in currentSelectedRegionIdsSet:
					continue
				else:
					pass

				regionDatas = regionsDictOfThisView[containedRegionId]
				line = regionDatas[SublimeSocketAPISettings.SELECTEDREGIONS_LINE]
				fromParam = regionDatas[SublimeSocketAPISettings.SELECTEDREGIONS_FROM]
				toParam = regionDatas[SublimeSocketAPISettings.SELECTEDREGIONS_TO]
				messages = regionDatas[SublimeSocketAPISettings.SELECTEDREGIONS_MESSAGES]

				# add the line contents of this region. selection x region
				crossed = self.editorAPI.crossedContents(view, fromParam, toParam)

				SushiJSONParser.runSelectors(
					params, 
					SublimeSocketAPISettings.SELECTEDREGIONS_INJECTIONS, 
					[path, name, crossed, line, fromParam, toParam, messages],
					self.runAPI
				)

			# update current contained region for preventing double-run.
			self.server.updateSelectingRegionIdsAndResetOthers(path, latestContainedRegionIdentities)
			currentSelectedRegionIdsSet = self.server.selectingRegionIds(path)

	def defineFilter(self, params):
		assert SublimeSocketAPISettings.DEFINEFILTER_NAME in params, "defineFilter require 'name' key."

		# load defined filters
		filterNameAndPatternsArray = self.server.filtersDict()

		filterName = params[SublimeSocketAPISettings.DEFINEFILTER_NAME]

		filters = params[SublimeSocketAPISettings.DEFINEFILTER_FILTERS]
		assert type(filters) == list, "defineFilter require: filterPatterns must be list."

		patterns = []

		def mustBeSingleDict(filterDict):
			assert len(filterDict) is 1, "defineFilter. too many filter in one dictionary. len is "+str(len(filterDict))
			pattern = list(filterDict)[0]

			patterns.append(pattern)

		[mustBeSingleDict(currentFilterDict) for currentFilterDict in filters]

		filterNameAndPatternsArray[filterName] = filters
		self.server.updateFiltersDict(filterNameAndPatternsArray)

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.DEFINEFILTER_INJECTIONS,
			[filterName, patterns],
			self.runAPI
		)
		

	def filtering(self, params):
		assert SublimeSocketAPISettings.FILTERING_NAME in params, "filtering require 'name' param."
		assert SublimeSocketAPISettings.FILTERING_SOURCE in params, "filtering require 'source' param."

		filterName = params[SublimeSocketAPISettings.FILTERING_NAME]
		filterSource = params[SublimeSocketAPISettings.FILTERING_SOURCE]


		debug = False
		if SublimeSocketAPISettings.FILTERING_DEBUG in params:
			debug = params[SublimeSocketAPISettings.FILTERING_DEBUG]

		filtersDict = self.server.filtersDict()

		if filterName in filtersDict:
			pass

		else:
			self.editorAPI.printMessage("filterName:"+str(filterName) + " " + "is not yet defined.")
			return
		
		# get filter key-values array
		filterPatternsArray = filtersDict[filterName]

		for pattern in filterPatternsArray:

			key = list(pattern)[0]
			
			executablesDict = pattern[key]


			if debug:
				self.editorAPI.printMessage("filterName:"+str(filterName))
				self.editorAPI.printMessage("pattern:" + str(pattern))
				self.editorAPI.printMessage("executablesDict:" + str(executablesDict))

			if SushiJSON.SUSHIJSON_KEYWORD_SELECTORS in executablesDict:
				pass
			else:
				continue

			dotall = False
			if SublimeSocketAPISettings.DEFINEFILTER_DOTALL in executablesDict:
				dotall = executablesDict[SublimeSocketAPISettings.DEFINEFILTER_DOTALL]

			# search
			if dotall:
				searchResult = re.finditer(re.compile(r'%s' % key, re.M | re.DOTALL), filterSource)				
			else:
				searchResult = re.finditer(re.compile(r'%s' % key, re.M), filterSource)


			
			for searched in searchResult:
				if searched:
					paramDict = copy.deepcopy(executablesDict)
					if SushiJSON.SUSHIJSON_KEYWORD_INJECTS in paramDict:
						injectionDict = paramDict[SushiJSON.SUSHIJSON_KEYWORD_INJECTS].copy()
					else:
						injectionDict = {}
						
					
					if debug:
						executablesArray = paramDict[SushiJSON.SUSHIJSON_KEYWORD_SELECTORS]
					
						self.editorAPI.printMessage("matched defineFilter selectors:" + str(executablesArray))
						self.editorAPI.printMessage("filterSource\n---------------------\n" + filterSource + "\n---------------------")
						self.editorAPI.printMessage("matched group():" + str(searched.group()))
						self.editorAPI.printMessage("matched groups():" + str(searched.groups()))
					
						if SublimeSocketAPISettings.DEFINEFILTER_COMMENT in paramDict:
							self.editorAPI.printMessage("matched defineFilter comment:" + paramDict[SublimeSocketAPISettings.DEFINEFILTER_COMMENT])

					for index in range(len(searched.groups())):
						searchedValue = searched.groups()[index]
						
						searchedKey = "groups[" + str(index) + "]"
						paramDict[searchedKey] = searchedValue

						# inject if not revealed yet.
						if searchedKey in injectionDict:
							pass
						else:
							injectionDict[searchedKey] = searchedValue

					paramDict["group"] = searched.group()
					if "group" in injectionDict:
						pass
					else:
						injectionDict["group"] = searched.group()

					injectionDict[SublimeSocketAPISettings.FILTERING_SOURCE] = filterSource

					
					SushiJSONParser.runSelectors(
						paramDict,
						injectionDict.keys(),
						injectionDict.values(),
						self.runAPI
					)

				else:
					if debug:
						self.editorAPI.printMessage("filtering not match")

	## set reactor for reactive-event
	def setEventReactor(self, params):
		assert SublimeSocketAPISettings.SETREACTOR_REACT in params, "setEventReactor require 'react' param."
		
		reactEventName = params[SublimeSocketAPISettings.SETREACTOR_REACT]

		check = False
		for prefix in SublimeSocketAPISettings.REACTIVE_PREFIXIES:
			if reactEventName.startswith(prefix):
				check = True

		assert check, "setEventReactor can only set the 'react' param which starts with 'ss_f_' or 'event_' prefix."
		
		self.setReactor(params)

	## set reactor for view
	def setViewReactor(self, params):
		self.setReactor(params)
		
		
	## erase all reactors
	def resetReactors(self, params):
		deletedReactors = self.removeAllReactors()

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.RESETREACTORS_INJECTIONS,
			[deletedReactors],
			self.runAPI
		)

		


	def viewEmit(self, params):
		assert SublimeSocketAPISettings.VIEWEMIT_IDENTITY in params, "viewEmit require 'identity' param."
		
		identity = params[SublimeSocketAPISettings.VIEWEMIT_IDENTITY]

		# delay
		delay = 0
		if SublimeSocketAPISettings.VIEWEMIT_DELAY in params:
			delay = params[SublimeSocketAPISettings.VIEWEMIT_DELAY]

		
		(view, path, name) = self.internal_getViewAndPathFromViewOrName(params, SublimeSocketAPISettings.VIEWEMIT_VIEW, SublimeSocketAPISettings.VIEWEMIT_NAME)
		if view == None:
			return

		if not self.isExecutableWithDelay(SublimeSocketAPISettings.SS_FOUNDATION_VIEWEMIT, identity, delay):
			pass

		else:
			body = self.editorAPI.bodyOfView(view)

			modifiedPath = path.replace(":","&").replace("\\", "/")

			# get modifying line num
			rowColStr = self.editorAPI.selectionAsStr(view)
			
			SushiJSONParser.runSelectors(
				params, 
				SublimeSocketAPISettings.VIEWEMIT_INJECTIONS, 
				[body, path, name, modifiedPath, rowColStr, identity],
				self.runAPI
			)

	def modifyView(self, params):
		(view, path, name) = self.internal_getViewAndPathFromViewOrName(params, SublimeSocketAPISettings.MODIFYVIEW_VIEW, SublimeSocketAPISettings.MODIFYVIEW_NAME)
		if view == None:
			return

		line = 0
		to = 0

		if SublimeSocketAPISettings.MODIFYVIEW_ADD in params:
			add = params[SublimeSocketAPISettings.MODIFYVIEW_ADD]

			# insert text to the view with "to" or "line" param, or other.
			if SublimeSocketAPISettings.MODIFYVIEW_TO in params:
				to = int(params[SublimeSocketAPISettings.MODIFYVIEW_TO])
				line = self.editorAPI.getLineFromPoint(view, to)

				self.editorAPI.runCommandOnView(view, 'insert_text', {'string': add, "fromParam":to})

			elif SublimeSocketAPISettings.MODIFYVIEW_LINE in params:
				line = int(params[SublimeSocketAPISettings.MODIFYVIEW_LINE])
				to = self.editorAPI.getTextPoint(view, line)

				self.editorAPI.runCommandOnView(view, 'insert_text', {'string': add, "fromParam":to})

			# no "line" set = append the text to next to the last character of the view.
			else:
				self.editorAPI.runCommandOnView(view, 'insert_text', {'string': add, "fromParam":self.editorAPI.viewSize(view)})
			
		if SublimeSocketAPISettings.MODIFYVIEW_REDUCE in params:
			self.editorAPI.runCommandOnView(view, 'reduce_text')

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.MODIFYVIEW_INJECTIONS,
			[path, name, line, to],
			self.runAPI
		)

	## generate selection to view
	def setSelection(self, params):
		(view, path, name) = self.internal_getViewAndPathFromViewOrName(params, SublimeSocketAPISettings.SETSELECTION_VIEW, SublimeSocketAPISettings.SETSELECTION_NAME)

		if view == None:
			return
		
		assert SublimeSocketAPISettings.SETSELECTION_SELECTIONS in params, "setSelection require 'selections' param."
		
		selections = params[SublimeSocketAPISettings.SETSELECTION_SELECTIONS]
		
		
		def appendSelection(selection):
			regionFrom = selection[SublimeSocketAPISettings.SETSELECTION_FROM]
			regionTo = selection[SublimeSocketAPISettings.SETSELECTION_TO]
			
			if regionTo < 0:
				regionFrom = 0
				regionTo = self.editorAPI.viewSize(view)

			region = self.editorAPI.generateRegion(regionFrom, regionTo)
			
			self.editorAPI.addSelectionToView(view, region)

			return [regionFrom, regionTo]

		selecteds = [appendSelection(selection) for selection in selections]

		# emit viewReactor
		viewParams = self.editorAPI.generateSublimeViewInfo(
			view,
			SublimeSocketAPISettings.VIEW_SELF,
			SublimeSocketAPISettings.VIEW_ID,
			SublimeSocketAPISettings.VIEW_BUFFERID,
			SublimeSocketAPISettings.VIEW_PATH,
			SublimeSocketAPISettings.VIEW_NAME,
			SublimeSocketAPISettings.VIEW_VNAME,
			SublimeSocketAPISettings.VIEW_SELECTEDS,
			SublimeSocketAPISettings.VIEW_ISEXIST)


		emitIdentity = str(uuid.uuid4())
		viewParams[SublimeSocketAPISettings.REACTOR_VIEWKEY_EMITIDENTITY] = emitIdentity

		self.fireReactor(SublimeSocketAPISettings.REACTORTYPE_VIEW, SublimeSocketAPISettings.SS_VIEW_ON_SELECTION_MODIFIED_BY_SETSELECTION, viewParams)
		
		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.SETSELECTION_INJECTIONS,
			[path, name, selecteds],
			self.runAPI
		)

		


	def clearSelection(self, params):
		(view, path, name) = self.internal_getViewAndPathFromViewOrName(params, SublimeSocketAPISettings.CLEARSELECTION_VIEW, SublimeSocketAPISettings.CLEARSELECTION_NAME)
		if view == None:
			return

		cleards = self.editorAPI.clearSelectionOfView(view)
		
		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.CLEARSELECTION_INJECTIONS,
			[path ,name, cleards],
			self.runAPI
		)



	## show message
	def showStatusMessage(self, params):
		if SublimeSocketAPISettings.LOG_FORMAT in params:
			currentParams = self.formattingMessageParameters(params, SublimeSocketAPISettings.LOG_FORMAT, SublimeSocketAPISettings.LOG_MESSAGE)
			self.showStatusMessage(currentParams)
			return

		assert SublimeSocketAPISettings.SHOWSTATUSMESSAGE_MESSAGE in params, "showStatusMessage require 'message' param."
		message = params[SublimeSocketAPISettings.SHOWSTATUSMESSAGE_MESSAGE]
		self.editorAPI.statusMessage(message)

		if SublimeSocketAPISettings.SHOWSTATUSMESSAGE_DEBUG in params:
			if params[SublimeSocketAPISettings.SHOWSTATUSMESSAGE_DEBUG]:
				self.showAtLog({"message":message})


	## append region
	def appendRegion(self, params):
		if SublimeSocketAPISettings.LOG_FORMAT in params:
			currentParams = self.formattingMessageParameters(params, SublimeSocketAPISettings.LOG_FORMAT, SublimeSocketAPISettings.LOG_MESSAGE)
			self.appendRegion(currentParams)
			return
			
		assert SublimeSocketAPISettings.APPENDREGION_LINE in params, "appendRegion require 'line' param."
		assert SublimeSocketAPISettings.APPENDREGION_MESSAGE in params, "appendRegion require 'message' param."
		assert SublimeSocketAPISettings.APPENDREGION_CONDITION in params, "appendRegion require 'condition' param."

		line = params[SublimeSocketAPISettings.APPENDREGION_LINE]
		message = params[SublimeSocketAPISettings.APPENDREGION_MESSAGE]
		condition = params[SublimeSocketAPISettings.APPENDREGION_CONDITION]

		(view, path, name) = self.internal_getViewAndPathFromViewOrName(params, SublimeSocketAPISettings.APPENDREGION_VIEW, SublimeSocketAPISettings.APPENDREGION_NAME)
		
		
		# add region
		if view != None:
			regions = []
			regions.append(self.editorAPI.getLineRegion(view, line))

			identity = SublimeSocketAPISettings.REGION_UUID_PREFIX + str(regions[0])
			
			# add region to displaying region in view.
			self.editorAPI.addRegionToView(view, identity, regions, condition, "sublime.DRAW_OUTLINED")
			
			# store region
			regionFrom, regionTo = self.editorAPI.convertRegionToTuple(regions[0])
			
			self.server.storeRegion(path, identity, line, regionFrom, regionTo, message)

			SushiJSONParser.runSelectors(
				params,
				SublimeSocketAPISettings.APPENDREGION_INJECTIONS,
				[path, name, identity, line, regionFrom, regionTo, message, condition],
				self.runAPI
			)


		# raise no view found
		else:
			# use name param to notify the name of the view which not opened in editor.
			if SublimeSocketAPISettings.APPENDREGION_NAME in params:
				name = params[SublimeSocketAPISettings.APPENDREGION_NAME]
			else:
				return

			currentParams = {}
			currentParams[SublimeSocketAPISettings.NOVIEWFOUND_NAME] = name
			currentParams[SublimeSocketAPISettings.NOVIEWFOUND_MESSAGE] = message

			self.fireReactor(SublimeSocketAPISettings.REACTORTYPE_VIEW, SublimeSocketAPISettings.SS_FOUNDATION_NOVIEWFOUND, currentParams)
			


	## emit notification mechanism
	def notify(self, params):
		assert SublimeSocketAPISettings.NOTIFY_TITLE in params, "notify require 'title' param."
		assert SublimeSocketAPISettings.NOTIFY_MESSAGE in params, "notify require 'message' param."

		title = params[SublimeSocketAPISettings.NOTIFY_TITLE]
		message = params[SublimeSocketAPISettings.NOTIFY_MESSAGE]
		
		env = self.editorAPI.platform()

		if env == "osx":
			debug = False
			if SublimeSocketAPISettings.NOTIFY_DEBUG in params:
				debug = params[SublimeSocketAPISettings.NOTIFY_DEBUG]
			
			exe = "\"" + self.editorAPI.packagePath() + "/"+SublimeSocketAPISettings.MY_PLUGIN_PATHNAME+"/tool/notification/MacNotifier.sh\""
			exeArray = ["-t", title, "-m", message, "-replaceunderscore", "", ]

			shellParams = {
				SublimeSocketAPISettings.RUNSHELL_MAIN: "/bin/sh",
				exe: exeArray,
				SublimeSocketAPISettings.RUNSHELL_DEBUG: debug
			}
			
			self.runShell(shellParams)

			SushiJSONParser.runSelectors(
				params,
				SublimeSocketAPISettings.NOTIFY_INJECTIONS,
				[title, message],
				self.runAPI
			)
			



	## get current project's file paths
	def getAllFilePath(self, params):
		assert SublimeSocketAPISettings.GETALLFILEPATH_ANCHOR in params, "getAllFilePath require 'anchor' param."

		anchor = params[SublimeSocketAPISettings.GETALLFILEPATH_ANCHOR]

		self.setSublimeSocketWindowBasePath({})

		filePath = self.sublimeSocketWindowBasePath

		if filePath:
			pass
		else:
			return

		folderPath = os.path.dirname(filePath)
	
		depth = len(filePath.split("/"))-1
		
		basePath_default = "default"
		basePath = basePath_default

		folderPath2 = folderPath


		limitation = -1
		if SublimeSocketAPISettings.GETALLFILEPATH_LIMIT in params:
			limitation = params[SublimeSocketAPISettings.GETALLFILEPATH_LIMIT]


		for i in range(depth-1):
			for r,d,f in os.walk(folderPath):

				for files in f:
					if files == anchor:
						basePath = os.path.join(r,files)
						break
						
				if basePath != basePath_default:
					break

			if basePath != basePath_default:
				break

			
			if limitation == 0:
				
				return

			limitation = limitation - 1

			# not hit, up
			folderPath = os.path.dirname(folderPath)

			

		baseDir = os.path.dirname(basePath)


		paths = []
		fullpaths = []
		for r,d,f in os.walk(baseDir):
			for files in f:
				fullPath = os.path.join(r,files)
				
				partialPath = fullPath.replace(baseDir, "")

				paths.append(partialPath)
				fullpaths.append(fullPath)

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.GETALLFILEPATH_INJECTIONS,
			[baseDir, paths, fullpaths],
			self.runAPI
		)

		


	def readFile(self, params):
		assert SublimeSocketAPISettings.READFILE_PATH in params, "readFile require 'path' param."
		
		original_path = params[SublimeSocketAPISettings.READFILE_PATH]

		path = self.getKeywordBasedPath(original_path, 
			SublimeSocketAPISettings.RUNSUSHIJSON_PREFIX_SUBLIMESOCKET_PATH,
			self.editorAPI.packagePath() + "/"+SublimeSocketAPISettings.MY_PLUGIN_PATHNAME+"/")

		currentFile = open(path, 'r')
		data = currentFile.read()
		currentFile.close()

		if data:
			SushiJSONParser.runSelectors(
				params, 
				SublimeSocketAPISettings.READFILE_INJECTIONS, 
				[original_path, path, data],
				self.runAPI
			)


	def eventEmit(self, params):
		assert SublimeSocketAPISettings.EVENTEMIT_TARGET in params, "eventEmit require 'target' param."
		assert SublimeSocketAPISettings.EVENTEMIT_EVENT in params, "eventEmit require 'eventemit' param."

		target = params[SublimeSocketAPISettings.EVENTEMIT_TARGET]
		eventName = params[SublimeSocketAPISettings.EVENTEMIT_EVENT]
		assert eventName.startswith(SublimeSocketAPISettings.REACTIVE_PREFIX_USERDEFINED_EVENT), "eventEmit only emit 'user-defined' event such as starts with 'event_' keyword."

		self.fireReactor(SublimeSocketAPISettings.REACTORTYPE_EVENT, eventName, params)

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.EVENTEMIT_INJECTIONS,
			[target, eventName],
			self.runAPI
		)


	def cancelCompletion(self, params):
		(view, _, _) = self.internal_getViewAndPathFromViewOrName(params, SublimeSocketAPISettings.CANCELCOMPLETION_VIEW, SublimeSocketAPISettings.CANCELCOMPLETION_NAME)
		
		if view != None:
			# hide completion
			self.editorAPI.runCommandOnView(view, "hide_auto_complete")

			SushiJSONParser.runSelectors(
				params,
				SublimeSocketAPISettings.CANCELCOMPLETION_INJECTIONS,
				[],
				self.runAPI
			)
			

	
	def runCompletion(self, params):
		assert SublimeSocketAPISettings.RUNCOMPLETION_COMPLETIONS in params, "runCompletion require 'completion' param."
		
		(view, path, name) = self.internal_getViewAndPathFromViewOrName(params, SublimeSocketAPISettings.RUNCOMPLETION_VIEW, SublimeSocketAPISettings.RUNCOMPLETION_NAME)
		if view == None:
			return

		
		completions = params[SublimeSocketAPISettings.RUNCOMPLETION_COMPLETIONS]		

		formatHead = ""
		if SublimeSocketAPISettings.RUNCOMPLETION_FORMATHEAD in params:
			formatHead = params[SublimeSocketAPISettings.RUNCOMPLETION_FORMATHEAD]

		formatTail = ""
		if SublimeSocketAPISettings.RUNCOMPLETION_FORMATTAIL in params:
			formatTail = params[SublimeSocketAPISettings.RUNCOMPLETION_FORMATTAIL]
		

		def transformToFormattedTuple(sourceDict):
			a = formatHead
			b = formatTail
			for key in sourceDict:
				a = a.replace(key, sourceDict[key])
				b = b.replace(key, sourceDict[key])
			
			return (a, b)
			
		completionStrs = list(map(transformToFormattedTuple, completions))
		
		
		# set completion
		self.updateCompletion(path, completionStrs)

		# display completions
		self.editorAPI.runCommandOnView(view, "auto_complete")

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.RUNCOMPLETION_INJECTIONS,
			[path, name],
			self.runAPI
		)
			

	def forcelySave(self, params):
		(view, path, name) = self.internal_getViewAndPathFromViewOrName(params, SublimeSocketAPISettings.FORCELYSAVE_VIEW, SublimeSocketAPISettings.FORCELYSAVE_NAME)
		if view == None:
			return

		self.editorAPI.runCommandOnView(view, 'forcely_save')

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.FORCELYSAVE_INJECTIONS,
			[path, name],
			self.runAPI
		)

		
	def setSublimeSocketWindowBasePath(self, params):
		def runInMainThread():
			basepath = self.editorAPI.getFileName()
			if basepath:
				basename = os.path.basename(basepath)
				self.sublimeSocketWindowBasePath = basepath
				
				SushiJSONParser.runSelectors(
					params,
					SublimeSocketAPISettings.SETSUBLIMESOCKETWINDOWBASEPATH_INJECTIONS,
					[basepath, basename],
					self.runAPI
				)
		self.editorAPI.runAfterDelay(lambda: runInMainThread(), 0)

		
		
	## verify SublimeSocket API-version and SublimeSocket version
	def versionVerify(self, params, clientId):
		assert clientId, "versionVerify require 'client' object."
		assert SublimeSocketAPISettings.VERSIONVERIFY_SOCKETVERSION in params, "versionVerify require 'socketVersion' param."
		assert SublimeSocketAPISettings.VERSIONVERIFY_APIVERSION in params, "versionVerify require 'apiVersion' param."
		

		# targetted socket version
		targetSocketVersion = int(params[SublimeSocketAPISettings.VERSIONVERIFY_SOCKETVERSION])

		# targetted API version
		targetVersion = params[SublimeSocketAPISettings.VERSIONVERIFY_APIVERSION]
		

		# current socket version
		currentSocketVersion = SublimeSocketAPISettings.SSSOCKET_VERSION

		# current API version
		currentVersion			= SublimeSocketAPISettings.SSAPI_VERSION


		# check socket version
		if targetSocketVersion is not currentSocketVersion:
			self.sendVerifiedResultMessage(0, targetSocketVersion, SublimeSocketAPISettings.SSSOCKET_VERSION, targetVersion, currentVersion, client)
			return

		# SublimeSocket version matched.

		# check socket versipn
		targetVersionArray = targetVersion.split(".")

		targetMajor	= int(targetVersionArray[0])
		targetMinor	= int(targetVersionArray[1])
		# targetPVer	= int(targetVersionArray[2])

		
		currentVersionArray = currentVersion.split(".")

		currentMajor	= int(currentVersionArray[0])
		currentMinor	= int(currentVersionArray[1])
		# currentPVer		= int(currentVersionArray[2])

		code = SublimeSocketAPISettings.VERIFICATION_CODE_REFUSED_DIFFERENT_SUBLIMESOCKET

		isDryRun = False
		if SublimeSocketAPISettings.VERSIONVERIFY_DRYRUN in params:
			isDryRun = params[SublimeSocketAPISettings.VERSIONVERIFY_DRYRUN]

		# major check
		if targetMajor < currentMajor:
			code = SublimeSocketAPISettings.VERIFICATION_CODE_REFUSED_CLIENT_UPDATE
			message = self.sendVerifiedResultMessage(code, isDryRun, targetSocketVersion, SublimeSocketAPISettings.SSSOCKET_VERSION, targetVersion, currentVersion, clientId)

		elif targetMajor == currentMajor:
			if targetMinor < currentMinor:
				code = SublimeSocketAPISettings.VERIFICATION_CODE_VERIFIED_CLIENT_UPDATE
				message = self.sendVerifiedResultMessage(code, isDryRun, targetSocketVersion, SublimeSocketAPISettings.SSSOCKET_VERSION, targetVersion, currentVersion, clientId)

			elif targetMinor == currentMinor:
				code = SublimeSocketAPISettings.VERIFICATION_CODE_VERIFIED
				message = self.sendVerifiedResultMessage(code, isDryRun, targetSocketVersion, SublimeSocketAPISettings.SSSOCKET_VERSION, targetVersion, currentVersion, clientId)

			else:
				code = SublimeSocketAPISettings.VERIFICATION_CODE_REFUSED_SUBLIMESOCKET_UPDATE
				message = self.sendVerifiedResultMessage(code, isDryRun, targetSocketVersion, SublimeSocketAPISettings.SSSOCKET_VERSION, targetVersion, currentVersion, clientId)
				
		else:
			code = SublimeSocketAPISettings.VERIFICATION_CODE_REFUSED_SUBLIMESOCKET_UPDATE
			message = self.sendVerifiedResultMessage(code, isDryRun, targetSocketVersion, SublimeSocketAPISettings.SSSOCKET_VERSION, targetVersion, currentVersion, clientId)


		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.VERSIONVERIFY_INJECTIONS, 
			[code, message],
			self.runAPI
		)

		

	## send result to client then exit or continue WebSocket connection.
	def sendVerifiedResultMessage(self, resultCode, isDryRun, targetSocketVersion, currentSocketVersion, targetAPIVersion, currentAPIVersion, clientId):
		# python-switch
		for case in PythonSwitch(resultCode):
			if case(SublimeSocketAPISettings.VERIFICATION_CODE_REFUSED_DIFFERENT_SUBLIMESOCKET):
				message = "REFUSED/DIFFERENT_SUBLIMESOCKET:	The current running SublimeSocket version = "+str(currentSocketVersion)+", please choose the other version of SublimeSocket. this client requires SublimeSocket "+str(targetSocketVersion)+", see https://github.com/sassembla/SublimeSocket"

				self.server.sendMessage(clientId, message)

				if not isDryRun:
					self.server.closeClient(clientId)
			
				break
			if case(SublimeSocketAPISettings.VERIFICATION_CODE_VERIFIED):
				message = "VERIFIED:	The current running SublimeSocket api version = "+currentAPIVersion+", SublimeSocket "+str(currentSocketVersion)
				self.server.sendMessage(clientId, message)
				break
			if case(SublimeSocketAPISettings.VERIFICATION_CODE_VERIFIED_CLIENT_UPDATE):
				message = "VERIFIED/CLIENT_UPDATE: The current running SublimeSocket api version = "+currentAPIVersion+", this client requires api version = "+str(targetAPIVersion)+", please update this client if possible."
				self.server.sendMessage(clientId, message)
				break

			if case(SublimeSocketAPISettings.VERIFICATION_CODE_REFUSED_SUBLIMESOCKET_UPDATE):
				message = "REFUSED/SUBLIMESOCKET_UPDATE:	The current running SublimeSocket api version = "+currentAPIVersion+", this is out of date. please update SublimeSocket. this client requires SublimeSocket "+str(targetAPIVersion)+", see https://github.com/sassembla/SublimeSocket"
				self.server.sendMessage(clientId, message)
				
				if not isDryRun:
					self.server.closeClient(clientId)

				break

			if case(SublimeSocketAPISettings.VERIFICATION_CODE_REFUSED_CLIENT_UPDATE):
				message = "REFUSED/CLIENT_UPDATE:	The current running SublimeSocket api version = "+currentAPIVersion+", this client requires api version = "+str(targetAPIVersion)+", required api version is too old. please update this client."
				self.server.sendMessage(clientId, message)
				
				if not isDryRun:
					self.server.closeClient(clientId)
					
				break

		self.editorAPI.printMessage("verify: " + message)
		return message

	def checkIfViewExist_appendRegion_Else_notFound(self, view, viewInstance, line, message, condition):
		# this check should be run in main thread
		return self.server.internal_appendRegion(viewInstance, line, message, condition)

	### region control


	## erase all regions of view/condition
	def eraseAllRegions(self, params):
		regionsDict = self.server.regionsDict()
		
		deletes = {}
		if regionsDict:
			deleteTargetPaths = []

			# if target view specified and it exist, should erase specified view's regions only.
			if SublimeSocketAPISettings.API_ERASEALLREGIONS in params:
				(_, path, _) = self.internal_getViewAndPathFromViewOrName(params, None, SublimeSocketAPISettings.ERASEALLREGIONS_NAME)
				
				if path and path in regionsDict:
					deleteTargetPaths.append(path)

				# if not found, do nothing.
				else:
					pass

			else:
				deleteTargetPaths = list(regionsDict)

		
			def eraseRegions(path):
				targetRegionsDict = regionsDict[path]
				
				deletedRegionIdentities = []
				for regionIdentity in targetRegionsDict:
					(view, _) = self.internal_detectViewInstance(path)
					if view != None:
						self.editorAPI.removeRegionFromView(view, regionIdentity)

						deletedRegionIdentities.append(regionIdentity)
				

				if deletedRegionIdentities:
					deletes[path] = deletedRegionIdentities

			[eraseRegions(path) for path in deleteTargetPaths]
			
			for delPath in deletes:
				del regionsDict[delPath]

			self.server.updateRegionsDict(regionsDict)
		
		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.ERASEALLREGIONS_INJECTIONS,
			[deletes],
			self.runAPI
		)

		

	
	def formattingMessageParameters(self, params, formatKey, outputKey):
		currentParams = copy.deepcopy(params)
		currentFormat = currentParams[formatKey]

		for key in params:
			if key != formatKey:
				currentParam = str(currentParams[key])
				currentFormat = currentFormat.replace("["+key+"]", currentParam)

		
		currentParams[outputKey] = currentFormat
		del currentParams[formatKey]

		return currentParams

	def getKeywordBasedPath(self, path, keyword, replace):
		if path.startswith(keyword):
			filePathArray = path.split(keyword[-1])
			path = replace + filePathArray[1]

		return path












	# view series

	def internal_detectViewPath(self, view):
		instances = []
		viewsDict = self.server.viewsDict()
		
		if viewsDict:
			for path in list(viewsDict):
				viewInstance = viewsDict[path][SublimeSocketAPISettings.VIEW_SELF]
				if view == viewInstance:
					return path

				instances.append(viewInstance)

		return None


	def internal_getViewAndPathFromViewOrName(self, params, viewParamKey, nameParamKey):
		view = None
		path = None

		if viewParamKey and viewParamKey in params:
			view = params[viewParamKey]
			
			path = self.internal_detectViewPath(view)
			
				
		elif nameParamKey and nameParamKey in params:
			name = params[nameParamKey]
			
			(view, name) = self.internal_detectViewInstance(name)
			path = self.internal_detectViewPath(view)


		if view != None and path:
			return (view, path, name)
		else:
			return (None, None, None)


	## get the target view-s information if params includes "filename.something" or some pathes represents filepath.
	def internal_detectViewInstance(self, name):
		# if specific path used, load current filename of the view.
		if SublimeSocketAPISettings.SS_VIEWKEY_CURRENTVIEW == name:
			name = self.editorAPI.getFileName()

		viewDict = self.server.viewsDict()
		if viewDict:
			viewKeys = viewDict.keys()

			viewSearchSource = name

			# remove empty and 1 length string pattern.
			if not viewSearchSource or len(viewSearchSource) is 0:
				return None

			viewSearchSource = viewSearchSource.replace("\\", "&")
			viewSearchSource = viewSearchSource.replace("/", "&")

			# straight full match in viewSearchSource. "/aaa/bbb/ccc.d something..." vs "*********** /aaa/bbb/ccc.d ***********"
			for viewKey in viewKeys:

				# replace path-expression by component with &.
				viewSearchKey = viewKey.replace("\\", "&")
				viewSearchKey = viewSearchKey.replace("/", "&")

				if re.findall(viewSearchSource, viewSearchKey):
					return (viewDict[viewKey][SublimeSocketAPISettings.VIEW_SELF], name)
			
			# partial match in viewSearchSource. "ccc.d" vs "********* ccc.d ************"
			for viewKey in viewKeys:
				viewBasename = viewDict[viewKey][SublimeSocketAPISettings.VIEW_NAME]
				if viewBasename in viewSearchSource:
					return (viewDict[viewKey][SublimeSocketAPISettings.VIEW_SELF], name)

		# totally, return None and do nothing
		return (None, None)


	## collect current views
	def collectViews(self, params):
		collecteds = []
		for views in [window.views() for window in self.editorAPI.windows()]:
			for view in views:
				viewParams = self.editorAPI.generateSublimeViewInfo(
					view,
					SublimeSocketAPISettings.VIEW_SELF,
					SublimeSocketAPISettings.VIEW_ID,
					SublimeSocketAPISettings.VIEW_BUFFERID,
					SublimeSocketAPISettings.VIEW_PATH,
					SublimeSocketAPISettings.VIEW_NAME,
					SublimeSocketAPISettings.VIEW_VNAME,
					SublimeSocketAPISettings.VIEW_SELECTEDS,
					SublimeSocketAPISettings.VIEW_ISEXIST
				)

				emitIdentity = str(uuid.uuid4())
				viewParams[SublimeSocketAPISettings.REACTOR_VIEWKEY_EMITIDENTITY] = emitIdentity


				self.fireReactor(
					SublimeSocketAPISettings.REACTORTYPE_VIEW,
					SublimeSocketAPISettings.SS_EVENT_COLLECT, 
					viewParams
				)

				collecteds.append(viewParams[SublimeSocketAPISettings.VIEW_PATH])

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.COLLECTVIEWS_INJECTIONS,
			[collecteds],
			self.runAPI
		)

		
	

	def runRenew(self, eventParam):
		viewInstance = eventParam[SublimeSocketAPISettings.VIEW_SELF]
		filePath = eventParam[SublimeSocketAPISettings.REACTOR_VIEWKEY_PATH]

		if self.editorAPI.isBuffer(filePath):
			if self.editorAPI.isNamed(viewInstance):
				pass
			else:
				# no name buffer view will ignore.
				return
			
		# update or append if exist.
		viewDict = self.server.viewsDict()


		viewInfo = {}
		if filePath in viewDict:
			viewInfo = viewDict[filePath]

		viewInfo[SublimeSocketAPISettings.VIEW_ISEXIST] = eventParam[SublimeSocketAPISettings.REACTOR_VIEWKEY_ISEXIST]
		viewInfo[SublimeSocketAPISettings.VIEW_ID] = eventParam[SublimeSocketAPISettings.REACTOR_VIEWKEY_ID]
		viewInfo[SublimeSocketAPISettings.VIEW_BUFFERID] = eventParam[SublimeSocketAPISettings.REACTOR_VIEWKEY_BUFFERID]
		viewInfo[SublimeSocketAPISettings.VIEW_NAME] = filePath
		viewInfo[SublimeSocketAPISettings.VIEW_VNAME] = eventParam[SublimeSocketAPISettings.REACTOR_VIEWKEY_VNAME]
		viewInfo[SublimeSocketAPISettings.VIEW_SELF] = viewInstance

		# add
		viewDict[filePath] = viewInfo
		self.server.updateViewsDict(viewDict)

	def runDeletion(self, eventParam):
		view = eventParam[SublimeSocketAPISettings.VIEW_SELF]
		path = eventParam[SublimeSocketAPISettings.REACTOR_VIEWKEY_PATH]

		viewsDict = self.server.viewsDict()
		regionsDict = self.server.regionsDict()

		# delete
		if path in viewsDict:
			del viewsDict[path]
			self.server.updateViewsDict(viewsDict)

		if path in regionsDict:
			del regionsDict[path]
			self.server.updateRegionsDict(regionsDict)



	# reactor series
	def setReactor(self, params):
		assert SublimeSocketAPISettings.SETREACTOR_TARGET in params, "set_X_Reactor require 'target' param."
		assert SublimeSocketAPISettings.SETREACTOR_REACT in params, "set_X_Reactor require 'react' param."
		assert SublimeSocketAPISettings.SETREACTOR_REACTORS in params, "set_X_Reactor require 'reactors' param."

		reactorsDict = self.server.reactorsDict()
		reactorsLogDict = self.server.reactorsLogDict()

		target = params[SublimeSocketAPISettings.SETREACTOR_TARGET]
		reactEventName = params[SublimeSocketAPISettings.SETREACTOR_REACT]
		reactors = params[SublimeSocketAPISettings.SETREACTOR_REACTORS]

		# set default delay
		delay = 0
		if SublimeSocketAPISettings.SETREACTOR_DELAY in params:
			delay = params[SublimeSocketAPISettings.SETREACTOR_DELAY]
		

		# store reactors as selectors.
		reactDict = {}
		reactDict[SushiJSON.SUSHIJSON_KEYWORD_SELECTORS] = reactors
		reactDict[SublimeSocketAPISettings.SETREACTOR_DELAY] = delay

		if SushiJSON.SUSHIJSON_KEYWORD_INJECTS in params:
			reactDict[SushiJSON.SUSHIJSON_KEYWORD_INJECTS] = params[SushiJSON.SUSHIJSON_KEYWORD_INJECTS]

		if SublimeSocketAPISettings.SETREACTOR_ACCEPTS in params:
			reactDict[SublimeSocketAPISettings.SETREACTOR_ACCEPTS] = params[SublimeSocketAPISettings.SETREACTOR_ACCEPTS]

		# already set or not-> spawn dictionary for name.
		if not reactEventName in reactorsDict:			
			reactorsDict[reactEventName] = {}
			reactorsLogDict[reactEventName] = {}


		# store reactor			
		reactorsDict[reactEventName][target] = reactDict

		# reset reactLog too
		reactorsLogDict[reactEventName][target] = {}


		self.server.updateReactorsDict(reactorsDict)
		self.server.updateReactorsLogDict(reactorsLogDict)

		SushiJSONParser.runSelectors(
			params,
			SublimeSocketAPISettings.SETREACTOR_INJECTIONS,
			[target, reactEventName, delay],
			self.runAPI
		)


	def removeAllReactors(self):
		deletedReactorsList = []

		reactorsDict = self.server.reactorsDict()
		
		# from {'on_post_save': {'someone': {'delay': 0, 'selectors': []}}}
		# to [{on_post_save:someone}]
		for react, value in reactorsDict.items():
			for target in list(value):
				deletedReactorsList.append({react:target})
		
		# erase all
		self.server.updateReactorsDict({})
		self.server.updateReactorsLogDict({})
		
		return deletedReactorsList


	def fireReactor(self, reactorType, eventName, eventParam):

		reactorsDict = self.server.reactorsDict()
		reactorsLogDict = self.server.reactorsLogDict()

		if eventName in SublimeSocketAPISettings.REACTIVE_FOUNDATION_EVENT:
			if reactorsDict and eventName in reactorsDict:
				self.runFoundationEvent(eventName, eventParam, reactorsDict[eventName])
				
		else:
			if eventName in SublimeSocketAPISettings.VIEW_EVENTS_RENEW:
				self.runRenew(eventParam)

			if eventName in SublimeSocketAPISettings.VIEW_EVENTS_DEL:
				self.runDeletion(eventParam)

			# if reactor exist, run all selectors. not depends on "target".
			if reactorsDict and eventName in reactorsDict:
				reactorDict = reactorsDict[eventName]
				for reactorKey in list(reactorDict):
					
					delay = reactorsDict[eventName][reactorKey][SublimeSocketAPISettings.SETREACTOR_DELAY]
					if not self.isExecutableWithDelay(eventName, reactorKey, delay):
						pass

					else:
						reactorParams = reactorDict[reactorKey]
						self.runReactor(reactorType, reactorParams, eventParam)
						


	# completion series

	## return completion then delete.
	def consumeCompletion(self, viewIdentity, eventName):
		completions = self.server.completionsDict()
		if completions:
			if viewIdentity in list(completions):
				completion = completions[viewIdentity]
				
				self.server.deleteCompletion(viewIdentity)
				return completion

		return None

	def updateCompletion(self, viewIdentity, composedCompletions):
		completionsDict = self.server.completionsDict()

		completionsDict[viewIdentity] = composedCompletions
		self.server.updateCompletionsDict(completionsDict)
		

	# other

	def isExecutableWithDelay(self, name, target, elapsedWaitDelay):
		currentTime = round(int(time.time()*1000))
		reactorsLogDict = self.server.reactorsLogDict()

		if elapsedWaitDelay == 0:
			pass
		else:
			# check should delay or not.

			# delay log is exist.
			if name in reactorsLogDict and target in reactorsLogDict[name]:
				delayedExecuteLog = reactorsLogDict[name][target]
				if SublimeSocketAPISettings.REACTORSLOG_LATEST in delayedExecuteLog:
					latest = delayedExecuteLog[SublimeSocketAPISettings.REACTORSLOG_LATEST]

					# should delay = not enough time passed.
					if 0 < (elapsedWaitDelay + latest - currentTime):
						return False


		# update latest time

		# create executed log dict if not exist.
		if name in reactorsLogDict:
			if target in reactorsLogDict[name]:
				pass
			else:
				reactorsLogDict[name][target] = {}
		else:
			reactorsLogDict[name] = {}
			reactorsLogDict[name][target] = {}

		reactorsLogDict[name][target][SublimeSocketAPISettings.REACTORSLOG_LATEST]	= currentTime
		self.server.updateReactorsLogDict(reactorsLogDict)
		
		return True

class TransformerStream:
	def __init__(self, buf):
		self.buf = buf

	def write(self, text):
		self.buf.append(text)
		pass
