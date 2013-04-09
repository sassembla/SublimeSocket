class WS {

    public uri = 'ws://127.0.0.1:8823/';
    public currentTargetFolderPath = "";
    public currentCompilationTargetMode = -1;
    public currentTSCompileLogFileName = "defaultLogFileName";
    public ws:WebSocket;


    init (targetLogPath:string, compilationTargetMode) {

        // replace file path as FileSystem path
        var logPath = targetLogPath.replace("file:///", "/");

        var pathArray = logPath.split("/");

        // last path is "logfile.log"
        this.currentTSCompileLogFileName = pathArray[pathArray.length-1];
        
        // get FolderPath
        this.currentTargetFolderPath = logPath.replace("/"+this.currentTSCompileLogFileName, "/");
        console.log("currentTargetFolderPath    "+this.currentTargetFolderPath);

        // set mode from preferences
        this.currentCompilationTargetMode = compilationTargetMode;
    }

    connect () {
      this.ws = new WebSocket(this.uri);
      this.ws.onopen = function (e) => this.onOpen(e);
      this.ws.onclose = function (e) => this.onClose(e);
      this.ws.onmessage = function (e) => this.onMessage(e);
      this.ws.onerror = function (e) => this.onError(e);
    }

    onOpen (e) {
        this.send("ss@runSetting:"+JSON.stringify({"path":CURRENT_SETTING_PATH}));
    }

    onClose (e) {
        console.log("closed!!? closed nande!?"+e);
    }

    onMessage (e) {
        if (e.data.indexOf(TSC_CHECKVERSIONRESULT) === 0) {
            console.log("checkVersion result:   "+e.data);
            return;
        }

        if (e.data.indexOf(TSC_IDENTIFIED_SENDER_STARTMARK) === 0) {
            console.log("save");
            var currentCompileTargetFileName = e.data.replace(TSC_IDENTIFIED_SENDER_STARTMARK+":","")
            if (currentCompileTargetFileName.indexOf(this.currentTargetFolderPath) !== -1) {
                // exist in target folder.
            } else {
                return;
            }

            var runShellJSON;

            switch (this.currentCompilationTargetMode) {
                case TARGET_FOCUSED:
                    
                    runShellJSON = {
                        "main": "/bin/sh",
                        "":[
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
                        ]
                    };

                    break;
                case TARGET_RECURSIVE:
                    runShellJSON = {
                        "main": "/bin/sh",
                        "":[
                            TSC_RECURSIVE_COMPILE_SHELLPATH,
                            this.currentTargetFolderPath + TSC_TYPESCRIPTFILE_WILDCARD,
                            this.currentTargetFolderPath + this.currentTSCompileLogFileName
                        ]
                    };
                    break;
            } 

            needTail = true;
            
            var command = "ss@runShell:"+JSON.stringify(runShellJSON);

            console.log("TARGET_FOLDER here command "+command);

            this.send(command);
            return;
        }
        
        if (e.data.indexOf(TSC_IDENTIFIED_SENDER_ENDMARK) === 0) {
            needTail = false;
            return;
        }

        // 

    }

    onError (e) {
        console.log("error:"+e.error);
    }


    send (message:string) {
        if (!message.length) {
            alert('Empty message not allowed !');
        } else {
            this.ws.send(message);
        }
    }

    close () {
        console.log("close!!");
        this.ws.close();
    }
};