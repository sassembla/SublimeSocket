var __extends = this.__extends || function (d, b) {
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
var currentFilterName = "mruby";
var mrbcPath = "/Users/sassembla/test/mruby/bin/mrbc";
var mrubyPath = "/Users/sassembla/test/mruby/bin/mruby";
var MODE_MRBC = 0;
var MODE_MRUBY = 1;
var MRB_RUN_MODE = MODE_MRUBY;
var CURRENT_SETTING_PATH = "SUBLIMESOCKET_PATH:tool/chromeClients/MrubyClient/mrubyFilter.txt";
var MRB_CONVERT_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClients/MrubyClient/mrubyconv.sh";
var MRB_MRUBY_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClients/MrubyClient/mruby.sh";
var TSC_TYPESCRIPTFILE_WILDCARD = "*.rb";
var TARGET_FOCUSED = 0;
var TARGET_FOLDER = 1;
var TSC_COMPILATIONTARGETMODE = TARGET_FOLDER;
var TSC_CHECKVERSIONRESULT = "API VERIFIED:";
var TSC_IDENTIFIED_SENDER_STARTMARK = "mrubysaved";
var TSC_IDENTIFIED_SENDER_ENDMARK = "mrubyfinished";
var MrubyClientDelegate = (function (_super) {
    __extends(MrubyClientDelegate, _super);
    function MrubyClientDelegate(tab) {
        _super.call(this, tab);
    }
    MrubyClientDelegate.prototype.onOpen = function (delegate, e) {
        delegate.send("ss@runSetting:" + JSON.stringify({
            "path": CURRENT_SETTING_PATH
        }));
    };
    MrubyClientDelegate.prototype.onMessage = function (delegate, e) {
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
            var runTargetShell;
            var runTargetCommandPath;
            switch(MRB_RUN_MODE) {
                case MODE_MRBC:
                    runTargetShell = MRB_CONVERT_SHELLPATH;
                    runTargetCommandPath = mrbcPath;
                    break;
                case MODE_MRUBY:
                    runTargetShell = MRB_MRUBY_SHELLPATH;
                    runTargetCommandPath = mrubyPath;
                    break;
            }
            var runShellJSON;
            switch(TSC_COMPILATIONTARGETMODE) {
                case TARGET_FOCUSED:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "": [
                            runTargetShell, 
                            runTargetCommandPath, 
                            currentCompileTargetFileName, 
                            this.currentTargetFolderPath + this.currentCompilationLogFileName
                        ],
                        "debug": true
                    };
                    break;
                case TARGET_FOLDER:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "": [
                            runTargetShell, 
                            runTargetCommandPath, 
                            this.currentTargetFolderPath + TSC_TYPESCRIPTFILE_WILDCARD, 
                            this.currentTargetFolderPath + this.currentCompilationLogFileName
                        ],
                        "debug": true
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
    MrubyClientDelegate.prototype.tailed = function (delegate, text) {
        console.log("result:" + text);
        var lines = text.split("\n");
        for(var i = 0; i < lines.length; i++) {
            var line = lines[i].replace(/"/g, "_");
            var filteringJSON = {
                "name": currentFilterName,
                "source": line,
                "debug":true
            };
            if(lines[i] != '') {
                delegate.send("ss@filtering:" + JSON.stringify(filteringJSON));
            }
        }
    };
    return MrubyClientDelegate;
})(ExtensionDelegate);
