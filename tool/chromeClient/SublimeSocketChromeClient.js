var ssChromeClient_tailing_tab = null;
var ssChromeClient_tailing_interval = 0;

var ssChromeClient_read_position = 0;
var ssChromeClient_current_text = null;
var ssChromeClient_display_lock = false;

var INTERVAL_TAILING = 500;

// settings for TypeScript
var CURRENT_SETTING_PATH = "SUBLIMESOCKET_PATH:tool/chromeClient/TypeScriptFilter.txt";

var TSC_COMPILESHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClient/tscwithenv.sh";

var TSC_COMPILETARGETFILENAME = "*.ts";
var TSC_COMPILETARGETLOGFILENAME = "tscompile.log";

chrome.browserAction.onClicked.addListener(function(tab){
    if( ssChromeClient_tailing_tab === null && tab.url.indexOf('file://') == 0){
        ssChromeClient_tailing_tab = tab;
        chrome.browserAction.setIcon({path:"images/sublimesocketchromeicon-active.png"});
        ssChromeClient_tailing_interval = setInterval(checkFile, INTERVAL_TAILING);
        
        // connect.
        _WS.init(tab.url);
        _WS.connect();
    }else{
        chrome.browserAction.setIcon({path:"images/sublimesocketchromeicon-inactive.png"});
        clearInterval(ssChromeClient_tailing_interval);
        ssChromeClient_tailing_tab = null;

        // close
        _WS.close();
    }
})

var _WS = {
    uri: 'ws://127.0.0.1:8823/',
    currentTargetFolderPath:"",
    
    ws: null,

    init : function (targetLogPath) {
        // replace file path as FileSystem path
        var logPath = targetLogPath.replace("file:///", "/");
        currentTargetFolderPath = logPath.replace("/"+TSC_COMPILETARGETLOGFILENAME, "");
    },

    connect : function (e) {
      _WS.s = new WebSocket(_WS.uri);
      _WS.s.onopen = function (e) { _WS.onOpen(e); };
      _WS.s.onclose = function (e) { _WS.onClose(e); };
      _WS.s.onmessage = function (e) { _WS.onMessage(e); };
      _WS.s.onerror = function (e) { _WS.onError(e); };
    },

    onOpen: function () {
        
        identityJSON = {
            "id":"SublimeSocketChromeClient"
        };

        showAtLogJSON = {
            "message": "SublimeSocketChromeClient connected to SublimeSocket."
        };

        showStatusMessageJSON = {
            "message": "SublimeSocketChromeClient connected to SublimeSocket."
        };

        runSettingJSON = {
            "path":CURRENT_SETTING_PATH
        };

        setReactorJSON_2 = {
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
                            TSC_COMPILESHELLPATH,
                            currentTargetFolderPath + TSC_COMPILETARGETFILENAME,
                            currentTargetFolderPath + TSC_COMPILETARGETLOGFILENAME
                        ]
                    }
                }
            ] 
        };

        showAtLogJSON_2 = {
            "message": "typescript-compilation sequence ready!"
        };

        showStatusMessageJSON_2 = {
            "message": "typescript-compilation sequence ready!"
        };


        //call api then get callback
        _WS.s.send('sublimesocket@inputIdentity:'+JSON.stringify(identityJSON)+
            "->showAtLog:"+JSON.stringify(showAtLogJSON)+
            "->showStatusMessage:"+JSON.stringify(showStatusMessageJSON)+
            "->runSetting:"+JSON.stringify(runSettingJSON)+
            "->setReactor:"+JSON.stringify(setReactorJSON_1)+
            "->setReactor:"+JSON.stringify(setReactorJSON_2)+
            "->showAtLog:"+JSON.stringify(showAtLogJSON_2)+
            "->showStatusMessage:"+JSON.stringify(showStatusMessageJSON_2)
        );
    },

    onClose: function () {
        console.log("closed!!?");
        // _WS.writeLog('<span class="label label-important">RESPONSE:DISCONNECTED</span>');
    },

    onMessage: function (e) {
        // _WS.writeLog('<span class="label label-success">RESPONSE: ' + e.data + '</span>');
    },

    onError: function (e) {
        // _WS.writeLog('<span style="color: red;">ERROR:</span> ' + e.data);
    },


    send: function (message) {
        if (!message.length) {
            alert('Empty message not allowed !');
        } else {
            _WS.s.send(message);
        }
    },
    close: function () {
        console.log("close!!");
        _WS.s.close();
    }
};



function checkFile(){
    if( ssChromeClient_tailing_tab == null ){
        return;
    }
    
    chrome.tabs.reload(ssChromeClient_tailing_tab.id);
    
    chrome.tabs.executeScript(
        ssChromeClient_tailing_tab.id, {code:'document.body.innerText'}, function(result){
            if( ssChromeClient_display_lock == true ){
                return;
            }

            if( ssChromeClient_current_text !== null ){
              ssChromeClient_current_text = result[0].substr(ssChromeClient_read_position);
            }else{
                ssChromeClient_current_text = '';
            }

            ssChromeClient_read_position = result[0].length;
            if( ssChromeClient_current_text == '' ){
                return;
            }
            chrome.windows.getAll(
                function(windows){
                    for( var i = 0; i < windows.length; i++ ){
                        chrome.tabs.getAllInWindow(
                            window.id, function(tabs){
                                for( var j = 0; j < tabs.length; j++ ){
                                    if( tabs[j].url.indexOf('file') == 0 || tabs[j].url.indexOf('http') == 0 ){
                                        if( ssChromeClient_current_text != '' ){

                                            var lines = ssChromeClient_current_text.split("\n");
                                            for (var i = 0; i < lines.length; i++) {
                                                filteringJSON = {
                                                    "name":"typescript",
                                                    "source":lines[i]
                                                };

                                                // console.log("ssChromeClient_current_text:"+ssChromeClient_current_text);
                                                _WS.s.send("ss@filtering:"+JSON.stringify(filteringJSON));
                                            }
                                        }
                                    }
                                }
                                ssChromeClient_current_text = '';
                                ssChromeClient_display_lock = false;
                            }
                        )
                    }
                }
            )
        }
    );
}

