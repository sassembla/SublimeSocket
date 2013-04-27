var currentTab = null;
var mrubyC;
chrome.browserAction.setIcon({
    path: "images/sublimesocketchromeicon-inactive.png"
});
chrome.browserAction.onClicked.addListener(function (tab) {
    if(currentTab === null && tab.url.indexOf('file://') == 0) {
        currentTab = tab;
        chrome.browserAction.setIcon({
            path: "images/sublimesocketchromeicon-active.png"
        });
        mrubyC = new mrubyClientDelegate(tab);
    } else {
        chrome.browserAction.setIcon({
            path: "images/sublimesocketchromeicon-inactive.png"
        });
        if(mrubyC) {
            mrubyC.close();
        } else {
            console.log("no instance");
        }
    }
});
