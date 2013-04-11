var currentTab = null;
var sDel;
chrome.browserAction.setIcon({
    path: "images/sublimesocketchromeicon-inactive.png"
});
chrome.browserAction.onClicked.addListener(function (tab) {
    if(currentTab === null && tab.url.indexOf('file://') == 0) {
        currentTab = tab;
        chrome.browserAction.setIcon({
            path: "images/sublimesocketchromeicon-active.png"
        });
        sDel = new ScalaClientDelegate(tab);
    } else {
        chrome.browserAction.setIcon({
            path: "images/sublimesocketchromeicon-inactive.png"
        });
        if(sDel) {
            sDel.close();
        } else {
            console.log("no instance");
        }
    }
});
