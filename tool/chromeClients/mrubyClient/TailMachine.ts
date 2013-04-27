/**
    tail tab-opend file with intervals.
    run "currentTimerFunc" function when tail caught some lines of texts.
*/
class TailMachine {
    private interval = 500;

    private delegate:ExtensionDelegate;

	public lockKey:bool;
	private targetTab;

	private intervalInstance;
    private readPosition = -1;

    private timerFunc;

	constructor (delegate:ExtensionDelegate, currentTargetTab, currentTimerFunc) {
		this.lockKey = false;

        this.targetTab = currentTargetTab;
        
        // start timer event
        this.intervalInstance = setInterval(function () => {this.runInterval(this);}, this.interval);
        this.delegate = delegate;

        this.timerFunc = currentTimerFunc;
	}

    /**
        timer execution
    */
    intervalExecute (text:string) {
        this.timerFunc(this.delegate, text);
    }

    unlock () {
        this.lockKey = true;
    }

    lock () {
        this.lockKey = false;   
    }


    killInterval () {
        clearInterval(this.intervalInstance);
        this.targetTab = null;
    }

	runInterval(self:TailMachine) {

        if (self.targetTab == null) {
            return;
        }

        if (!self.lockKey) {
            return;
        }
        
        // reload tab. get latest fileData.
        chrome.tabs.reload(self.targetTab.id);
        
        chrome.tabs.executeScript(
            self.targetTab.id, {code:'document.body.innerText'}, function(result) {

                if (self.readPosition == -1) {
                    self.readPosition = result[0].length;
                    return;
                }

                if (self.readPosition < result[0].length) {
                    
                } else {
                    return;
                }

                var text = result[0].substr(self.readPosition);
                
                self.readPosition = result[0].length;
                if (text == '') {
                    return;
                }

                self.intervalExecute(text);

            }
        );
    }
}