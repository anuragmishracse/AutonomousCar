from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import os
import movecar
import socket
import cv2

runtime = 0.3

resolution_x = 150
resolution_y = 75

print "Started..."

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("Anurags-MacBook-Air.local",10000))

print "Connected to Mac..."

camera = PiCamera()
#camera.hflip=True
#camera.vflip=True
camera.resolution = (resolution_x, resolution_y)
camera.framerate = 15

rawCapture = PiRGBArray(camera, size=(resolution_x, resolution_y))

time.sleep(1)

motion = movecar.MoveCar()
motion.initialize()

print "Starting the camera stream..."

for frame in camera.capture_continuous(rawCapture, format= 'bgr', use_video_port=True):
    	color_image = frame.array
    	img = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
	img = img.tostring()	
	rawCapture.truncate(0)

	length_sent  = clientSocket.send(img)

	command = clientSocket.recv(5)
	print "Decision : "+str(command)
	if(command == '0'):
		#Move forward
		motion.move_stopall()
		motion.move_forward()
		time.sleep(runtime)
		motion.move_stopall()
	elif(command == '1'):
		#Move backward
		motion.move_stopall()
		motion.move_backward()
		time.sleep(runtime)
		motion.move_stopall()
	elif(command == '2'):
		#Move left
		motion.move_left()
		motion.move_forward()
		time.sleep(runtime)
		motion.move_stopfb()
	elif(command == '3'):
		#Move right
		motion.move_right()
		motion.move_forward()
		time.sleep(runtime)
		motion.move_stopfb()
	else:
		#Do nothing
		motion.move_stopfb()
	print "Received and executed command word\n"
	
	
  
motion.close()
clientSocket.close()

