# -*- coding: utf-8 -*-
import SublimeSocketAPISettings


import signal
import sys
import sublime
import sublime_plugin
import subprocess
import shlex
import threading
import glob
import string

class Openhtml(sublime_plugin.TextCommand):
  
  @classmethod
  def openSublimeSocketTest(self, params):
    assert "host" in params, "openSublimeSocketTest require 'host' param."
    assert "port" in params, "openSublimeSocketTest require 'port' param."

    # get current Plugin's tests path.
    host = params["host"]
    port = params["port"]

    currentPackagePath = sublime.packages_path() + "/"+SublimeSocketAPISettings.MY_PLUGIN_PATHNAME+"/"

    self.generateHTML(
        {
            SublimeSocketAPISettings.SS_HOST_REPLACE:host, 
            SublimeSocketAPISettings.SS_PORT_REPLACE:port,
        },
        currentPackagePath + "tests/tests.html", 
        currentPackagePath + "tmp/tests.html")


  @classmethod
  # replace, output, then open.
  def generateHTML(self, replaceableDict, sourcePath, outputPath):
    
    html = ""

    # prepare html contents    
    with open(sourcePath, mode='r', encoding='utf-8') as htmlFile:
        html = htmlFile.read()
        
    # replace host:port
    for key in replaceableDict:
        if key in SublimeSocketAPISettings.HTML_REPLACEABLE_KEYS:
            target = key
            value = replaceableDict[key]
            html = html.replace(target, str(value))

    # replace version
    html = html.replace(SublimeSocketAPISettings.SS_VERSION_REPLACE, SublimeSocketAPISettings.SSAPI_VERSION)

    # generate preference
    with open(outputPath, mode='w', encoding='utf-8') as htmlFile:
        htmlFile.write(html)
        
    # set Target-App to open Preference.html
    targetAppPath = sublime.load_settings("SublimeSocket.sublime-settings").get('preference browser')

    # mac only
    # compose command
    command = "open" + " " + "-a" + " " + targetAppPath + " \"" + outputPath + "\""

    # run on the other thread
    thread = BuildThread(command)
    thread.start()


class BuildThread(threading.Thread):
  def __init__(self, command):
    self.command = command  
    threading.Thread.__init__(self)

  def run(self):
    print("command = ", self.command)
    # run command
    subprocess.call(self.command, shell=True)



