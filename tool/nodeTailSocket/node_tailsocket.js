
var WebSocket = require('ws');

var assert = require('assert');
var msgpack = require('msgpack');
var ws = new WebSocket('ws://127.0.0.1:8823/');

Tail = require('tail').Tail;
tail = new Tail("/Users/sassembla/Library/Logs/Unity/Editor.log");

ws.on('open', function() {});

tail.on("line", function(data) {
	
	apiModifiedData = "eval:[\"sublime.message_dialog('"+data+"')\"]"
	// apiModifiedData = 


	//json
	var str = {"mp" : apiModifiedData};
	
	//msgpack
	var bin = msgpack.pack(str);
  var arraybuffer = new Uint8Array(bin);

  ws.send(arraybuffer.buffer, {binary: true});//default mask:true(ws sets implicitly, from client to server) 
});

ws.on('message', function(data, flags) {});