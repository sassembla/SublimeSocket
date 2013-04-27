var currentTab = null;
var mrubyDel;
chrome.browserAction.setIcon({
    path: "images/sublimesocketchromeicon-inactive.png"
});
chrome.browserAction.onClicked.addListener(function (tab) {
    if(currentTab === null && tab.url.indexOf('file://') == 0) {
        currentTab = tab;
        chrome.browserAction.setIcon({
            path: "images/sublimesocketchromeicon-active.png"
        });
        mrubyDel = new MrubyClientDelegate(tab);
    } else {
        chrome.browserAction.setIcon({
            path: "images/sublimesocketchromeicon-inactive.png"
        });
        if(mrubyDel) {
            mrubyDel.close();
        } else {
            console.log("no instance");
        }
    }
});
