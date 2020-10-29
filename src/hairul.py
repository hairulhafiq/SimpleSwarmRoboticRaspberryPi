#sonar obstacle avoiding bot in python

#import required Python libraries
import time
import MFRC522
import signal
import socket
import RPi.GPIO as GPIO
from subprocess import call

#RFID
MIFAREReader = MFRC522.MFRC522()

cardA = [6,100,18,73,57]
cardB = [242,231,88,100,41]

def end_read(signal, frame):
  global continue_reading
  continue_reading = False
  MIFAREReader.GPIO_CLEEN()

signal.signal(signal.SIGINT, end_read)

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 23

MLEFT = 4
MRIGHT = 25
e1 = 17 
e2 =10 

#set pins as output and input
GPIO.setwarnings(False)                 #Disable warnings
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)	#Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)		#Echo

#Set trigger to false(low)
GPIO.output(GPIO_TRIGGER, False)

#allow module to settle
time.sleep(0.5)

def sonar(n):
	#send 10 us pulse to trigger
        stop = False
	GPIO.output(GPIO_TRIGGER,1)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, 0)
        
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

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(GPIO_ECHO, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(e1, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(e2, GPIO.OUT)
GPIO.setwarnings(False)
time.sleep(1)

while True:
        stop = True
	time.sleep(0.3)

	distance = sonar (0)
	print distance

	if(distance >8.5):
		#foward
		GPIO.output(e1, 1)
		GPIO.output(e2, 1)
		GPIO.output(MLEFT, 1)
		GPIO.output(MRIGHT,1)

	elif(4.9<distance<8.0):
		#stop
		GPIO.output(e1, 0)
		GPIO.output(e2, 0)
		GPIO.output(MLEFT, 0)
		GPIO.output(MRIGHT,0)
		time.sleep(2)
                #rfid
		print "detecting RFID"
		
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                if status == MIFAREReader.MI_OK:
                  #continue_reading = True
                  #while continue_reading:
                  print "Card detected"
                (status,backData) = MIFAREReader.MFRC522_Anticoll()
                if status == MIFAREReader.MI_OK:
                  print "Card read UID: "+str(backData[0])+","+str(backData[1])+","+str(backData[2])+","+str(backData[3])+","+str(backData[4])
                  if  backData == cardA:
                    print "Robot A"
                    #UDP_IP = "192.168.0.121"
                    #UDP_PORT = 5005
                    #MESSAGE = "11"
                    #print "UDP target IP: ", UDP_IP
                    #print "UDP target port: ", UDP_PORT
                    #print "Message: ", MESSAGE
                    #sock = socket.socket(socket.AF_INET,
                    #                     socket.SOCK_DGRAM)
                    #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

                  elif backData == cardB:
                    print "Robot B"
                    #UDP_IP = "192.168.0.122"
                    #UDP_PORT = 5005
                    #MESSAGE = "11"
                    #print "UDP target IP: ", UDP_IP
                    #print "UDP target port: ", UDP_PORT
                    #print "Message: ", MESSAGE
                    #sock = socket.socket(socket.AF_INET,
                    #                     socket.SOCK_DGRAM)
                    #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                MIFAREReader.GPIO_CLEEN()
                #continue_reading = False
                time.sleep(2)

                #runaway
                #elif status == MIFAREReader.MI_OK:
                 # print "No RFID Detected"
                  #GPIO.output(e1, 0)
                  #GPIO.output(e2, 0)
                  #GPIO.output(MLEFT, 0)
                  #GPIO.output(MRIGHT,0)
                  #time.sleep(2)
                  #GPIO.output(e1, 1)
                  #GPIO.output(MRIGHT, 1)
