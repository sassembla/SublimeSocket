var __extends = this.__extends || function (d, b) {
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
var currentFilterName = "mruby";
var CURRENT_SETTING_PATH = "SUBLIMESOCKET_PATH:tool/chromeClients/mrubyClient/mrubyFilter.txt";
var MRB_SIMPLE_COMPILE_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClients/mrubyClient/mrubyc.sh";
var MRB_RECURSIVE_COMPILE_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClients/mrubyClient/mrubyc.sh";
var MRB_MRUBYFILE_WILDCARD = "*.rb";
var TARGET_FOCUSED = 0;
var TARGET_FOLDER = 1;
var TARGET_RECURSIVE = 2;
var MRB_COMPILATIONTARGETMODE = TARGET_FOCUSED;
var MRB_CHECKVERSIONRESULT = "API VERIFIED:";
var MRB_IDENTIFIED_SENDER_STARTMARK = "mrubysaved";
var MRB_IDENTIFIED_SENDER_ENDMARK = "mrubycompilefinished";
var mrubyClientDelegate = (function (_super) {
    __extends(mrubyClientDelegate, _super);
    function mrubyClientDelegate(tab) {
        _super.call(this, tab);
    }
    mrubyClientDelegate.prototype.onOpen = function (delegate, e) {
        delegate.send("ss@runSetting:" + JSON.stringify({
            "path": CURRENT_SETTING_PATH
        }));
    };
    mrubyClientDelegate.prototype.onMessage = function (delegate, e) {
        if(e.data.indexOf(MRB_CHECKVERSIONRESULT) === 0) {
            console.log("checkVersion result:   " + e.data);
            return;
        }
        if(e.data.indexOf(MRB_IDENTIFIED_SENDER_STARTMARK) === 0) {
            if(!delegate.isLocked()) {
                delegate.unlock();
            } else {
                return;
            }
            console.log("compile start");
            var currentCompileTargetFileName = e.data.replace(MRB_IDENTIFIED_SENDER_STARTMARK + ":", "");
            if(currentCompileTargetFileName.indexOf(this.currentTargetFolderPath) !== -1) {
            } else {
                return;
            }
            var runShellJSON;
            switch(MRB_COMPILATIONTARGETMODE) {
                case TARGET_FOCUSED:
                    console.log("MRB_SIMPLE_COMPILE_SHELLPATH	" + MRB_SIMPLE_COMPILE_SHELLPATH);
                    console.log("currentCompileTargetFileName	" + currentCompileTargetFileName);
                    console.log("this.currentTargetFolderPath + this.currentCompilationLogFileName	" + this.currentTargetFolderPath + this.currentCompilationLogFileName);
                    runShellJSON = {
                        "main": "/bin/sh",
                        "": [
                            MRB_SIMPLE_COMPILE_SHELLPATH, 
                            currentCompileTargetFileName, 
                            this.currentTargetFolderPath + this.currentCompilationLogFileName
                        ]
                    };
                    break;
                case TARGET_FOLDER:
                    console.log("MRB_SIMPLE_COMPILE_SHELLPATH	" + MRB_SIMPLE_COMPILE_SHELLPATH);
                    console.log("this.currentTargetFolderPath + MRB_MRUBYFILE_WILDCARD	" + this.currentTargetFolderPath + MRB_MRUBYFILE_WILDCARD);
                    console.log("this.currentTargetFolderPath + this.currentCompilationLogFileName	" + this.currentTargetFolderPath + this.currentCompilationLogFileName);
                    runShellJSON = {
                        "main": "/bin/sh",
                        "": [
                            MRB_SIMPLE_COMPILE_SHELLPATH, 
                            this.currentTargetFolderPath + MRB_MRUBYFILE_WILDCARD, 
                            this.currentTargetFolderPath + this.currentCompilationLogFileName
                        ]
                    };
                    break;
                case TARGET_RECURSIVE:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "": [
                            MRB_RECURSIVE_COMPILE_SHELLPATH, 
                            this.currentTargetFolderPath + MRB_MRUBYFILE_WILDCARD, 
                            this.currentTargetFolderPath + this.currentCompilationLogFileName
                        ]
                    };
                    break;
            }
            var command = "ss@runShell:" + JSON.stringify(runShellJSON);
            delegate.send(command);
            return;
        }
        if(e.data.indexOf(MRB_IDENTIFIED_SENDER_ENDMARK) === 0) {
            console.log("compiled");
            delegate.lock();
            return;
        }
    };
    mrubyClientDelegate.prototype.tailed = function (delegate, text) {
        console.log("result:" + text);
        var lines = text.split("\n");
        for(var i = 0; i < lines.length; i++) {
            var filteringJSON = {
                "name": currentFilterName,
                "source": lines[i],
                "debug": true
            };
            if(lines[i] != '') {
                console.log("sendは発生している");
                delegate.send("ss@filtering:" + JSON.stringify(filteringJSON));
            }
        }
    };
    return mrubyClientDelegate;
})(ExtensionDelegate);
