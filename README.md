# SublimeSocket
##### version 1.4.0
**API Server** for the SublimeText.   
Control SublimeTextAPI via WebSocket protocol.  
![alt roundabout](https://dl.dropbox.com/u/36583594/2013%3A04%3A05%201-17-34/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202013-04-05%2013.27.48.png)  
・Keep SublimeText "LIGHT".  
・Show Errors and Suggestions on SublimeText.  
・Enable Tooltip as Mac-Notification.  



#Supported languages
* Unity + C# (Unity Asset, coming soon!)
* TypeScript (ChromeExtension)
* mruby (ChromeExtension) 

#Demo movie
* [Work with Unity	:	Build and show parameters and errors](https://vimeo.com/62957311)  
* [Work with TypeScript	:	Build and show errors with Chrome Ext](https://vimeo.com/63188211)  



#USAGE: CommandPalette >  
* ##### SublimeSocket: on
**-> start WebSocket server at http://localhost:8823**

* ##### SublimeSocket: on > open preference
**-> server ON, then show SublimeSocket's preference page.**  
(**will connect to SublimeServer automatically.**)

* ##### SublimeSocket: open preference
**-> show SublimeSocket's preference.**  

* ##### SublimeSocket: status
**-> show SublimeSocket's status and current connections.**  

* ##### SublimeSocket: off
Please restart SublimeText manually.
  

#sample filters
SublimeSocket can show "error" regions through the filtered-data from WebSocket.

* The sample filter for Unity3D:  
[https://github.com/sassembla/SublimeSocket/...UnityFilter.txt](https://github.com/sassembla/SublimeSocket/blob/unity/FilterSettingSamples/UnityFilter.txt)  

* The tail-WebSocket node.js component:  
[/tool/nodeTailSocket/node_tailsocket_unity.js](https://github.com/sassembla/SublimeSocket/blob/master/tool/nodeTailSocket/node_tailsocket.js)    




#Purpose/Motivation
* Enable control SublimeText from other process, browser, websocket clients.
* Pick out all heavy-process from SublimeText to the outside.


#ToDo
* Completion support

#Done
* (Done)ST3 adopt -> go to [SublimeSocket3](https://github.com/sassembla/SublimeSocket3)
* (Done)Windows support -> go to [SublimeSocket3](https://github.com/sassembla/SublimeSocket3)
