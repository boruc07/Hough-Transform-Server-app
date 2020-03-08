from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory
import base64
import os
import cv2
import numpy as np

def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

class MyServerProtocol(WebSocketServerProtocol):
   i = 0
   x = 8
   def onConnect(self, request):
      print("Client connecting: {0}".format(request.peer))

   def onOpen(self):
      print("WebSocket connection open.")

   def onMessage(self, payload, isBinary):
      MyServerProtocol.i = MyServerProtocol.i+1
      print(MyServerProtocol.i)
      if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
      else:
            print("Text message received, saving to a file")
            # decode the image and save locally
            path = "D:\Dokumenty/testy/serwer/image_received{}.png".format(MyServerProtocol.i)
            with open(path, "wb") as image_file:
                image_file.write(base64.b64decode(payload.decode().split('base64,')[1]))
      if (MyServerProtocol.i == 2):
          print("I am calculating x = {} and i = {}".format(MyServerProtocol.x,MyServerProtocol.i))
          img_rgb = cv2.imread("D:\Dokumenty/testy/serwer/image_received2.png")
         
          for n in range(MyServerProtocol.x):
                MyServerProtocol.i = (360 / MyServerProtocol.x) * n  
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                template = cv2.imread("D:\Dokumenty/testy/serwer/image_received1.png",0)
                template = rotateImage(template, MyServerProtocol.i)
                w, h = template.shape[::-1]

                res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                threshold = 0.85
                loc = np.where( res >= threshold)
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
                cv2.imwrite("D:\Dokumenty/testy/serwer/res.png",img_rgb)
                #res = cv2.normalize(res,  res, 0, 255, cv2.NORM_MINMAX)
                #path = "D:\Dokumenty/testy/odbiorca/acumulators/acc{}.png".format(i)
                #cv2.imwrite(path,res)
                img_rgb = cv2.imread("D:\Dokumenty/testy/serwer/res.png")
                txt = "Wykonano {}".format((n+1)/MyServerProtocol.x * 100) 
                to_send = round((n+1)/MyServerProtocol.x * 100)
                txt = "{}".format(to_send)
                #s.send(txt.encode())
                #self.sendMessage(base64.b64encode(txt.encode()), isBinary= True)
                print(to_send)
                
          #res = cv2.normalize(res,  res, 0, 255, cv2.NORM_MINMAX)
          #cv2.imwrite("D:\Dokumenty/testy/serwer/acc.png",res)
          #Sending final image
          filename = "D:\Dokumenty/testy/serwer/res.png"
          size = os.path.getsize(filename)
          file = open(filename , 'rb')
          file_data = file.read(size)  
          self.sendMessage(("data:image/png;base64," + base64.b64encode(file_data).decode()).encode(), isBinary= False)
          MyServerProtocol.i = 0
     

   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {0}".format(reason))



if __name__ == '__main__':

   import sys
   from twisted.python import log
   from twisted.internet import reactor

   log.startLogging(sys.stdout)

   factory = WebSocketServerFactory("ws://192.168.0.107:9000")#192.168.56.1
   factory.protocol = MyServerProtocol

   reactor.listenTCP(9000, factory)
   reactor.run()