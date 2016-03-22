import RPi.GPIO as GPIO
import time

class EchoDistance():
	def __init__(self):
		self.trig = 23
		self.echo = 24
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.trig, GPIO.OUT)
		GPIO.setup(self.echo, GPIO.IN)
		GPIO.output(self.trig, False)
		time.sleep(2)
		return
	def get_obstacle_distance(self):
		GPIO.output(self.trig, True)
		time.sleep(0.00001)
		GPIO.output(self.trig, False)

		while(GPIO.input(self.echo) == False):
			pulse_start = time.time()
		while(GPIO.input(self.echo) == True):
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start

		distance = pulse_duration * 17150
	
		return distance
