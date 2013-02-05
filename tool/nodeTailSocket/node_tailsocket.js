
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

	// if (data.lastIndexOf(prefix_errorheader_compile, 0) == 0) {
	// 	return "eval:[\"sublime.status_message('"+data+"')\"]";
	// }
	// if (data.lastIndexOf(prefix_error, 0) == 0) {
	// 	return "eval:[\"sublime.message_dialog('"+data+"')\"]";
	// }

	// if (data.lastIndexOf(prefix_file, 0) == 0) {

	// 	data = data.replace("(", "");
	// 	data = data.replace(")", "");
	// 	dataArray = data.split(" ");
		
	// 	for (var i in dataArray) {
	//   	dataArray[i] = dataArray[i].replace(/:/, "");
	//   }

	//   //only linenum... set dotmark on the error line.
	//   return "eval:[\"self.getLineCount_And_SetToArray("+dataArray[3]+",lines)\",\"regions.append(active_view.line(lines[0]))\",\"active_view.add_regions('hereComes', regions, 'comment', 'dot', sublime.DRAW_OUTLINED)\"]";
	// }
	// if (data.split(":").length - 1 == 2) {
	// 	//return "eval:[\"sublime.status_message('"+data+"')\"]";
	// }
	var json = '{"source":"' + data + '"}';
	var parsed = JSON.parse(json);
	return "ss@filter:" + JSON.stringify(parsed);
}

ws.on('open', function() {});

tail.on("line", function(message) {
	console.log("original	"+message);
	apiModifiedData = filterAndGenerateAPI(message);
	
 	ws.send(apiModifiedData);
});

ws.on('message', function(data, flags) {});
