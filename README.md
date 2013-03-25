# SublimeSocket
###### version 0.8.3
WebSocket server for SublieText.   
Control SublimeTextAPI through the WebSocket protocol.  

Keep SublimeText "LIGHT".


#Demo movie
[movie: Work with Unity](http://www.youtube.com/watch?v=3sXamdk30fY&feature=youtu.be)


#CommandPalette >  
##### SublimeSocket: on
**-> start WebSocket server at http://localhost:8823**

##### SublimeSocket: on > open preference
**-> server ON, then show SublimeSocket's preference,**  
**will connect to SublimeServer automatically.**  

##### SublimeSocket: open preference
**-> show SublimeSocket's preference.**  

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