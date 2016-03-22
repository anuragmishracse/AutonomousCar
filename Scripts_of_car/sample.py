import stopdetect
import cv2
import picamera

camera = picamera.PiCamera()
camera.resolution = (150, 75)

camera.capture("stop.jpg")

detect = stopdetect.StopDetect()
img = cv2.imread("stop.jpg")
stops =  detect.detect_stops(img)

print stops

w=0
for stop, distance in stops:
    x,y,w,h = stop
    print str(w)+"-->"+str(distance)
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),2)

cv2.imwrite("oh.jpg",img)
