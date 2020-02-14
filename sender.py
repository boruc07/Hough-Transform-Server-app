import socket
import os

conn = socket.socket()
host = "127.0.0.1"
port = 8080
conn.connect((host,port))
print("Connected on port {}".format(port))

#sending source image
filename = "D:\Dokumenty/testy/serwer/flames.png"
size = os.path.getsize(filename)
print (size)
file = open(filename , 'rb')
file_data = file.read(size)
conn.send(file_data)
print("Source image has been transmitted successfully")

#sending pattern image
filename = "D:\Dokumenty/testy/serwer/pt.png"
size = os.path.getsize(filename)
print (size)
file = open(filename , 'rb')
file_data = file.read(size)
conn.send(file_data)
print("Pattern image has been transmitted successfully")

#Progress status
file_data = conn.recv(1000000)
file_data = file_data.decode()
i = 0    
while file_data != "100":        
    print("{}% Progress".format(file_data))
    file_data = conn.recv(100000)
    file_data = file_data.decode()
    i = i+1
print("100% Progress")

#Reciving final image
filename = "D:\Dokumenty/testy/serwer/rev.png"
file = open(filename, 'wb')
file_data = conn.recv(1000000)
file.write(file_data)
file.close()
print("Final image has been received successfully.")