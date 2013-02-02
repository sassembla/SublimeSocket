
var WebSocket = require('ws');

var assert = require('assert');
var msgpack = require('msgpack');
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

	if (data.lastIndexOf(prefix_errorheader_compile, 0) == 0) {
		return "eval:[\"sublime.status_message('"+data+"')\"]";
	}
	if (data.lastIndexOf(prefix_error, 0) == 0) {
		return "eval:[\"sublime.message_dialog('"+data+"')\"]";
	}

	if (data.lastIndexOf(prefix_file, 0) == 0) {

		data = data.replace("(", "");
		data = data.replace(")", "");
		dataArray = data.split(" ");
		
		for (var i in dataArray) {
	  	dataArray[i] = dataArray[i].replace(/:/, "");
	  }

	  //only linenum... set dotmark on the error line.
		return "eval:[\"regions.append(active_view.line("+dataArray[3]+"))\", \"active_view.add_regions('error', regions, 'error', 'dot')\"]";
	}
	if (data.split(":").length - 1 == 2) {
		//return "eval:[\"sublime.status_message('"+data+"')\"]";
	}

	return "";
}

ws.on('open', function() {});

tail.on("line", function(message) {
	// console.log("original					"+data);

	apiModifiedData = filterAndGenerateAPI(message);

	if (apiModifiedData == "") return;

	console.log("\napiModifiedData "+apiModifiedData+"\n");
	//json
	var str = {"mp" : apiModifiedData};
	
	//msgpack
	var bin = msgpack.pack(str);
  var arraybuffer = new Uint8Array(bin);

  ws.send(arraybuffer.buffer, {binary: true});//default mask:true(ws sets implicitly, from client to server) 
});

ws.on('message', function(data, flags) {});