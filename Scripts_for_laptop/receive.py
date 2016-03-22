import os
import cv2
import time
import numpy as np
import csv 
import socket

print "Started..."

resolution_x = 150  
resolution_y = 75

csvfile = open('ImageCommand.csv', 'ab') 
writer = csv.writer(csvfile, delimiter='#',quotechar='|', quoting=csv.QUOTE_MINIMAL)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(),10000))
serverSocket.listen(1)


while(True):
    clientSocket, addr = serverSocket.accept()
    print "Car connected..."

    while(True):
        data=''
        while(len(data)<resolution_x*resolution_y):
            data += clientSocket.recv(10000)
        img = np.fromstring(data, dtype = 'uint8').reshape(resolution_y, resolution_x)

        print "Received image."
        cv2.imshow("image",img)
        k = cv2.waitKey(0)
        command = '0'

        if k & 0xFF == ord('w'):
            command = '0'
        elif k & 0xFF == ord('s'):
            command = '1'
        elif k & 0xFF == ord('a'):
            command = '2'
        elif k & 0xFF == ord('d'):
            command = '3'
        elif k & 0xFF == ord('q'):
            command = '-1'
            exit(0)
        else:
            command = '-1'

        if command != '-1' :
            writer.writerow([list(img.ravel()), command])
            csvfile.flush()

        clientSocket.send(command)
        #os.remove('image.jpg')
        #os.system('scp result.txt pi@192.168.1.1:/home/pi/Documents/Scripts/AutonomousCar/')
        print "Sent command word.\n"

serverSocket.close()
