import cv2

class StopDetect():
    def __init__(self):
        return

    def get_stop_distance(self, img, stop):
        x,y,w,h = stop
        f = 165
	distance = (f*4.5)/float(w)	
	return distance	

    def detect_stops(self, img):
        stopCascade = cv2.CascadeClassifier("/home/pi/Documents/Scripts/AutonomousCar/cascade.xml")
        stops = stopCascade.detectMultiScale(
            img,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(22, 22),
            maxSize=(26, 26),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
	result = []
	for stop in stops:
	    distance = self.get_stop_distance(img, stop)
	    result.append([stop, distance])
	return result
