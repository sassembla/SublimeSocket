// 
// Client of SublimeSocket.
// 

var ssChromeClient_tailing_tab = null;
var ssChromeClient_tailing_interval = 0;

var ssChromeClient_read_position = 0;
var ssChromeClient_current_text = null;
var ssChromeClient_display_lock = false;

var INTERVAL_TAILING = 500;



var currentFilterName = "typescript";
var KEY_CLIENT_IDENTITY = "SublimeSocketChromeClient";


// settings for TypeScript
var CURRENT_SETTING_PATH = "SUBLIMESOCKET_PATH:tool/chromeClient/TypeScriptFilter.txt";

var TSC_SIMPLE_COMPILE_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClient/tscshell.sh";

var TSC_TYPESCRIPTFILE_WILDCARD = "*.ts";
var currentTSCompileLogFileName = "";


var TARGET_FOCUSED = 0;
var TARGET_FOLDER = 1;
var TARGET_RECURSIVE = 2;

var TSC_COMPILATIONTARGETMODE = TARGET_FOLDER;
var TSC_IDENTIFIED_SENDER_STARTMARK = "typescriptsaved";
var TSC_IDENTIFIED_SENDER_ENDMARK = "typescriptcompilefinished";

var needTail = false;

chrome.browserAction.onClicked.addListener(function(tab){
    if( ssChromeClient_tailing_tab === null && tab.url.indexOf('file://') == 0){

        if (tab.url.indexOf("%20") !== -1)  {
            window.alert("This address includes 'space' in path:"+tab.url+". Not acceptable. Please change project's path.");
        } else {
            ssChromeClient_tailing_tab = tab;
            chrome.browserAction.setIcon({path:"images/sublimesocketchromeicon-active.png"});

            needTail = false;        
            ssChromeClient_tailing_interval = setInterval(checkFile, INTERVAL_TAILING);

            // connect.
            _WS.init(tab.url, TSC_COMPILATIONTARGETMODE);
            _WS.connect();
        }
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

        pathArray = logPath.split("/");

        // last path is "logfile.log"
        currentTSCompileLogFileName = pathArray[pathArray.length-1];
        
        // get FolderPath
        currentTargetFolderPath = logPath.replace("/"+currentTSCompileLogFileName, "/");
        
        console.log("currentTargetFolderPath    "+currentTargetFolderPath);
        
        // set mode from preferences
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

        //call api then get callback
        _WS.s.send(
            'sublimesocket@inputIdentity:'+JSON.stringify(
            {
                "id":KEY_CLIENT_IDENTITY
            }
            )+
            "->showAtLog:"+JSON.stringify(
            {
                "message": "SublimeSocketChromeClient connected to SublimeSocket."
            }
            )+
            "->showStatusMessage:"+JSON.stringify(
            {
                "message": "SublimeSocketChromeClient connected to SublimeSocket."
            }
            )+
            "->runSetting:"+JSON.stringify(
            {
                "path":CURRENT_SETTING_PATH
            })
        );
    },

    onClose: function (e) {
        console.log("closed!!? closed nande!?"+e);
    },

    onMessage: function (e) {
        if (e.data.indexOf(TSC_IDENTIFIED_SENDER_STARTMARK) === 0) {
            
            var currentCompileTargetFileName = e.data.replace(TSC_IDENTIFIED_SENDER_STARTMARK+":","")
            
            console.log("currentCompileTargetFileName = "+currentCompileTargetFileName);
            console.log("currentTargetFolderPath = "+currentTargetFolderPath);

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
                            TSC_SIMPLE_COMPILE_SHELLPATH,
                            currentCompileTargetFileName,
                            currentTargetFolderPath + currentTSCompileLogFileName
                        ]
                    };

                    break;
                case TARGET_FOLDER:

                    runShellJSON = {
                        "main": "/bin/sh",
                        "":[
                            TSC_SIMPLE_COMPILE_SHELLPATH,
                            currentTargetFolderPath + TSC_TYPESCRIPTFILE_WILDCARD,
                            currentTargetFolderPath + currentTSCompileLogFileName
                        ]
                    };

                    break;
                case TARGET_RECURSIVE:
                    console.log("not yet implemented:recursive mode");
                    runShellJSON = {
                        "main": "/bin/sh",
                        "":[
                            TSC_RECURSIVE_COMPILE_SHELLPATH,
                            currentTargetFolderPath + TSC_TYPESCRIPTFILE_WILDCARD,
                            currentTargetFolderPath + currentTSCompileLogFileName
                        ]
                    };
                    break;
            } 

            needTail = true;
            
            var command = "ss@runShell:"+JSON.stringify(runShellJSON);

            _WS.s.send(command);
        } else {
            console.log("not hit !!"+e.data);
        }

        if (e.data.indexOf(TSC_IDENTIFIED_SENDER_ENDMARK) === 0) {
            needTail = false;
        }

    },

    onError: function (e) {
        console.log("error:"+e.error);
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
                    for(var i = 0; i < windows.length; i++){
                        chrome.tabs.getAllInWindow(
                            window.id, function(tabs){
                                for( var j = 0; j < tabs.length; j++ ){
                                    if( tabs[j].url.indexOf('file') == 0 || tabs[j].url.indexOf('http') == 0 ){
                                        if( ssChromeClient_current_text != '' ){

                                            var lines = ssChromeClient_current_text.split("\n");

                                            for (var i = 0; i < lines.length; i++) {
                                                var currentLine = lines[i].replace(/"/g, "@");
                                                // console.log("replaced line "+currentLine);


                                                filteringJSON = {
                                                    "name": currentFilterName,
                                                    "source": currentLine
                                                    // "debug": true
                                                };
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

