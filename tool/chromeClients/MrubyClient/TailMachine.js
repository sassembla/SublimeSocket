var TailMachine = (function () {
    function TailMachine(delegate, currentTargetTab, currentTimerFunc) {
        var _this = this;
        this.interval = 500;
        this.readPosition = 0;
        this.lockKey = false;
        this.targetTab = currentTargetTab;
        this.intervalInstance = setInterval(function () {
            _this.runInterval(_this);
        }, this.interval);
        this.delegate = delegate;
        this.timerFunc = currentTimerFunc;
    }
    TailMachine.prototype.intervalExecute = function (text) {
        console.log("this.timerFunc is " + this.timerFunc);
        this.timerFunc(this.delegate, text);
    };
    TailMachine.prototype.unlock = function () {
        this.lockKey = true;
    };
    TailMachine.prototype.lock = function () {
        this.lockKey = false;
    };
    TailMachine.prototype.killInterval = function () {
        clearInterval(this.intervalInstance);
        this.targetTab = null;
    };
    TailMachine.prototype.runInterval = function (self) {
        if(self.targetTab == null) {
            return;
        }
        if(!self.lockKey) {
            return;
        }
        chrome.tabs.reload(self.targetTab.id);
        chrome.tabs.executeScript(self.targetTab.id, {
            code: 'document.body.innerText'
        }, function (result) {
            if(self.readPosition == -1) {
                self.readPosition = 0;
            }
            if(self.readPosition < result[0].length) {
            } else {
                return;
            }
            var text = result[0].substr(self.readPosition);
            self.readPosition = result[0].length;
            if(text == '') {
                return;
            }
            self.intervalExecute(text);
        });
    };
    return TailMachine;
})();
