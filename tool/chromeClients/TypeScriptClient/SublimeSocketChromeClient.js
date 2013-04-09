var ssChromeClient_tailing_tab = null;
var ssChromeClient_tailing_interval = 0;
var ssChromeClient_read_position = 0;
var ssChromeClient_current_text = null;
var ssChromeClient_display_lock = false;
var INTERVAL_TAILING = 500;
var currentFilterName = "typescript";
var CURRENT_SETTING_PATH = "SUBLIMESOCKET_PATH:tool/chromeClients/TypeScriptClient/TypeScriptFilter.txt";
var TSC_SIMPLE_COMPILE_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClient/tscshell.sh";
var TSC_RECURSIVE_COMPILE_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClient/tscshell.sh";
var TSC_TYPESCRIPTFILE_WILDCARD = "*.ts";
var TARGET_FOCUSED = 0;
var TARGET_FOLDER = 1;
var TARGET_RECURSIVE = 2;
var TSC_COMPILATIONTARGETMODE = TARGET_FOLDER;
var TSC_CHECKVERSIONRESULT = "API VERIFIED:";
var TSC_IDENTIFIED_SENDER_STARTMARK = "typescriptsaved";
var TSC_IDENTIFIED_SENDER_ENDMARK = "typescriptcompilefinished";
var needTail = false;
var websocketCont;
chrome.browserAction.onClicked.addListener(function (tab) {
    if(ssChromeClient_tailing_tab === null && tab.url.indexOf('file://') == 0) {
        ssChromeClient_tailing_tab = tab;
        chrome.browserAction.setIcon({
            path: "images/sublimesocketchromeicon-active.png"
        });
        needTail = false;
        ssChromeClient_tailing_interval = setInterval(checkFile, INTERVAL_TAILING);
        websocketCont = new WS();
        websocketCont.init(tab.url, TSC_COMPILATIONTARGETMODE);
        websocketCont.connect();
    } else {
        chrome.browserAction.setIcon({
            path: "images/sublimesocketchromeicon-inactive.png"
        });
        clearInterval(ssChromeClient_tailing_interval);
        ssChromeClient_tailing_tab = null;
        websocketCont.close();
    }
});
var WS = (function () {
    function WS() {
        this.uri = 'ws://127.0.0.1:8823/';
        this.currentTargetFolderPath = "";
        this.currentCompilationTargetMode = -1;
        this.currentTSCompileLogFileName = "defaultLogFileName";
    }
    WS.prototype.init = function (targetLogPath, compilationTargetMode) {
        var logPath = targetLogPath.replace("file:///", "/");
        var pathArray = logPath.split("/");
        this.currentTSCompileLogFileName = pathArray[pathArray.length - 1];
        this.currentTargetFolderPath = logPath.replace("/" + this.currentTSCompileLogFileName, "/");
        console.log("currentTargetFolderPath    " + this.currentTargetFolderPath);
        this.currentCompilationTargetMode = compilationTargetMode;
    };
    WS.prototype.connect = function () {
        var _this = this;
        this.ws = new WebSocket(this.uri);
        this.ws.onopen = function (e) {
            return _this.onOpen(e);
        };
        this.ws.onclose = function (e) {
            return _this.onClose(e);
        };
        this.ws.onmessage = function (e) {
            return _this.onMessage(e);
        };
        this.ws.onerror = function (e) {
            return _this.onError(e);
        };
    };
    WS.prototype.onOpen = function (e) {
        this.send("ss@runSetting:" + JSON.stringify({
            "path": CURRENT_SETTING_PATH
        }));
    };
    WS.prototype.onClose = function (e) {
        console.log("closed!!? closed nande!?" + e);
    };
    WS.prototype.onMessage = function (e) {
        if(e.data.indexOf(TSC_CHECKVERSIONRESULT) === 0) {
            console.log("checkVersion result:   " + e.data);
            return;
        }
        if(e.data.indexOf(TSC_IDENTIFIED_SENDER_STARTMARK) === 0) {
            console.log("save");
            var currentCompileTargetFileName = e.data.replace(TSC_IDENTIFIED_SENDER_STARTMARK + ":", "");
            if(currentCompileTargetFileName.indexOf(this.currentTargetFolderPath) !== -1) {
            } else {
                return;
            }
            var runShellJSON;
            switch(this.currentCompilationTargetMode) {
                case TARGET_FOCUSED:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "": [
                            TSC_SIMPLE_COMPILE_SHELLPATH, 
                            currentCompileTargetFileName, 
                            this.currentTargetFolderPath + this.currentTSCompileLogFileName
                        ],
                        "debug": true
                    };
                    break;
                case TARGET_FOLDER:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "": [
                            TSC_SIMPLE_COMPILE_SHELLPATH, 
                            this.currentTargetFolderPath + TSC_TYPESCRIPTFILE_WILDCARD, 
                            this.currentTargetFolderPath + this.currentTSCompileLogFileName
                        ],
                        "debug": true
                    };
                    break;
                case TARGET_RECURSIVE:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "": [
                            TSC_RECURSIVE_COMPILE_SHELLPATH, 
                            this.currentTargetFolderPath + TSC_TYPESCRIPTFILE_WILDCARD, 
                            this.currentTargetFolderPath + this.currentTSCompileLogFileName
                        ],
                        "debug": true
                    };
                    break;
            }
            needTail = true;
            var command = "ss@runShell:" + JSON.stringify(runShellJSON);
            console.log("TARGET_FOLDER here command " + command);
            this.send(command);
            return;
        }
        console.log("ov" + e.data);
        if(e.data.indexOf(TSC_IDENTIFIED_SENDER_ENDMARK) === 0) {
            console.log("over!");
            needTail = false;
        }
    };
    WS.prototype.onError = function (e) {
        console.log("error:" + e.error);
    };
    WS.prototype.send = function (message) {
        if(!message.length) {
            alert('Empty message not allowed !');
        } else {
            this.ws.send(message);
        }
    };
    WS.prototype.close = function () {
        console.log("close!!");
        this.ws.close();
    };
    return WS;
})();
;
function checkFile() {
    if(ssChromeClient_tailing_tab == null) {
        return;
    }
    if(!needTail) {
        return;
    }
    chrome.tabs.reload(ssChromeClient_tailing_tab.id);
    chrome.tabs.executeScript(ssChromeClient_tailing_tab.id, {
        code: 'document.body.innerText'
    }, function (result) {
        if(ssChromeClient_display_lock == true) {
            return;
        }
        if(ssChromeClient_current_text !== null) {
            ssChromeClient_current_text = result[0].substr(ssChromeClient_read_position);
        } else {
            ssChromeClient_current_text = '';
        }
        ssChromeClient_read_position = result[0].length;
        if(ssChromeClient_current_text == '') {
            return;
        }
        chrome.windows.getAll(function (windows) {
            for(var i = 0; i < windows.length; i++) {
            }
        });
    });
}
