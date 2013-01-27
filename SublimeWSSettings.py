#version 0.0.1


#Protocole version	see-> http://tools.ietf.org/html/rfc6455
VERSION = 13

#Operation codes
OP_CONTINUATION = 0x0
OP_TEXT = 0x1
OP_BINARY = 0x2
OP_CLOSE = 0x8
OP_PING = 0x9
OP_PONG = 0xA

OPCODES = (OP_CONTINUATION, OP_TEXT, OP_BINARY, OP_CLOSE, OP_PING, OP_PONG)


#API for Input to ST2 through WebSocket
API_DEFINE_DELIM = "@"
API_PREFIX = "sublimesocket"
API_INPUTIDENTITY = "inputIndetity:"


#API for Oputput from ST2 through WebSocket
API_KILLKEY = "killkey:"



#Closing frame status codes.
NORMAL_CLOSURE =  1000 # \x03\xe8
ENDPOINT_IS_GOING_AWAY =  1001 # \x03\xe9
PROTOCOL_ERROR =  1002 # \x03\xea
UNSUPPORTED_DATA_TYPE =  1003 # \x03\xeb
# NOT_AVAILABLE = 1005
# ABNORMAL_CLOSED = 1006
INVALID_PAYLOAD =  1007 # \x03\xef - INCONSISTENT DATA/TYPE
POLICY_VIOLATION =  1008 # \x03\xf0
MESSAGE_TOO_BIG =  1009 # \x03\xf1
EXTENSION_NOT_FOUND_ON_SERVER =  1010 # \x03\xf2
UNEXPECTED_CONDITION_ENCOUTERED_ON_SERVER =  1011 # \x03\xf3
# TLS_HANDSHAKE_ERROR = 1015

CLOSING_CODES = (NORMAL_CLOSURE, ENDPOINT_IS_GOING_AWAY, PROTOCOL_ERROR, UNSUPPORTED_DATA_TYPE, INVALID_PAYLOAD, POLICY_VIOLATION, MESSAGE_TOO_BIG, EXTENSION_NOT_FOUND_ON_SERVER, UNEXPECTED_CONDITION_ENCOUTERED_ON_SERVER)

# instant client-html for control SublimeSocket via WebSocket
PREFERENCE_HTML = """<!DOCTYPE html>
<html lang="fr" xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>SublimeSocket Preferences</title>
    <meta charset="UTF-8" />
    <script type="text/javascript">

      //generage uuid for SublimeSocket api
      var uuid = (function(){
          var S4 = function() {
              return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
          }   
          return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4() +S4());
      })();
      
      var _WS = {

        //websoket port (will be replaced by SublimeSocket plugin)
        uri: 'ws://SUBLIME_HOST:SUBLIME_PORT/',
        
        ws: null,

        init : function (e) {
          _WS.s = new WebSocket(_WS.uri);
          _WS.s.onopen = function (e) { _WS.onOpen(e); };
          _WS.s.onclose = function (e) { _WS.onClose(e); };
          _WS.s.onmessage = function (e) { _WS.onMessage(e); };
          _WS.s.onerror = function (e) { _WS.onError(e); };
        },

        onOpen: function () {
          _WS.write('CONNECTED');

          //call api then get callback
          _WS.s.send('sublimesocket@inputIdentity:{\"id\":\"'+uuid+'\"}');
        },

        onClose: function () {
          _WS.write('DISCONNECTED');
        },

        onMessage: function (e) {
          window.alert("received e = "+e.data);
          // if (e.data) 
          var p = document.createElement('p');
          p.innerHTML = "killsign";
          document.getElementById('kill').appendChild(p);

          _WS.write('<span style="color: blue;">RESPONSE: ' + e.data+'</span>');
        },

        onError: function (e) {
          _WS.write('<span style="color: red;">ERROR:</span> ' + e.data);
        },


        //Methods
        /*
        write textlist
        */
        write: function (message) {
            var p = document.createElement('p');
            p.style.wordWrap = 'break-word';
            p.innerHTML = message.toString();
            document.getElementById('output').appendChild(p);
        },
        send: function (message) {
          if (!message.length) {
            alert('Empty message not allowed !');
          } else {
            _WS.write('SEND: ' + message);
            _WS.s.send(message);
          }
        },
        close: function () {
          _WS.write('GOODBYE !');
          _WS.s.close();
        }
      };

      window.addEventListener('load', _WS.init, false);

    </script>
  </head>

  <body>
    <h2>SublimeSocket Preferences</h2>
    <input type="text" id="input" name="input" value="" />
    &nbsp;
    <div id="kill" style="max-height:40px;overflow:auto"></div>
    &nbsp;
    <input type="button" value="Send"  onclick="_WS.send(document.getElementById('input').value);"/>
    &nbsp;
    <input type="button" value="Close"  onclick="_WS.close();"/>
    &nbsp;
    <input type="button" value="Kill"  onclick="_WS.send(document.getElementById('kill').innerHTML);"/>
    <br/>
    <div id="output" style="max-height:300px;overflow:auto"></div>
  </body>
</html>
"""