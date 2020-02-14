import socket
import os
import cv2
import numpy as np
import time
from matplotlib import pyplot as plt

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

while 1:
  sc = socket.socket()
  host = "127.0.0.1"
  port = 8080
  sc.bind((host,port))
  sc.listen(1)
  print(host)
  print("Waiting for any incoming connections ... ")
  s, addr = sc.accept()
  print(addr, "Has connected to the server")



  filename = "D:\Dokumenty/testy/odbiorca/source.png"

  file = open(filename, 'wb')
  file_data = s.recv(100000)
  file.write(file_data)
  file.close()
  print("Source has been received successfully.")

  filename = "D:\Dokumenty/testy/odbiorca/pattern.png"

  file = open(filename, 'wb')
  file_data = s.recv(100000)
  file.write(file_data)
  file.close()
  print("Pattern has been received successfully.")

  #Calculating best pattern equivalents in source image for each rotation
  x = 7
  img_rgb = cv2.imread("D:\Dokumenty/testy/odbiorca/source.png")
  for n in range(x):
      i = (360 / x) * n  
      img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
      template = cv2.imread("D:\Dokumenty/testy/odbiorca/pattern.png",0)
      template = rotateImage(template, i)
      w, h = template.shape[::-1]

      res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
      threshold = 0.85
      loc = np.where( res >= threshold)
      for pt in zip(*loc[::-1]):
          cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
      cv2.imwrite("D:\Dokumenty/testy/odbiorca/res.png",img_rgb)
      img_rgb = cv2.imread("D:\Dokumenty/testy/odbiorca/res.png")
      txt = "Wykonano {}".format((n+1)/x * 100) 
      to_send = round((n+1)/x * 100)
      txt = "{}".format(to_send)
      s.send(txt.encode())
      print(to_send)   

#Sending final image
  filename = "D:\Dokumenty/testy/odbiorca/res.png"
  size = os.path.getsize(filename)
  file = open(filename , 'rb')
  file_data = file.read(size)
  print(size)
  s.send(file_data)
  print("Final image has been transmitted successfully")