
var WebSocket = require('ws');

var assert = require('assert');
var msgpack = require('msgpack');
var ws = new WebSocket('ws://127.0.0.1:8823/');

Tail = require('tail').Tail;
tail = new Tail("/Users/sassembla/Library/Logs/Unity/Editor.log");

ws.on('open', function() {});

tail.on("line", function(data) {

	var str = {"mp" : data};

	//msgpack
	var bin = msgpack.pack(str);
  var arraybuffer = new Uint8Array(bin);
  ws.send(arraybuffer.buffer);

});

ws.on('message', function(data, flags) {});