import socket
import os
import sys

# client2 Address, Port, and Socket
c2addr = ('localhost', 5000)
c2sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c2sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Program Loop
while True :
	os.system("clear")
	print ("===[Wellcome to Tugas ANP Ko Irvan]===")
	print ("|1. Run tugaskoirvan.exe             |")
	print ("|2. Exit                             |")
	print ("======================================")
	chc = int(raw_input(">>> "))
	if chc == 1 :
		# Bind address
		c2sock.bind(c2addr)
		
		# Listen to a connection
		c2sock.listen(1)
		print ("[*] Waiting for Connection...")
		
		# Accept
		connection, conaddr = c2sock.accept()
		
		# Main Code
		print ("[*] Got connection from %s" %(conaddr[0]))
		guestname = connection.recv(1024)
		print ("-------------------------------------")
		print ("%s says hello ! Lets start Chatting !" %guestname)
		
		while True :
			msg = connection.recv(1024)
			if msg == "signal.exit" :
				c2sock.close()
				os.system("clear")
				sys.exit(0)
			print("%s : %s" %(guestname,msg))
			msg = raw_input("%s : "%(c2addr[0]))
			connection.send(msg)
			
	
	elif chc == 2 :
		os.system("clear")
		sys.exit(0)

c2sock.close



