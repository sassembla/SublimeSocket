# -*- coding: utf-8 -*-
import SublimeWSSettings
import SublimeSocketAPISettings

import os
import signal
import sys
import sublime
import sublime_plugin
import subprocess
import shlex
import threading
import glob
import string

class Openpreference(sublime_plugin.TextCommand):
  def run (self, edit) :
    self.openSublimeSocketPreference()

  @classmethod
  def openSublimeSocketPreference(self):
    host = sublime.load_settings("SublimeSocket.sublime-settings").get('host')
    port = sublime.load_settings("SublimeSocket.sublime-settings").get('port')
    

    # create path of Preference.html
    currentPackagePath = sublime.packages_path() + "/SublimeSocket/"
    originalHtmlPath = "resource/source.html"
    originalPath = currentPackagePath + originalHtmlPath

    preferenceFilePath = "tmp/preference.html"
    preferencePath = currentPackagePath + preferenceFilePath

    # prepare html contents
    htmlFile = open(originalPath, 'r')
    html = htmlFile.read()
    htmlFile.close()
        
    # replace host:port
    html = html.replace(SublimeWSSettings.SS_HOST_REPLACE, host)
    html = html.replace(SublimeWSSettings.SS_PORT_REPLACE, str(port))

    # replace version
    html = html.replace(SublimeWSSettings.SS_VERSION_REPLACE, SublimeSocketAPISettings.API_VERSION)

    # generate preference
    outputFile = open(preferencePath, 'w')
    outputFile.write(html)
    outputFile.close()
    
    # set Target-App to open Preference.htnl
    targetAppPath = sublime.load_settings("SublimeSocket.sublime-settings").get('preference browser')

    # compose coomand
    command = "open" + " " + "-a" + " " + targetAppPath + " \"" + preferencePath + "\""

    # run on the other thread
    thread = BuildThread(command)
    thread.start()


class BuildThread(threading.Thread):
  def __init__(self, command):
    self.command = command  
    threading.Thread.__init__(self)

  def run(self):
    print "command = ", self.command
    # run command
    self.process = subprocess.Popen(shlex.split(self.command.encode('utf8')), stdout=subprocess.PIPE, preexec_fn=os.setsid)
    for line in self.process.stdout:
      print line



