// for TypeScript ver 1.0.0

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

console.log("connecting to SublimeSocket...");

tail = new Tail(logPath);

ws.on('open', function() {
    console.log("connected to SublimeSocket.");
    
    var inputIdentityJSON = 
    {
        "to" : "nodetail"
    }
    var defineFilterJSON = 
    {
        "name": "typescript",
        "filters": [
            {
                "(.*?)[(]([0-9].*?)[,].*: error .*: (.*)": {
                    "injects": {
                        "groups[0]": "name",
                        "groups[1]": "line",
                        "groups[2]": "message"
                    },
                    "selectors": [
                        {
                            "showStatusMessage<-message": {
                                
                            }
                        },
                        {
                            "showAtLog<-message": {

                            }
                        },
                        {
                            "appendRegion<-name, line, message": {
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
                            "eraseAllRegions":{}
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
        "react": "on_selection_modified",
        "delay": 100,
        "reactors": [
            {
                "selectedRegions<-name, selecteds": {
                    "selectors":[
                        {
                            "generate filtring source for quickfix/transform<-path, crossed, messages, to, line": {
                                "code": "import os\nname = os.path.basename(inputs[\"path\"])\nonselected = []\nmessages = inputs[\"messages\"]\nto = inputs[\"to\"]\nline = inputs[\"line\"]\nfor message in messages:\n\tselector = []\n\tfilteringContents = {\"name\":\"quickfix\", \"source\":message+\" @to \"+str(to)+\"  @line \"+str(line)+\" @on \"+name}\n\tfilteringAPI = {\"filtering\":filteringContents}\n\tselector.append(filteringAPI)\n\ttooltipItem = {}\n\ttooltipItem[message] = selector\n\tonselected.append(tooltipItem)\noutput({\"name\":name, \"onselected\":onselected, \"message\": messages[0]})\n",
                                "selectors": [
                                    {
                                        "clearSelection<-name": {

                                        }
                                    },
                                    {
                                        "afterAsync<-name, onselected": {
                                            "identity": "waitForClearSelection",
                                            "ms": 100,
                                            "selectors": [
                                                {
                                                    "showToolTip<-name, onselected": {
                                                        "oncancelled": [
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    };

    var saveReactorJSON = {
        "react": "on_post_save",
        "delay": 100,
        "reactors": [
            {
                "afterAsync": {
                    "identity": "typescript-compilation",
                    "ms": 1,
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
                }
            }
            
        ] 
    };
    
    var setUpDone = {
        "message": "SublimeSocket : typescript-compilation sequence ready!"
    };

    ws.send("ss@changeIdentity:"+JSON.stringify(inputIdentityJSON)
        +"->defineFilter:"+JSON.stringify(defineFilterJSON)
        +"->setViewReactor:"+JSON.stringify(cursorModifyReactorJSON)
        +"->setViewReactor:"+JSON.stringify(saveReactorJSON)
        +"->showAtLog:"+JSON.stringify(setUpDone)
    );
});

tail.on("line", function(message) {
    console.log("original   "+message);

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
