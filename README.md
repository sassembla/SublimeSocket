# SublimeSocket
###### version 0.8.2
WebSocket server for SublieText. Control SublimeTextAPI through the WebSocket protocol.



#Demo movie
[movie: implemented TestConsole](http://www.youtube.com/watch?v=JGBRNrKjrtE)

[movie: Work with Unity](http://www.youtube.com/watch?v=JSdpa_LXa8c&feature=youtu.be)

[movie: Work with Unity part2](http://www.youtube.com/watch?v=JSdpa_LXa8c&feature=youtu.be)

#CommandPalette >  
##### SublimeSocket: on
**-> start WebSocket server at http://localhost:8823**

##### SublimeSocket: on > open preference
**-> server ON, then show SublimeSocket's preference,**  
**will connect to SublimeServer automatically.**  

##### SublimeSocket: open preference
**-> show SublimeSocket's preference.**  

##### SublimeSocket: off
**-> not yet work!!**  
Please restart SublimeText manually. or use preferences's kill button.
  

#Input & Filtering data to SublimeText
SublimeSocket can show "error" regions through the filtered-data from WebSocket.

here is sample filter for Unity3D.  
[https://github.com/sassembla/SublimeSocket/...UnityFilter.txt](https://github.com/sassembla/SublimeSocket/blob/unity/FilterSettingSamples/UnityFilter.txt)  

and tail-WebSocket node.js component using that unity filter.
[/tool/nodeTailSocket/node_tailsocket_unity.js](https://github.com/sassembla/SublimeSocket/blob/master/tool/nodeTailSocket/node_tailsocket.js)    



#Purpose/Motivation
* Enable control ST2 from other process, browser, websocket clients.
* Remove all heavy-process running with ST2. More light, less energy.


#ToDo
* stop server graceful
* ST3 adopt