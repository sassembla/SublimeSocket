# -*- coding: utf-8 -*-
import sublime, sublime_plugin
from SublimeWSServer import *
from OpenPreference import *

class Socketon(sublime_plugin.TextCommand):
    def run(self, edit):
        self.startServer()
        
    # @classmethod
    def startServer(self):
        host = sublime.load_settings("SublimeSocket.sublime-settings").get('host')
        port = sublime.load_settings("SublimeSocket.sublime-settings").get('port')

        thread = SublimeSocketThread(host, port)
        thread.start()

class On_then_openpref(sublime_plugin.TextCommand):
    def run(self, edit):
        Socketon.startServer()
        Openpreference.openSublimeSocketPreference()

class Socketoff(sublime_plugin.TextCommand):
    def run(self, edit):
        print "off.... not yet implimented as standalone. Plase use preference > Kill Button"
        
# threading
class SublimeSocketThread(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self._server = SublimeWSServer()
        self._host = host
        self._port = port

    def run(self):
        self._server.start(self._host, self._port)
