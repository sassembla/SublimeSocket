var __extends = this.__extends || function (d, b) {
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
var currentFilterName = "typescript";
var CURRENT_SETTING_PATH = "SUBLIMESOCKET_PATH:tool/chromeClients/TypeScriptClient/TypeScriptFilter.txt";
var TSC_SIMPLE_COMPILE_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClients/TypeScriptClient/tscshell.sh";
var TSC_RECURSIVE_COMPILE_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClients/TypeScriptClient/tscshell.sh";
var TSC_TYPESCRIPTFILE_WILDCARD = "*.ts";
var TARGET_FOCUSED = 0;
var TARGET_FOLDER = 1;
var TARGET_RECURSIVE = 2;
var TSC_COMPILATIONTARGETMODE = TARGET_FOLDER;
var TSC_CHECKVERSIONRESULT = "API VERIFIED:";
var TSC_IDENTIFIED_SENDER_STARTMARK = "typescriptsaved";
var TSC_IDENTIFIED_SENDER_ENDMARK = "typescriptcompilefinished";
var TypeScriptClientDelegate = (function (_super) {
    __extends(TypeScriptClientDelegate, _super);
    function TypeScriptClientDelegate(tab) {
        _super.call(this, tab);
    }
    TypeScriptClientDelegate.prototype.onOpen = function (delegate, e) {
        delegate.send("ss@runSetting:" + JSON.stringify({
            "path": CURRENT_SETTING_PATH
        }));
    };
    TypeScriptClientDelegate.prototype.onMessage = function (delegate, e) {
        if(e.data.indexOf(TSC_CHECKVERSIONRESULT) === 0) {
            console.log("checkVersion result:   " + e.data);
            return;
        }
        if(e.data.indexOf(TSC_IDENTIFIED_SENDER_STARTMARK) === 0) {
            if(!delegate.isLocked()) {
                delegate.unlock();
            } else {
                return;
            }
            console.log("compile start");
            var currentCompileTargetFileName = e.data.replace(TSC_IDENTIFIED_SENDER_STARTMARK + ":", "");
            if(currentCompileTargetFileName.indexOf(this.currentTargetFolderPath) !== -1) {
            } else {
                return;
            }
            var runShellJSON;
            switch(TSC_COMPILATIONTARGETMODE) {
                case TARGET_FOCUSED:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "": [
                            TSC_SIMPLE_COMPILE_SHELLPATH, 
                            currentCompileTargetFileName, 
                            this.currentTargetFolderPath + this.currentCompilationLogFileName
                        ]
                    };
                    break;
                case TARGET_FOLDER:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "": [
                            TSC_SIMPLE_COMPILE_SHELLPATH, 
                            this.currentTargetFolderPath + TSC_TYPESCRIPTFILE_WILDCARD, 
                            this.currentTargetFolderPath + this.currentCompilationLogFileName
                        ]
                    };
                    break;
                case TARGET_RECURSIVE:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "": [
                            TSC_RECURSIVE_COMPILE_SHELLPATH, 
                            this.currentTargetFolderPath + TSC_TYPESCRIPTFILE_WILDCARD, 
                            this.currentTargetFolderPath + this.currentCompilationLogFileName
                        ]
                    };
                    break;
            }
            var command = "ss@runShell:" + JSON.stringify(runShellJSON);
            delegate.send(command);
            return;
        }
        if(e.data.indexOf(TSC_IDENTIFIED_SENDER_ENDMARK) === 0) {
            console.log("compiled");
            delegate.lock();
            return;
        }
    };
    TypeScriptClientDelegate.prototype.tailed = function (delegate, text) {
        console.log("result:" + text);
        var lines = text.split("\n");
        for(var i = 0; i < lines.length; i++) {
            var filteringJSON = {
                "name": currentFilterName,
                "source": lines[i]
            };
            if(lines[i] != '') {
                delegate.send("ss@filtering:" + JSON.stringify(filteringJSON));
            }
        }
    };
    return TypeScriptClientDelegate;
})(ExtensionDelegate);
