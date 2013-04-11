var currentTab = null;
var tsDel;
chrome.browserAction.setIcon({
    path: "images/sublimesocketchromeicon-inactive.png"
});
chrome.browserAction.onClicked.addListener(function (tab) {
    if(currentTab === null && tab.url.indexOf('file://') == 0) {
        currentTab = tab;
        chrome.browserAction.setIcon({
            path: "images/sublimesocketchromeicon-active.png"
        });
        tsDel = new TypeScriptClientDelegate(tab);
    } else {
        chrome.browserAction.setIcon({
            path: "images/sublimesocketchromeicon-inactive.png"
        });
        if(tsDel) {
            tsDel.close();
        } else {
            console.log("no instance");
        }
    }
});
