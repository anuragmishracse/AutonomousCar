import picamera
import cv2
import os
import time

camera = picamera.PiCamera()
camera.resolution = (150,75)
i=0
j=0

time.sleep(1)
print "Start."
while(j<=600):
       	k = raw_input()
	if k == 's':
		i+=1
		camera.capture("stop"+str(i)+".jpg")
		os.system("scp stop"+str(i)+".jpg anurag@192.168.1.62:Documents/Scripts/AutonomousCar/images/")

        elif k == 'o':
		j+=1
		camera.capture("background"+str(j)+".jpg")
		os.system("scp background"+str(j)+".jpg anurag@192.168.1.62:Documents/Scripts/AutonomousCar/images/")
		time.sleep(0.5)
	else:
		continue
