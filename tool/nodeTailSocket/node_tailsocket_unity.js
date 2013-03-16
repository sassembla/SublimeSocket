// requires ws, nodetail
var WebSocket = require('ws');

var assert = require('assert');
// var msgpack = require('msgpack');
var ws = new WebSocket('ws://127.0.0.1:8823/');

Tail = require('tail').Tail;
tail = new Tail("/Users/sassembla/Library/Logs/Unity/Editor.log");
// tail = new Tail("/Users/sassembla/errors.log");

ws.on('open', function() {
	console.log("OPENED");
	
    var inputIdentityJSON = 
    {
        "id" : "nodetail"
    }
	var defineFilterJSON = 
    {
        "name": "unity",
        "patterns": [
            {
                "[(]([0-9].*?),.*:(.*)": {
                    "selectors": [
                        {
                            "appendRegion": {
                                "line": "groups[1]",
                                "message": "groups[2]"
                            }
                        }
                    ]
                }
            },
            {
                "Compilation failed:(.*)": {
                    "selectors": [
                        {
                            "eraseAllRegion": {}
                        },{
                            "showStatusMessage": {
                                "message":"groups[0]"
                            }
                        }
                    }
                }
            },
            {
                "(^Mono: successfully reloaded assembly)": {
                    "selectors": [
                        {
                            "eraseAllRegion": {}
                        },{
                            "showStatusMessage": {
                                "message":"groups[0]"
                            }
                        }
                    ]
                }         
           }
        ]
    };
    var setReactorJSON = 
    {
        "target": "nodetail",
        "event": "on_selection_modified",
        "selectors": [
            {
                "containsREgions": {
                    "view": "will be replace to specific view",
                    "debug":true
                }
            }
        ],
        "replacefromto": {
            "view": "view"
        },
        "interval": 100
    };

	ws.send("ss@inputIdentity:"+JSON.stringify(inputIdentityJSON)
        +"->defineFilter:"+JSON.stringify(defineFilterJSON)
        +"->setReactor:"+JSON.stringify(setReactorJSON));
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
