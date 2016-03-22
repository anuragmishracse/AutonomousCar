import os
import cv2
import time
import numpy as np
import csv 
from picamera import PiCamera
from picamera.array import PiRGBArray
import movecar
import pybrain
from pybrain.tools.xml.networkreader import NetworkReader
import stopdetect
import echodistance
import RPi.GPIO as GPIO
import thread
import sys

def write_to_file(msg):
    f = open("/var/www/html/decision.txt", 'wb')
    f.write(msg)
    f.flush()
    f.close()

def write_to_image(img):
    cv2.imwrite("/var/www/html/track.jpg", img)

motion = movecar.MoveCar()
motion.initialize()
motion.runtime = 0.5

stop_object = stopdetect.StopDetect()

echo_object = echodistance.EchoDistance()

red = 21 
yellow = 20
green = 26
button = 16

GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)	

GPIO.output(red, 0)
GPIO.output(yellow, 0)
GPIO.output(green, 0)

print "Loading network..."
write_to_file("Loading network...")

GPIO.output(yellow, 1)
if os.path.isfile('/home/pi/Documents/Scripts/AutonomousCar/network.xml'): 
    fnn = NetworkReader.readFrom('/home/pi/Documents/Scripts/AutonomousCar/network.xml') 
    print "Loaded..."
    write_to_file("Loaded...")
else:
    print "Network not present..."
    write_to_file("Network not present...")
    exit(0)
GPIO.output(yellow, 0)

while(True):
    GPIO.output(red, 1)
    while(GPIO.input(button)==True):
        print "Waiting to start..."
        write_to_file("Waiting to start...")
        continue
    GPIO.output(red, 0)
    print "Button press: Starting autonomous run."
    write_to_file("Button press: Starting autonomous run.")
    try:
        GPIO.output(green, 1)

	time.sleep(1)

        resolution_x = 150
        resolution_y = 75

        camera = PiCamera()
        camera.resolution = (resolution_x, resolution_y)
        camera.framerate = 15

        rawCapture = PiRGBArray(camera, size=(resolution_x, resolution_y))

        time.sleep(0.1)

        for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
	    print "Image Captured..."

            color_image = frame.array
            rawCapture.truncate(0)
    	
            if(GPIO.input(button)==False):
                print "Button press: Stopping autonomous run."
                write_to_file("Button press: Stopping autonomous run.")
                raise 1
        		
            obstacle_distance = echo_object.get_obstacle_distance()
            if obstacle_distance <= 40.0:
            	motion.brake()
#		motion.move_stopall()
            	cv2.imwrite("/var/www/html/track.jpg", color_image)
            	print "Obstacle found at "+str(obstacle_distance)+" cm.\n"
            	f = open("/var/www/html/decision.txt", 'wb')
            	f.write("Obstacle found at "+str(obstacle_distance)+" cm.\n")
            	f.flush()
            	f.close()
            	GPIO.output(red, 1)
            	continue

            stops = stop_object.detect_stops(color_image)
            stops = sorted(stops,key=lambda l:l[1], reverse=True)
            stop_command = 0 
            stop_distance = 0
           
            if len(stops)!=0:	
                if stops[0][1] < 35.0:
                    stop_command = 1
                    stop_distance = stops[0][1]
        	    x, y, w ,h = stops[0][0]
         
            if stop_command == 1:
                motion.brake()
#		motion.move_stopall()
                cv2.rectangle(color_image, (x,y), (x+h,y+w), (0,255,0), 2)	
                cv2.imwrite("/var/www/html/track.jpg", color_image)
                f = open("/var/www/html/decision.txt", 'wb')
                f.write("Stop found at "+str(stop_distance)+" cm.\n")
                f.flush()
                f.close()
                print "Stop found at "+str(stop_distance)+" cm.\n"
                GPIO.output(red, 1)
		time.sleep(3)
                continue

            if True:
		GPIO.output(red, 0)
                img = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
                command = np.argmax(fnn.activate(np.ravel(img)))

                if(command == 0):
                    #Move forward
                    motion.move_stoplr()
                    motion.move_forward()

                elif(command == 1):
                    #Move backward
                    motion.move_stoplr()
                    motion.move_backward()

                elif(command == 2):
                    #Move left
                    motion.move_left()
                    motion.move_forward()

                elif(command == 3):
                    #Move right
                    motion.move_right()
                    motion.move_forward()

                else:
                    #Do nothing
                    motion.move_stopfb()
     	
#        	cv2.imwrite("/var/www/html/track.jpg", color_image)
#		thread.start_new_thread(write_to_image,(color_image,))
	    	direction = {0:'Moving forward', 1:'Moving backward', 2:'Moving left', 3:'Moving right'}
	       	f = open("/var/www/html/decision.txt", 'wb')
	  	f.write(direction[command])
		f.flush()
		f.close()
		print "Decision : "+str(direction[command])+"\n"
	
    except:
	camera.close()
        GPIO.output(green, 0)
	GPIO.output(red, 1)
        motion.move_stopall()
	time.sleep(1)		
motion.close()



	
