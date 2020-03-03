from autobahn.twisted.websocket import WebSocketClientProtocol, \
                                       WebSocketClientFactory

# import the base64 module
import base64

class MyClientProtocol(WebSocketClientProtocol):

   def onConnect(self, response):
      print("Server connected: {0}".format(response.peer))

   def onOpen(self):
      print("WebSocket connection open.")

      def hello():

         encoded_string = 'herrrroooo'.encode()
         # sending the encoded image         
         self.sendMessage(encoded_string)
      hello()

   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {0} bytes".format(len(payload)))
         print(payload.decode())
      else:
         # printing the size of the encoded image which is received
         print("Encoded size of the received text: {0} bytes".format(len(payload)))
         print(payload.decode())
         

   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {0}".format(reason))



if __name__ == '__main__':

   import sys

   from twisted.python import log
   from twisted.internet import reactor

   log.startLogging(sys.stdout)

   factory = WebSocketClientFactory("ws://localhost:9000")
   factory.protocol = MyClientProtocol

   reactor.connectTCP("127.0.0.1", 9000, factory)
   reactor.run()