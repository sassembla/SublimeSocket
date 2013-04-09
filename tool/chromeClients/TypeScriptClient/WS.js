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
                        ]
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
                        ]
                    };
                    break;
            }
            needTail = true;
            var command = "ss@runShell:" + JSON.stringify(runShellJSON);
            console.log("TARGET_FOLDER here command " + command);
            this.send(command);
            return;
        }
        if(e.data.indexOf(TSC_IDENTIFIED_SENDER_ENDMARK) === 0) {
            needTail = false;
            return;
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
