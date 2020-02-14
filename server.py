import socket
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result


s = socket.socket()
host = "192.168.56.1"
port = 8080
s.connect((host,port))
#s._check_sendfile_params
print("Connected on port {}".format(port))

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

s = socket.socket()
host = "192.168.56.1"
port = 8081
s.bind((host,port))
s.listen(1)
print("Waiting for any incoming connections ... ")
conn, addr = s.accept()
print(addr, "Has connected to the server")
x = 7
img_rgb = cv2.imread('source.png')
for n in range(x):
    i = (360 / x) * n

   
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('pattern.png',0)
    #template = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)
    template = rotateImage(template, i)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.85
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
    cv2.imwrite('res.png',img_rgb)
    img_rgb = cv2.imread('res.png')
    txt = "Wykonano {}".format((n+1)/x * 100) 
    to_send = round((n+1)/x * 100)
    txt = "{}".format(to_send)
    conn.send(txt.encode())   
    #txt = "Wykonano {} %".format(n)
    print(to_send)
    






filename = "D:\Dokumenty/testy/odbiorca/res.png"
size = os.path.getsize(filename)
file = open(filename , 'rb')
file_data = file.read(size)
#print(size)
conn.send(file_data)
print("Final image has been transmitted successfully")