var __extends = this.__extends || function (d, b) {
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
var currentFilterName = "scala";
var CURRENT_SETTING_PATH = "SUBLIMESOCKET_PATH:tool/chromeClients/ScalaClient/ScalaFilter.txt";
var SCALA_GRADLE_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClients/ScalaClient/scalaShell.sh";
var TSC_CHECKVERSIONRESULT = "API VERIFIED:";
var SCALAC_IDENTIFIED_SENDER_STARTMARK = "scalasaved";
var SCALAC_IDENTIFIED_SENDER_ENDMARK = "scalacompilefinished";
var ScalaClientDelegate = (function (_super) {
    __extends(ScalaClientDelegate, _super);
    function ScalaClientDelegate(tab) {
        _super.call(this, tab);
    }
    ScalaClientDelegate.prototype.onOpen = function (delegate, e) {
        delegate.send("ss@runSetting:" + JSON.stringify({
            "path": CURRENT_SETTING_PATH
        }));
    };
    ScalaClientDelegate.prototype.onMessage = function (delegate, e) {
        if(e.data.indexOf(TSC_CHECKVERSIONRESULT) === 0) {
            console.log("checkVersion result:   " + e.data);
            return;
        }
        if(e.data.indexOf(SCALAC_IDENTIFIED_SENDER_STARTMARK) === 0) {
            if(!delegate.isLocked()) {
                delegate.unlock();
            } else {
                return;
            }
            console.log("compile start");
            var currentCompileTargetFileName = e.data.replace(SCALAC_IDENTIFIED_SENDER_STARTMARK + ":", "");
            if(currentCompileTargetFileName.indexOf(this.currentTargetFolderPath) !== -1) {
            } else {
                return;
            }
            console.log("SCALA_GRADLE_SHELLPATH" + SCALA_GRADLE_SHELLPATH);
            var runShellJSON = {
                "main": "/bin/sh",
                "": [
                    SCALA_GRADLE_SHELLPATH, 
                    this.currentTargetFolderPath, 
                    this.currentTargetFolderPath + this.currentCompilationLogFileName
                ]
            };
            var command = "ss@runShell:" + JSON.stringify(runShellJSON);
            delegate.send(command);
            return;
        }
        if(e.data.indexOf(SCALAC_IDENTIFIED_SENDER_ENDMARK) === 0) {
            console.log("compiled");
            delegate.lock();
            return;
        }
    };
    ScalaClientDelegate.prototype.tailed = function (delegate, text) {
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
    return ScalaClientDelegate;
})(ExtensionDelegate);
