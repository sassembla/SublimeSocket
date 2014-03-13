# SublimeSocket
======
![SS](/main.png)

**The set of API Server, KVS and Executor** for the SublimeText and more.   
Connect something to editor.  
Control EditorAPI by inputted **JSON string**.  

You can construct **the chain of filters and events** that you want to do. 

ver 1.4._(Final)


#!notice!
the SublimeSocket 1.4.x is the last version for SublimeText2.  
**I never update this plugin** for ST2.  
Because the ST3 or the other editor (e.g. Atom by github) is very good and they has the future.  

see [SublimeSocket3](https://github.com/sassembla/SublimeSocket3)


##demos
* [Construct and run compilation for ]

* [Work with Unity	:	Build and show parameters and errors](https://vimeo.com/62957311)  
* [Work with TypeScript	:	Build and show errors with Chrome Ext](https://vimeo.com/63188211)  



##usage: CommandPalette >  
start WebSocket server

	SublimeSocket: on
	
	start serving ws at http://localhost:8823 by default.

show status
	
	SublimeSocket: status
	
	show SublimeSocket's status and list current connections name.

test

	SublimeSocket: on > test
	
	run SublimeSocket's test on current view..
	
teardown

	SublimeSocket: off
	
	teardown.


#Purpose/Motivation
* Control SublimeText API from the other process, data, input.
* Pick out all heavy-process from SublimeText to the outside & keep async.


#Done
* (Done)ST3 adopt -> go to [SublimeSocket3](https://github.com/sassembla/SublimeSocket3)
* (Done)Windows support -> go to [SublimeSocket3](https://github.com/sassembla/SublimeSocket3)
