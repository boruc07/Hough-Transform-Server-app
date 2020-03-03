from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

# import the base64 module
import base64

class MyServerProtocol(WebSocketServerProtocol):
   i = 0 
   def onConnect(self, request):
      print("Client connecting: {0}".format(request.peer))

   def onOpen(self):
      print("WebSocket connection open.")

   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {0} bytes".format(len(payload)))
         print(payload.decode())
      else:
         print("Text message received, saving to a file")         
         print(payload.decode())
        

      # echo back message verbatim
      self.sendMessage(payload, isBinary)

   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {0}".format(reason))



if __name__ == '__main__':

   import sys
   from twisted.python import log
   from twisted.internet import reactor

   log.startLogging(sys.stdout)

   factory = WebSocketServerFactory("ws://localhost:9000")
   factory.protocol = MyServerProtocol

   reactor.listenTCP(9000, factory)
   reactor.run()