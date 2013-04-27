var WSController = (function () {
    function WSController() {
        this.uri = 'ws://127.0.0.1:8823/';
    }
    WSController.prototype.connect = function (delegate) {
        this.ws = new WebSocket(this.uri);
        this.ws.onopen = function (e) {
            return delegate.onOpen(delegate, e);
        };
        this.ws.onclose = function (e) {
            return delegate.onClose(delegate, e);
        };
        this.ws.onmessage = function (e) {
            return delegate.onMessage(delegate, e);
        };
        this.ws.onerror = function (e) {
            return delegate.onError(delegate, e);
        };
    };
    WSController.prototype.send = function (message) {
        this.ws.send(message);
    };
    WSController.prototype.close = function () {
        this.ws.close();
    };
    return WSController;
})();
