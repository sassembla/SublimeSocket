# -*- coding: utf-8 -*-
import sublime, sublime_plugin

import SublimeWSSettings
import json

from SublimeWSEncoder import *
import SublimeSocketAPISettings

# import subprocess
# import shlex
# import os
# import difflib
import re


from PythonSwitch import *

## API Parse the action
class SublimeSocketAPI:
	def __init__(self, server):
		self.server = server
		self.encoder = SublimeWSEncoder()

	## Parse the API command via WebSocket
	def parse(self, data, client):
		# print "data is ", data

		# SAMPLE: inputIdentity:{"id":"537d5da6-ce7d-42f0-387b-d9c606465dbb"}->showAlert...
		commands = data.split(SublimeSocketAPISettings.API_CONCAT_DELIM)

    # command and param  SAMPLE:		inputIdentity:{"id":"537d5da6-ce7d-42f0-387b-d9c606465dbb"}
		for commandIdentityAndParams in commands :
			command_params = commandIdentityAndParams.split(SublimeSocketAPISettings.API_COMMAND_PARAMS_DELIM, 1)
			command = command_params[0]

			params = ''
			if 1 < len(command_params):
				params = json.loads(command_params[1])

			self.runAPI(command, params, client)


	## run the specified API with JSON parameters. Dict or Array of JSON.
	def runAPI(self, command, params, client=None):

		evalResults = "empty"
  	
  	# python-switch
		for case in PythonSwitch(command):
			if case(SublimeSocketAPISettings.API_INPUTIDENTITY):
				clientId = params["id"]
				self.server.setKV("clientId", str(clientId))
				break

			if case(SublimeSocketAPISettings.API_KILLSERVER):
				self.server.killServerSelf()
				break

			if case(SublimeSocketAPISettings.API_TIMEREVENT):
				#残りのタスクを内包して、非同期で抜ける。
				print "params ", params
				# どんな分散をするか、
				# self.timerEventSetIntreval()
				break
				
			if case(SublimeSocketAPISettings.API_DEFINEFILTER):
				# define filter
				self.defineFilter(params)
				break

			if case(SublimeSocketAPISettings.API_FILTER):
				# run filter
				self.filter(params)
				client.send("evalResults")
				break

			if case(SublimeSocketAPISettings.API_EVENTLISTEN):
				# set listener to KVS for observing the event occured
				self.eventListen(params)
				break

			if case(SublimeSocketAPISettings.API_SET_KVSTOREEVENT):
				# set event to listener
				self.setKVStoredEvent(params)
				break

			# if case(SublimeSocketAPISettings.API_RUNSHELL):
			# 	self.runShell(params)
			# 	break

			if case(SublimeSocketAPISettings.API_OUTPUT):
				self.output(params)
				break

			if case(SublimeSocketAPISettings.API_EVAL):
				sublime.set_timeout(lambda: self.sublimeEval(params), 0)
				break

			if case():
				print "unknown command", command
				break


	## run API with interval.
	def runOnInterval(self, key):
		print "runOnInterval", key


	## set event onto KVS
	def setKVStoredEvent(self, params):
		print "setKVStoredEvent", params
		self.server.setKV(SublimeSocketAPISettings.API_SET_KVSTOREEVENT, params)

	# ## run shellScript
	# # params is array that will be evaluated as commandline marameters.
	# def runShell(self, params):
	# 	runnable = ' '.join(params)
	# 	if len(runnable):
			
	# 		# print "runnable", runnable
	# 		self.process = subprocess.Popen(shlex.split(runnable.encode('utf8')), stdout=subprocess.PIPE, preexec_fn=os.setsid)
	# 		for line in self.process.stdout:
	# 			print line


	## Define the filter and 
	def defineFilter(self, params):
		print "defineFilter", params

		# ここで、ファイルの読み出しを行う。
		# check filter name
		if not params.has_key(SublimeSocketAPISettings.FILTER_NAME):
			print "no filterName key."
			return

		# load defined filters
		filterNameAndPatternsArray = {}

		if self.server.isExistOnKVS(SublimeSocketAPISettings.API_DEFINEFILTER):
			filterNameAndPatternsArray = self.server.getV(SublimeSocketAPISettings.API_DEFINEFILTER)

		print "loaded filterNameAndPatternsArray:", filterNameAndPatternsArray

		filterName = params[SublimeSocketAPISettings.FILTER_NAME]

		# key = filterName, value = the match patterns of filter.
		filterNameAndPatternsArray[filterName] = params[SublimeSocketAPISettings.FILTER_PATTERNS]

		self.server.setKV(SublimeSocketAPISettings.API_DEFINEFILTER, filterNameAndPatternsArray)

	## filteri. matching -> run API with interval
	def filter(self, params):
		# check filter name
		if not params.has_key(SublimeSocketAPISettings.FILTER_NAME):
			print "no filterName key."
			return

		filterName = params[SublimeSocketAPISettings.FILTER_NAME]

		# check filterName exists or not
		if not self.server.isFilterDefined(filterName):
			print "please define filter before　using. requested filterName is :", filterName
			return

		filterSource = params[SublimeSocketAPISettings.FILTER_SOURCE]
		# print "filterName", filterName, "	/filterSource",filterSource

		# get filter key-values array
		filterPatternsArray = self.server.getV(SublimeSocketAPISettings.API_DEFINEFILTER)[filterName]

		print "filterPatternsArray", filterPatternsArray

		for pattern in filterPatternsArray:
			# regx key filterSource
			print "filterぶんまわるはず", pattern, "/filterSource", filterSource
			# -----CompilerOutput:-stdout--exitcode: 1--compilationhadfailure: True--outfile: Temp/Assembly-CSharp.dll
			# Compilation failed: 1 error(s), 0 warnings
			# Assets/NewBehaviourScript.cs(6,12): error CS8025: Parsing error
			# (Filename: Assets/NewBehaviourScript.cs Line: 6)
			try:
				m = re.match(r"(-----\w+)", "-----CompilerOutput:-stdout--exitcode: 1--compilationhadfailure: True--outfile: Temp/Assembly-CSharp.dll")
				print "m is ", m
			except Exception as e:
				print "error",e
				



		# む、画面への反映ロジックのところおもしろいぞ！？　filterのファイル単位化での反映とかが必要かも。intervalでいいのかな。。


	## set/remove {eventListener : emitSetting} at the event that are observed by ST.
	# The event will reach every-view that included by the window.
	# KVS-key is SublimeSocketAPISettings.API_EVENTLISTEN
	# KVS-value is Dictionary {eventListener:emitSetting}
	def eventListen(self, params):
		print "eventListen", params
		# on_new(view)	None	Called when a new buffer is created.
		# on_clone(view)	None	Called when a view is cloned from an existing one.
		# on_load(view)	None	Called when the file is finished loading.
		# on_close(view)	None	Called when a view is closed (note, there may still be other views into the same buffer).
		# on_pre_save(view)	None	Called just before a view is saved.
		# on_post_save(view)	None	Called after a view has been saved.
		# on_modified(view)	None	Called after changes have been made to a view.
		# on_selection_modified(view)	None	Called after the selection has been modified in a view.
		# on_activated(view)	None	Called when a view gains input focus.
		# on_deactivated(view)	None	Called when a view loses input focus.
		# on_query_context(view, key, operator, operand, match_all)	bool or None	Called when determining to trigger a key binding with the given context key. If the plugin knows how to respond to the context, it should return either True of False. If the context is unknown, it should return None.
		# 	operator is one of:
		# 	sublime.OP_EQUAL. Is the value of the context equal to the operand?
		# 	sublime.OP_NOT_EQUAL. Is the value of the context not equal to the operand?
		# 	sublime.OP_REGEX_MATCH. Does the value of the context match the regex given in operand?
		# 	sublime.OP_NOT_REGEX_MATCH. Does the value of the context not match the regex given in operand?
		# 	sublime.OP_REGEX_CONTAINS. Does the value of the context contain a substring matching the regex given in operand?
		# 	sublime.OP_NOT_REGEX_CONTAINS. Does the value of the context not contain a substring matching the regex given in operand?
		# 	match_all should be used if the context relates to the selections: does every selection have to match (match_all = True), or is at least one matching enough (match_all = Fals)?
		
		keys = params.keys()
		eventObservationArray = {}

		# check acceptable event
		valid_events = set(keys) & set(SublimeSocketAPISettings.LISTEN_EVENTS)
		for eventIdentity in valid_events:
			eventObservationArray[eventIdentity] = params[eventIdentity]
			

		# update
		self.server.setKV(SublimeSocketAPISettings.API_EVENTLISTEN, eventObservationArray)
		

	## evaluate strings
	# Not only eval.
	# Set environment parameters from reading KVS
	def sublimeEval(self, params):
		# SUBLIME series
		# sublime.Region
		# sublime.status_message("can you see me?")
		# sublime.message_dialog("new connection approaching")
		# sublime.ok_cancel_dialog
		# sublime.load_settings
		# sublime.save_settings
		# sublime.windows()	#[<sublime.Window object at 0x115f11d70>]
		# sublime.active_window() #<sublime.Window object at 0x115f11d70>
		# sublime.packages_path() #/Users/sassembla/Library/Application Support/Sublime Text 2/Packages
		# sublime.installed_packages_path() #/Users/sassembla/Library/Application Support/Sublime Text 2/Installed Packages
		# sublime.get_clipboard() 
		# sublime.set_clipboard("hereComesDaredevil") 
		# score_selector
		# run_command
		# log_commands
		# log_input
		# version
		# platform
		# arch

		# WINDOW series
		window = sublime.active_window()

		# set default
		self.window = window

		# id()	
		# new_file()	
		# open_file(file_name, <flags>)	View	
		# active_view() #<sublime.View object at 0x10b768a60>
		# active_view_in_group(group)	View	Returns the currently edited view in the given group.
		# views()	[View]	Returns all open views in the window.
		# views_in_group(group)	[View]	Returns all open views in the given group.
		# num_groups()	int	Returns the number of view groups in the window.
		# active_group()	int	Returns the index of the currently selected group.
		# focus_group(group)	None	Makes the given group active.
		# focus_view(view)	None	Switches to the given view.
		# get_view_index(view)	(group, index)	Returns the group, and index within the group of the view. Returns -1 if not found.
		# set_view_index(view, group, index)	None	Moves the view to the given group and index.
		# folders()	[String]	Returns a list of the currently open folders.
		# run_command(string, <args>)	None	Runs the named WindowCommand with the (optional) given arguments.
		# show_quick_panel(items, on_done, <flags>)	None	Shows a quick panel, to select an item in a list. on_done will be called once, with the index of the selected item. If the quick panel was cancelled, on_done will be called with an argument of -1.
		# show_input_panel(caption, initial_text, on_done, on_change, on_cancel)	View	Shows the input panel, to collect a line of input from the user. on_done and on_change, if not None, should both be functions that expect a single string argument. on_cancel should be a function that expects no arguments. The view used for the input widget is returned.
		# get_output_panel(name)


		# VIEW series
		active_view = window.active_view()

		# set default
		self.view = active_view
		
		# id()	int	Returns a number that uniquely identifies this view.
		# buffer_id()	int	Returns a number that uniquely identifies the buffer underlying this view.
		# file_name()	String	The full name file the file associated with the buffer, or None if it doesn't exist on disk.
		# name()	String	The name assigned to the buffer, if any
		# set_name(name)	None	Assigns a name to the buffer
		# is_loading()	bool	Returns true if the buffer is still loading from disk, and not ready for use.
		# is_dirty()	bool	Returns true if there are any unsaved modifications to the buffer.
		# is_read_only()	bool	Returns true if the buffer may not be modified.
		# set_read_only(value)	None	Sets the read only property on the buffer.
		# is_scratch()	bool	Returns true if the buffer is a scratch buffer. Scratch buffers never report as being dirty.
		# set_scratch(value)	None	Sets the scratch property on the buffer.
		# settings()	Settings	Returns a reference to the views settings object. Any changes to this settings object will be private to this view.
		# window()	Window	Returns a reference to the window containing the view.
		# run_command(string, <args>)	None	Runs the named TextCommand with the (optional) given arguments.
		# size()	int	Returns the number of character in the file.
		# substr(region)	String	Returns the contents of the region as a string.
		# substr(point)	String	Returns the character to the right of the point.
		# begin_edit(<command>, <args>)	Edit	Creates an edit object, demarcating an undo group. A corresponding call to end_edit() is required.
		# end_edit(edit)	Edit	Finishes the edit.
		# insert(edit, point, string)	int	Inserts the given string in the buffer at the specified point. Returns the number of characters inserted: this may be different if tabs are being translated into spaces in the current buffer.
		# erase(edit, region)	None	Erases the contents of the region from the buffer.
		# replace(edit, region, string)	None	Replaces the contents of the region with the given string.
		# sel()	RegionSet	Returns a reference to the selection.
		# line(point)	Region	Returns the line that contains the point.
		# line(region)	Region	Returns a modified copy of region such that it starts at the beginning of a line, and ends at the end of a line. Note that it may span several lines.
		# full_line(point)	Region	As line(), but the region includes the trailing newline character, if any.
		# full_line(region)	Region	As line(), but the region includes the trailing newline character, if any.
		# lines(region)	[Region]	Returns a list of lines (in sorted order) intersecting the region.
		# split_by_newlines(region)	[Region]	Splits the region up such that each region returned exists on exactly one line.
		# word(point)	Region	Returns the word that contains the point.
		# word(region)	Region	Returns a modified copy of region such that it starts at the beginning of a word, and ends at the end of a word. Note that it may span several words.
		# find(pattern, fromPosition, <flags>)	Region	Returns the first Region matching the regex pattern, starting from the given point, or None if it can't be found. The optional flags parameter may be sublime.LITERAL, sublime.IGNORECASE, or the two ORed together.
		# find_all(pattern, <flags>, <format>, <extractions>)	[Region]	Returns all (non-overlapping) regions matching the regex pattern. The optional flags parameter may be sublime.LITERAL, sublime.IGNORECASE, or the two ORed together. If a format string is given, then all matches will be formatted with the formatted string and placed into the extractions list.
		# rowcol(point)	(int, int)	Calculates the 0 based line and column numbers of the point.
		# text_point(row, col)	int	Calculates the character offset of the given, 0 based, row and column. Note that 'col' is interpreted as the number of characters to advance past the beginning of the row.
		# set_syntax_file(syntax_file)	None	Changes the syntax used by the view. syntax_file should be a name along the lines of Packages/Python/Python.tmLanguage. To retrieve the current syntax, use view.settings().get('syntax').
		# extract_scope(point)	Region	Returns the extent of the syntax name assigned to the character at the given point.
		# scope_name(point)	String	Returns the syntax name assigned to the character at the given point.
		# score_selector(point, selector)	Int	Matches the selector against the scope at the given location, returning a score. A score of 0 means no match, above 0 means a match. Different selectors may be compared against the same scope: a higher score means the selector is a better match for the scope.
		# find_by_selector(selector)	[Regions]	Finds all regions in the file matching the given selector, returning them as a list.
		# show(point, <show_surrounds>)	None	Scroll the view to show the given point.
		# show(region, <show_surrounds>)	None	Scroll the view to show the given region.
		# show(region_set, <show_surrounds>)	None	Scroll the view to show the given region set.
		# show_at_center(point) 
		# show_at_center(region)	None	Scroll the view to center on the region.
		# visible_region()	Region	Returns the currently visible area of the view.
		# viewport_position()#	(0.0, 646.0) Vector	Returns the offset of the viewport in layout coordinates.
		# set_viewport_position(vector, <animate<)	None	Scrolls the viewport to the given layout position.
		# viewport_extent()	vector	Returns the width and height of the viewport.
		# layout_extent()	vector	Returns the width and height of the layout.
		# text_to_layout(point)	vector	Converts a text position to a layout position
		# layout_to_text(vector)	point	Converts a layout position to a text position
		# line_height()	real	Returns the light height used in the layout
		# em_width()	real	Returns the typical character width used in the layout
		# add_regions("hereC", regions, "comment")	 comment以外にもアイコンとかも有る
		# get_regions(key)	[regions]	Return the regions associated with the given key, if any
		# erase_regions(key)	None	Removed the named regions
		# set_status(key, value)	None	Adds the status key to the view. The value will be displayed in the status bar, in a comma separated list of all status values, ordered by key. Setting the value to the empty string will clear the status.
		# get_status(key)	String	Returns the previously assigned value associated with the key, if any.
		# erase_status(key)	None	Clears the named status.
		# command_history(index, <modifying_only>)	(String,Dict,int)	Returns the command name, command arguments, and repeat count for the given history entry, as stored in the undo / redo stack.
		# fold([regions])	bool	Folds the given regions, returning False if they were already folded
		# fold(region)	bool	Folds the given region, returning False if it was already folded
		# unfold(region)	[regions]	Unfolds all text in the region, returning the unfolded regions
		# unfold([regions])	[regions]	Unfolds all text in the regions, returning the unfolded regions
		# encoding()	String	Returns the encoding currently associated with the file
		# set_encoding(encoding)	None	Applies a new encoding to the file. This encoding will be used the next time the file is saved.
		# line_endings()	String	Returns the line endings used by the current file.
		# set_line_endings(line_endings)	None	Sets the line endings that will be applied when next saving.


		# REGIONSET series
		# clear()	None	Removes all regions.
		# add(region)	None	Adds the given region. It will be merged with any intersecting regions already contained within the set.
		# add_all(region_set)	None	Adds all regions in the given set.
		# subtract(region)	None	Subtracts the region from all regions in the set.
		# contains(region)	bool	Returns true iff the given region is a subset.


		# REGION series
		regions = []

		# region = sublime.Region(100,200)
		# begin()	int	Returns the minimum of a and b.
		# end()	int	Returns the maximum of a and b.
		# size()	int	Returns the number of characters spanned by the region. Always >= 0.
		# empty()	bool	Returns true iff begin() == end().
		# cover(region)	Region	Returns a Region spanning both this and the given regions.
		# intersection(region)	Region	Returns the set intersection of the two regions.
		# intersects(region)	bool	Returns True iff this == region or both include one or more positions in common.
		# contains(region)	bool	Returns True iff the given region is a subset.
		# contains(point)


		# SETTING series
		# get(name)	value	Returns the named setting.
		# get(name, default)	value	Returns the named setting, or default if it's not defined.
		# set(name, value)	None	Sets the named setting. Only primitive types, lists, and dictionaries are accepted.
		# erase(name)	None	Removes the named setting. Does not remove it from any parent Settings.
		# has(name)	bool	Returns true iff the named option exists in this set of Settings or one of its parents.
		# add_on_change(key, on_change)	None	Register a callback to be run whenever a setting in this object is changed.
		# clear_on_change(key)	None	Remove all callbacks registered with the given key.
		

		# ## SPECIAL DEFINES ##
		# The "eval" cannot  create values. Use these params as "you defined these params".
		lines = []

		# EVENTLISTENER and the other Base Class series ...no needs

		### EVALUATE ###
		results = []
		for executable in params:
			print executable
			result = eval(executable)
			if result == None:
				result = "None"
			results.append(executable+" = "+result+"	/")

		# return result
		# client.send(results)

	## change lineCount to wordCount that is, includes the target-line index at SublimeText.
	def getLineCount_And_SetToArray(self, lineCount, lineArray):
		#check the namespace of inputted param
		len(lineArray)

		# Convert from 1 based to a 0 based line number
		line = int(lineCount) - 1
		print "line	", line
		# Negative line numbers count from the end of the buffer
		if line < 0:
			lines, _ = self.view.rowcol(self.view.size())
			line = lines + line + 1

		pt = self.view.text_point(line, 0)

		#store params to local param.
		lineArray.append(pt)


		



