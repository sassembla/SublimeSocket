// TypeScript ver 0.7.0

// process.argv.forEach(function (val, index, array) {
//   console.log(index + ': ' + val);
// });

// requires ws, nodetail
var WebSocket = require('ws');

var assert = require('assert');
// var msgpack = require('msgpack');
var ws = new WebSocket('ws://127.0.0.1:8823/');

Tail = require('tail').Tail;
var tscwithenvPath = process.argv[2];
var targetFilePath = process.argv[3]+"/*.ts";
var logPath = process.argv[3] + "/tscompile.log";


tail = new Tail(logPath);

ws.on('open', function() {
	console.log("OPENED");
	
    var inputIdentityJSON = 
    {
        "id" : "nodetail"
    }
	var defineFilterJSON = 
    {
        "name": "typescript",
        "patterns": [
            {
                "(.*)[.]ts[ ][(]([0-9]*),.*: (.*)": {
                    "selectors": [
                        {
                            "showStatusMessage": {
                                "message": "groups[0]"
                            }
                        },
                        {
                            "showAtLog": {
                                "message": "groups[0]"
                            }
                        },
                        {
                            "appendRegion": {
                                "line": "groups[2]",
                                "message": "\"groups[3]\"",
                                "view": "groups[1].ts",
                                "condition": "keyword"
                            }
                        }
                    ]
                }
            },
            {
                "(.*)[.]ts[(]([0-9]*),.*: (.*)": {
                    "selectors": [
                        {
                            "showStatusMessage": {
                                "message": "groups[0]"
                            }
                        },
                        {
                            "showAtLog": {
                                "message": "groups[0]"
                            }
                        },
                        {
                            "appendRegion": {
                                "line": "groups[2]",
                                "message": "\"groups[3]\"",
                                "view": "groups[1].ts",
                                "condition": "keyword"
                            }
                        }
                    ]
                }
            },
            {
                 "^start": {
                    "selectors": [
                        {
                            "eraseAllRegion":{}
                        }
                    ]
                }
            },
            {
                 "^typescript compile succeeded.": {
                    "selectors": [
                        {
                            "showStatusMessage": {
                                "message": "typescript compile succeeded."
                            }
                        },
                        {
                            "showAtLog": {
                                "message": "typescript compile succeeded."
                            }
                        },
                    ]
                }
            },
            {
                 "^typescript compile failure.": {
                    "selectors": [
                        {
                            "showStatusMessage": {
                                "message": "typescript compile failure."
                            }
                        },
                        {
                            "showAtLog": {
                                "message": "typescript compile failure."
                            }
                        },
                    ]
                }
            }
        ]
    };
    var cursorModifyReactorJSON = {
        "target": "typescript",
        "event": "on_selection_modified",
        "replacefromto": {
            "view": "view"
        },
        "interval": 100,
        // "debug":true,
        "selectors": [
            {
                "containsRegions": {
                    "target": "typescript",
                    "emit": "ss_errorEmitted",
                    // "debug": true,
                    "view": "replace"
                }
            }
        ]
    };
    var errorReactorJSON = {
        "target": "typescript",
        "event": "ss_errorEmitted",
        "replacefromto": {
            "message": "-message",
            "line": "-title"
        },
        "selectors": [
            {
                "runShell": {
                    "main": "terminal-notifier",
                    "-message": "\"default message\"",
                    "-title": "\"default title\"",
                    // "debug":true,
                    "-execute": "\"open -a 'Sublime Text 2.App'\""
                }
            }
        ]
    };

    var modifyReactJSON = {
        "target": "typescript",
        "event": "on_modified",
        "interval": 1000,
        "selectors": [
            {
                "runShell": {
                    "main": "/bin/sh",
                    "":[
                        tscwithenvPath,
                        targetFilePath,
                        logPath
                    ]
                }
            }
        ]
    };
    var saveReactorJSON = {
        "target": "typescript",
        "event": "on_post_save",
        "interval": 100,
        "selectors": [
            {
                "showStatusMessage": {
                    "message": "typescript compiling..."
                }
            },
            {
                "showAtLog": {
                    "message": "typescript compiling..."
                }
            },
            {
                "runShell": {
                    "main": "/bin/sh",
                    "":[
                        tscwithenvPath,
                        targetFilePath,
                        logPath
                    ]
                }
            }
        ] 
    };
    var setUpDone = {
        "message": "SublimeSocket : typescript-compilation sequence ready!"
    };

	ws.send("ss@inputIdentity:"+JSON.stringify(inputIdentityJSON)
        +"->defineFilter:"+JSON.stringify(defineFilterJSON)
        +"->setReactor:"+JSON.stringify(cursorModifyReactorJSON)
        +"->setReactor:"+JSON.stringify(errorReactorJSON)
        +"->setReactor:"+JSON.stringify(modifyReactJSON)
        +"->setReactor:"+JSON.stringify(saveReactorJSON)
        +"->showAtLog:"+JSON.stringify(setUpDone)
    );
});

tail.on("line", function(message) {
	console.log("original	"+message);

	var json = 
    {
        "name": "typescript",
        "source": message
        // "debug": true
    };
    
	apiModifiedData = "ss@filtering:" + JSON.stringify(json);
	
 	ws.send(apiModifiedData);
});

ws.on('message', function(data, flags) {
	console.log("input:"+data);    
});
