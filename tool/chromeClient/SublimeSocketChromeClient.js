// 
// Client of SublimeSocket.
// 

var ssChromeClient_tailing_tab = null;
var ssChromeClient_tailing_interval = 0;

var ssChromeClient_read_position = 0;
var ssChromeClient_current_text = null;
var ssChromeClient_display_lock = false;

var INTERVAL_TAILING = 500;

// settings for TypeScript
var CURRENT_SETTING_PATH = "SUBLIMESOCKET_PATH:tool/chromeClient/TypeScriptFilter.txt";

var TSC_SIMPLE_COMPILE_SHELLPATH = "/Users/sassembla/Library/Application@s@s@Support/Sublime@s@s@Text@s@s@2/Packages/SublimeSocket/tool/chromeClient/tscshell.sh";

var TSC_TYPESCRIPTFILE_WILDCARD = "*.ts";
var TSC_COMPILETARGETLOGFILENAME = "tscompile.log";



var TARGET_FOCUSED = 0;
var TARGET_FOLDER = 1;
var TARGET_RECURSIVE = 2;

var TSC_COMPILATIONTARGETMODE = TARGET_FOLDER;
var TSC_IDENTIFIED_SENDER_STARTMARK = "typescriptsaved";
var TSC_IDENTIFIED_SENDER_ENDMARK = "typescriptcompilefinished";

var needTail = false;

chrome.browserAction.onClicked.addListener(function(tab){
    if( ssChromeClient_tailing_tab === null && tab.url.indexOf('file://') == 0){
        ssChromeClient_tailing_tab = tab;
        chrome.browserAction.setIcon({path:"images/sublimesocketchromeicon-active.png"});
        
        ssChromeClient_tailing_interval = setInterval(checkFile, INTERVAL_TAILING);

        // connect.
        _WS.init(tab.url, TSC_COMPILATIONTARGETMODE);
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
    currentCompilationTargetMode:-1,

    ws: null,

    init : function (targetLogPath, compilationTargetMode) {

        // replace file path as FileSystem path
        var logPath = targetLogPath.replace("file:///", "/");
        currentTargetFolderPath = logPath.replace("/"+TSC_COMPILETARGETLOGFILENAME, "/");

        currentCompilationTargetMode = compilationTargetMode;
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

        //call api then get callback
        _WS.s.send(
            'sublimesocket@inputIdentity:'+JSON.stringify(identityJSON)+
            "->showAtLog:"+JSON.stringify(showAtLogJSON)+
            "->showStatusMessage:"+JSON.stringify(showStatusMessageJSON)+
            "->runSetting:"+JSON.stringify(runSettingJSON)
        );
    },

    onClose: function () {
        console.log("closed!!?");
    },

    onMessage: function (e) {
        if (e.data.indexOf(TSC_IDENTIFIED_SENDER_STARTMARK) === 0) {
            
            var currentCompileTargetFileName = e.data.replace(TSC_IDENTIFIED_SENDER_STARTMARK+":","")
            if (currentCompileTargetFileName.indexOf(currentTargetFolderPath) !== -1) {
                // exist in target folder.
            } else {
                return;
            }

            var runShellJSON = "";

            switch (currentCompilationTargetMode) {
                case TARGET_FOCUSED:
                    
                    runShellJSON = {
                        "main": "/bin/sh",
                        "":[
                            "\"" + TSC_SIMPLE_COMPILE_SHELLPATH + "\"",
                            currentCompileTargetFileName,
                            currentTargetFolderPath + TSC_COMPILETARGETLOGFILENAME
                        ]
                    };

                    break;
                case TARGET_FOLDER:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "":[
                            "\"" + TSC_SIMPLE_COMPILE_SHELLPATH + "\"",
                            currentTargetFolderPath + TSC_TYPESCRIPTFILE_WILDCARD,
                            currentTargetFolderPath + TSC_COMPILETARGETLOGFILENAME
                        ]
                    };

                    break;
                case TARGET_RECURSIVE:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "":[
                            TSC_RECURSIVE_COMPILE_SHELLPATH,
                            currentTargetFolderPath + TSC_TYPESCRIPTFILE_WILDCARD,
                            currentTargetFolderPath + TSC_COMPILETARGETLOGFILENAME
                        ]
                    };
                    break;
            } 

            needTail = true;
            
            var command = "ss@runShell:"+JSON.stringify(runShellJSON);
            _WS.s.send(command);
        }

        if (e.data.indexOf(TSC_IDENTIFIED_SENDER_ENDMARK) === 0) {
            needTail = false;
        }

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

    if (!needTail) {
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
                                                console.log("line "+lines[i]);
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

