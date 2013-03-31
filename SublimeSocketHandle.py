# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import threading
from SublimeWSServer import SublimeWSServer
from OpenPreference import Openpreference

# WebSocket server's thread
thread = None

class Socketon(sublime_plugin.TextCommand):
  def run(self, edit):
    self.startServer()

  @classmethod
  def startServer(self):
    global thread

    if thread is not None and thread.is_alive():
      alreadyRunningMessage = "SublimeSocket Already Running."

      sublime.status_message(alreadyRunningMessage)
      print "ss:", alreadyRunningMessage

      return 
        
    host = sublime.load_settings("SublimeSocket.sublime-settings").get('host')
    port = sublime.load_settings("SublimeSocket.sublime-settings").get('port')

    thread = SublimeSocketThread(host, port)
    thread.start()

class On_then_openpref(sublime_plugin.TextCommand):
  def run(self, edit):
    Socketon.startServer()
    Openpreference.openSublimeSocketPreference()
      

class Statuscheck(sublime_plugin.TextCommand):
  def run(self, edit):
    global thread
    if thread is not None and thread.is_alive():
      thread.currentConnections()
    else:
      notActivatedMessage = "SublimeSocket not yet activated."
      sublime.status_message(notActivatedMessage)
      print "ss:", notActivatedMessage

class Socketoff(sublime_plugin.TextCommand):
  def run(self, edit):
    global thread
    if thread is not None and thread.is_alive():
      thread.closeAllConnections()

# threading
class SublimeSocketThread(threading.Thread):
  def __init__(self, host, port):
    threading.Thread.__init__(self)
    self._server = SublimeWSServer()
    self._host = host
    self._port = port

  def run(self):
    self._server.start(self._host, self._port)


  # send eventName and data to server
  def toServer(self, eventName, eventParam=None):
    self._server.fireKVStoredItem(eventName, eventParam)
    
  def currentConnections(self):
    self._server.showCurrentConnections()
  
  def closeAllConnections(self):
    self._server.tearDown()

# event listeners
class CaptureEditing(sublime_plugin.EventListener):
  
  def on_modified(self, view):
    self.update("on_modified", view)
    
  def on_new(self, view):
    self.update("on_new", view)

  def on_clone(self, view):
    self.update("on_clone", view)

  def on_load(self, view):
    self.update("on_load", view)

  def on_close(self, view):
    self.update("on_close", view)

  def on_pre_save(self, view):
    self.update("on_pre_save", view)

  def on_post_save(self, view):
    self.update("on_post_save", view)
    
  def on_selection_modified(self, view):
    self.update("on_selection_modified", {"view":view})
    

  ## call when the event happen
  def update(self, eventName, param = None):
    global thread

    if thread is not None and thread.is_alive():
      thread.toServer(eventName, param)

