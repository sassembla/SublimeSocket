
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
	
	var json = 
    {
        "name": "unity",
        "_detectPrefixPath": "/Users/sassembla/Desktop/PanzaerStrike/",
        "patterns": [
            {
                "[(]([0-9].*?),.*:(.*)": {
                    "runnable": {
                        "showLine": {
                            "line": "groups[1]",
                            "message": "groups[2]"
                        }
                    }
                }
            },
            {
                "Compilation failed:(.*)": {
                    "runnable": {
                        "eraseAllRegion": {},
                        "showStatusMessage": {
                            "message":"groups[0]"
                        }
                    }
                }
            },
            {
                "(^Mono: successfully reloaded assembly)": {
                    "runnable": {
                        "eraseAllRegion": {},
                        "showStatusMessage": {
                            "message":"groups[0]"
                        }
                    }
                }         
           }
        ]
    };

	ws.send("ss@defineFilter:"+JSON.stringify(json));
});

tail.on("line", function(message) {
	console.log("original	"+message);

	var json = 
    {
        "name": "unity",
        "source": message,
        "debug": true
    };
    
	apiModifiedData = "ss@detectView+filtering:" + JSON.stringify(json);
	
 	ws.send(apiModifiedData);
});

ws.on('message', function(data, flags) {
	console.log("input:"+data);

});
