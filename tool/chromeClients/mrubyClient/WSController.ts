
/*
    control WebSocket.
    connect target uri is fixed as SublimeSocket's default.
*/
class WSController {
    public uri = 'ws://127.0.0.1:8823/';

    public ws:WebSocket;

    connect (delegate:ExtensionDelegate) {
      this.ws = new WebSocket(this.uri);
      this.ws.onopen = function (e) => delegate.onOpen(delegate, e);
      this.ws.onclose = function (e) => delegate.onClose(delegate, e);
      this.ws.onmessage = function (e) => delegate.onMessage(delegate, e);
      this.ws.onerror = function (e) => delegate.onError(delegate, e);
    }
    
    send (message:string) {
        this.ws.send(message);
    }

    close () {
        this.ws.close();
    }
}