import socket
import os


while 1:

    s = socket.socket()
    host = "192.168.56.1"
    port = 8080
    s.bind((host,port))
    s.listen(1)

    print(host)
    print("Waiting for any incoming connections ... ")
    conn, addr = s.accept()
    print(addr, "Has connected to the server")
 
    filename = "D:\Dokumenty/testy/serwer/flames.png"
    size = os.path.getsize(filename)
    #print (size)
    file = open(filename , 'rb')
    file_data = file.read(size)
    conn.send(file_data)
    print("Source image has been transmitted successfully")

    filename = "D:\Dokumenty/testy/serwer/pt.png"
    size = os.path.getsize(filename)
   # print (size)
    file = open(filename , 'rb')
    file_data = file.read(size)
    conn.send(file_data)
    print("Pattern image has been transmitted successfully")

    


    sc = socket.socket()
    host = "192.168.56.1"
    port = 8081
    
    sc.connect((host,port))
    #s._check_sendfile_params
    print("Connected on port {}".format(port))
    file_data = sc.recv(1000000)
    file_data = file_data.decode()
    i = 0    
    while file_data != "100":        
        print("{}% Progress".format(file_data))
        file_data = sc.recv(1000000)
        file_data = file_data.decode()
        i = i+1
    print("100% Progress")

    filename = "D:\Dokumenty/testy/serwer/rev.png"

    file = open(filename, 'wb')
    file_data = sc.recv(1000000)
    file.write(file_data)
    file.close()
    print("Final image has been received successfully.")