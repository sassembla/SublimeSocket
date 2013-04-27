/**
    Extension's main delegate class.
    this is base class for extension delegate.


    WSController:
        websocket instance. override below.
            "onOpen (delegate:ExtensionDelegate, e)" ,
            "onClose (delegate:ExtensionDelegate, e)" ,
            "onMessage (delegate:ExtensionDelegate, e)" ,
            "onError (delegate:ExtensionDelegate, e)" ,

    TailMachine:
        tail specific tab's file & emit "tail (delegate:ExtensionDelegate, text:string)" when tailed.


    send (message:string) : 
        send message to SublimeSocket.

    lock () : 
        lock tail movement. will be ignored when tail stopped already.

    unlock () : 
        unlock tail movement. will be ignored when tail running already.

*/

class ExtensionDelegate {

    private websocketCont:WSController;
    private tail:TailMachine;

    public currentTargetFolderPath = "";
    public currentCompilationLogFileName = "defaultLogFileName";
    

    constructor (tab) {
        this.beforeConstruct();

        // replace file path as FileSystem path
        var logPath = tab.url.replace("file:///", "/");

        var pathArray = logPath.split("/");

        // last path is "logfile.log"
        this.currentCompilationLogFileName = pathArray[pathArray.length-1];
        
        // get FolderPath
        this.currentTargetFolderPath = logPath.replace("/"+this.currentCompilationLogFileName, "/");
        
        // WebSocket
        this.websocketCont = new WSController();
        this.websocketCont.connect(this);

        // generate tail
        this.tail = new TailMachine(this, tab, this.tailed);

        this.afterConstruct();
    }

    beforeConstruct () {}

    afterConstruct () {}

    onOpen (delegate:ExtensionDelegate, e) {}

    onClose (delegate:ExtensionDelegate, e) {}

    onMessage (delegate:ExtensionDelegate, e) {}

    onError (delegate:ExtensionDelegate, e) {}


    send (message:string) {
        this.websocketCont.send(message);
    }

    tailed (delegate:ExtensionDelegate, text:string) {}

    lock () {
        this.tail.lock();
    }

    unlock () {
        this.tail.unlock();
    }

    isLocked () {
        return this.tail.lockKey;    
    }
    
    close () {
        this.websocketCont.close();
        this.tail.killInterval();
    }
}

