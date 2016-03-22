import RPi.GPIO as GPIO
import time

class MoveCar():
	def __init__(self):
		self.forward=2
		self.backward=3
		self.left=4
		self.right=17
		self.control=''
		self.runtime=0.1

	def initialize(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.forward, GPIO.OUT)
		GPIO.setup(self.backward, GPIO.OUT)
		GPIO.setup(self.left, GPIO.OUT)
		GPIO.setup(self.right, GPIO.OUT)

	def move_forward(self):
		self.control='f'
		GPIO.output(self.backward,0)
		GPIO.output(self.forward,1)

	def move_backward(self):
		self.control='b'
		GPIO.output(self.forward,0)
		GPIO.output(self.backward,1)

	def move_left(self):
		GPIO.output(self.right,0)
		GPIO.output(self.left,1)

	def move_right(self):
		GPIO.output(self.left,0)
		GPIO.output(self.right,1)

	def move_stopall(self):
		GPIO.output(self.left,0)
		GPIO.output(self.right,0)
		GPIO.output(self.backward,0)
		GPIO.output(self.forward,0)
	
	def move_stopfb(self):
                GPIO.output(self.backward,0)
                GPIO.output(self.forward,0)

	def move_stoplr(self):
		GPIO.output(self.left,0)
		GPIO.output(self.right,0)
	
	def brake(self):
		if(self.control==''):
			pass
		elif(self.control=='f'):
			print "Applying brake."
			self.move_backward()
			time.sleep(self.runtime)
			self.move_stopfb()
			self.control=''
		elif(self.control=='b'):
			print "Applying brake."
                        self.move_forward()
                        time.sleep(self.runtime)
                        self.move_stopfb()
			self.control=''
		else:
			pass
			

	def close(self):
		GPIO.cleanup()
		
