/**
	Chrome Extension's event start point
*/

var currentTab = null;

declare var chrome;
var tsDel:TypeScriptClientDelegate;

// default is inactive
chrome.browserAction.setIcon({path:"images/sublimesocketchromeicon-inactive.png"});

chrome.browserAction.onClicked.addListener(function(tab) {
    if (currentTab === null && tab.url.indexOf('file://') == 0) {
        // keep tab instance for check if runnning or not
        currentTab = tab;

        chrome.browserAction.setIcon({path:"images/sublimesocketchromeicon-active.png"});

        // generate ExtensionDelegate
        tsDel = new TypeScriptClientDelegate(tab);

    }else{
        chrome.browserAction.setIcon({path:"images/sublimesocketchromeicon-inactive.png"});
        
        if (tsDel) tsDel.close();
        else console.log("no instance");
    }
})