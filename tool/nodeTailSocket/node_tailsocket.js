
var WebSocket = require('ws');

var assert = require('assert');
// var msgpack = require('msgpack');
var ws = new WebSocket('ws://127.0.0.1:8823/');

Tail = require('tail').Tail;
tail = new Tail("/Users/sassembla/Library/Logs/Unity/Editor.log");

//error e.g and pre/suffix

//Compilation failed: 4 error(s), 0 warnings
prefix_errorheader_compile = "Compilation failed:";

//(Filename: Assets/ApplicationControl/ApplicationController.cs Line: 26)
prefix_file = "(Filename:"

prefix_error = "Error:";

function filterAndGenerateAPI (data) {
	
	return 
}

ws.on('open', function() {
	console.log("OPENED");
	
	// set Unity Filter,,,,toooooo hard to code.
	// var json = '{"filterName":"unity","filterPatterns":[{"-----CompilerOutput:-stdout--exitcode: (.+?)--.":["filterRunnable_eval:[\"sublime.message_dialog('groups[1]')\"]"]}]}';
	// var parsed = JSON.parse(json);
	// ws.send("ss@defineFilter:"+JSON.stringify(parsed));
});

tail.on("line", function(message) {
	console.log("original	"+message);

	var json = '{"name":"unity","source":"' + message + '"}';
	var parsed = JSON.parse(json);
	apiModifiedData = "ss@detectView+filtering:" + JSON.stringify(parsed);
	
 	ws.send(apiModifiedData);
});

ws.on('message', function(data, flags) {
	console.log("input:"+data);

});
