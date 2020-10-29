#sonar obstacle avoiding bot in python

#import required Python libraries
import time
import MFRC522
import signal
import RPi.GPIO as GPIO
import socket
import sys
from subprocess import call

#Set Raspberry Pi Mode
GPIO.setmode(GPIO.BOARD)

# Motor and Sensor
GPIO_TRIGGER = 12
GPIO_ECHO = 16

MLEFT = 7
MRIGHT = 22
e1 = 11 
e2 =19

#set pins as output and input
GPIO.setwarnings(False)                 #Disable warnings
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)	#Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)		#Echo

#Set trigger to false(low)
GPIO.output(GPIO_TRIGGER, False)

#allow module to settle
time.sleep(0.5)


#RFID
MIFAREReader = MFRC522.MFRC522()

cardA = [5,74,28,185,234]
cardB = [83,164,247,164,164]

#Connection
being_follow = False

#act as server
def server(n):
        UDP_IP = "192.168.0.109"
        UDP_PORT = 80
        MESSAGE = "1"

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(5005)
        if data == '1':
                GPIO.output(e1, 0)
		GPIO.output(e2, 0)
                print "Receive From   : ", addr
                sock.sendto(MESSAGE, addr)
                print "I am being follow by : ", addr
                being_follow = True
        return being_follow
                
                

def sonar(n):
	#send 10 us pulse to trigger
	GPIO.output(GPIO_TRIGGER,True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	start = time.time()

	#this doesn't allow for timeout!

	while GPIO.input(GPIO_ECHO)==0:
		start = time.time()

	while GPIO.input(GPIO_ECHO)==1:
		stop = time.time()
	
	#calculate pulse lenght
	elapsed = stop - start

	#distance pulse travelled in that time in time
	#multiplied by the speed of sound (cm/s)
	distance = elapsed * 34000

	#that was the distance there and back so halve the value
	distance = distance / 2
	
	return distance

GPIO.setup(MLEFT, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(MRIGHT, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(e1, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(e2, GPIO.OUT)
GPIO.setwarnings(False)
time.sleep(1)

while True:
        global delay
        
	time.sleep(0.3)
        server(0)
	distance = sonar (0)
	print distance

	if(distance >9):
		#foward
		GPIO.output(e1, 1)
		GPIO.output(e2, 1)
		GPIO.output(MLEFT, 1)
		GPIO.output(MRIGHT,1)

	elif(4.9<distance<8.9):
		#stop
		GPIO.output(e1, 0)
		GPIO.output(e2, 0)
		print "Detecting RFID"
		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                if status == MIFAREReader.MI_OK:
                        print "Card detected"
                        if  backData == cardA:
                                UDP_IP = "192.168.0.106"
                                UDP_PORT = 80
                                MESSAGE = "1"
                                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                                print "Following robot A"
                        elif backData == cardB:
                                UDP_IP = "192.168.0.104"
                                UDP_PORT = 80
                                MESSAGE = "1"
                                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                                print "Following robot B"
                        MIFAREReader.GPIO_CLEEN()
                
                elif status == MIFAREReader.MI_ERR:
                        print "No RFID detected, It's an obstacle or wall."
                        GPIO.output(e1, 1)
                        GPIO.output(e2, 1)
                        GPIO.output(MLEFT, 1)
                        GPIO.output(MRIGHT,0)
                        time.sleep(delay)
                        GPIO.output(e1, 0)
                        GPIO.output(e2, 0)
