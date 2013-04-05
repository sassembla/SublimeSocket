# SublimeSocket
###### version 0.8.6
**API Server** for the SublimeText.   
Control SublimeTextAPI via WebSocket protocol.  
![alt roundabout](https://dl.dropbox.com/u/36583594/2013%3A04%3A05%201-17-34/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202013-04-05%2013.02.38.png)
・Keep SublimeText "LIGHT".   
・Enable Tooltip as Notification.


#Demo movie
  

![alt unity](https://raw.github.com/sassembla/SublimeSocket/master/doc/images/U_SS_ST.png)  
[Work with Unity	:	Build and show parameters and errors](https://vimeo.com/62957311)  


![alt typescript](https://raw.github.com/sassembla/SublimeSocket/master/doc/images/TS_SS_ST.png)  
[Work with TypeScript	:	Build and show errors with Chrome Ext](https://vimeo.com/63188211)


#CommandPalette >  
##### SublimeSocket: on
**-> start WebSocket server at http://localhost:8823**

##### SublimeSocket: on > open preference
**-> server ON, then show SublimeSocket's preference,**  
**will connect to SublimeServer automatically.**  

##### SublimeSocket: open preference
**-> show SublimeSocket's preference.**  

##### SublimeSocket: status
**-> show SublimeSocket's status and current connections.**  

##### SublimeSocket: off
Please restart SublimeText manually.
  

#Input & Filtering data to SublimeText
SublimeSocket can show "error" regions through the filtered-data from WebSocket.

The sample filter for Unity3D:  
[https://github.com/sassembla/SublimeSocket/...UnityFilter.txt](https://github.com/sassembla/SublimeSocket/blob/unity/FilterSettingSamples/UnityFilter.txt)  

The tail-WebSocket node.js component:  
[/tool/nodeTailSocket/node_tailsocket_unity.js](https://github.com/sassembla/SublimeSocket/blob/master/tool/nodeTailSocket/node_tailsocket.js)    





#Purpose/Motivation
* Enable control ST2 from other process, browser, websocket clients.
* Pick out all heavy-process from SublimeText.


#ToDo
* ST3 adopt