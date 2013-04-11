var ExtensionDelegate = (function () {
    function ExtensionDelegate(tab) {
        this.currentTargetFolderPath = "";
        this.currentCompilationLogFileName = "defaultLogFileName";
        this.beforeConstruct();
        var logPath = tab.url.replace("file:///", "/");
        var pathArray = logPath.split("/");
        this.currentCompilationLogFileName = pathArray[pathArray.length - 1];
        this.currentTargetFolderPath = logPath.replace("/" + this.currentCompilationLogFileName, "/");
        this.websocketCont = new WSController();
        this.websocketCont.connect(this);
        this.tail = new TailMachine(this, tab, this.tailed);
        this.afterConstruct();
    }
    ExtensionDelegate.prototype.beforeConstruct = function () {
    };
    ExtensionDelegate.prototype.afterConstruct = function () {
    };
    ExtensionDelegate.prototype.onOpen = function (delegate, e) {
    };
    ExtensionDelegate.prototype.onClose = function (delegate, e) {
    };
    ExtensionDelegate.prototype.onMessage = function (delegate, e) {
    };
    ExtensionDelegate.prototype.onError = function (delegate, e) {
    };
    ExtensionDelegate.prototype.send = function (message) {
        this.websocketCont.send(message);
    };
    ExtensionDelegate.prototype.tailed = function (delegate, text) {
    };
    ExtensionDelegate.prototype.lock = function () {
        this.tail.lock();
    };
    ExtensionDelegate.prototype.unlock = function () {
        this.tail.unlock();
    };
    ExtensionDelegate.prototype.isLocked = function () {
        return this.tail.lockKey;
    };
    ExtensionDelegate.prototype.close = function () {
        this.websocketCont.close();
        this.tail.killInterval();
    };
    return ExtensionDelegate;
})();
