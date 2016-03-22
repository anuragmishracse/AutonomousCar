import socket
import movecar
import time

runtime = 0.1
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("Anurags-MacBook-Air.local",10000))

motion = movecar.MoveCar()
motion.initialize()

i=0

while True:
	i+=1
	command = clientSocket.recv(1)
	print "Packet received : "+str(i)
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
	clientSocket.send('1')
	
	
motion.close()
clientSocket.close()

