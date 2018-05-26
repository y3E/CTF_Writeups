import socket
import os
import sys


# Proxy Address, Port, and Socket
paddr = ('localhost',1234)
psock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
psock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind Address
psock.bind(paddr)

# Listen to a connection
psock.listen(1) 
print ("[*] Proxy active...")

# Loop to find a new connection & Rules
while True :
	#Accept connection to client
	print ("[*] Waiting for a new connection ...")
	connection, caddr1 = psock.accept()
	if connection is not None  :
		print "[*] Client connect success !"
	
	#Sending connection flag to client
	conflg = '1' 
	connection.send(conflg)
	
	# Receive target address to forward
	fwd = connection.recv(64)

# Rules Starts Here------------------------------------------------------------
	#Add another ip to ban with listed format below
	if fwd[0:fwd.index("#")] == "202.58.182.60" :
		print ("[*] Recorded client %s requesting to forbidden IP -> 202.58.182.60. Blocking Request ..." %caddr1[0])
		conflg = '3'
		msgerr = 'Error 3 : Forbidden IP'
		connection.send(conflg + '#' + msgerr)
		connection.close()
		print("[*] Request Blocked.")
		print("-----------------------------------------------------")
	elif fwd[0:fwd.index("#")] == "10.22.103.20" :
		print ("[*] Recorded client %s requesting to forbidden IP -> 10.22.103.20. Blocking Request ..." %caddr1[0])
		conflg = '3'
		msgerr = 'Error 3 : Forbidden IP'
		connection.send(conflg + '#' + msgerr)
		connection.close()
		print("[*] Request Blocked.")
		print("-----------------------------------------------------")
	
	else :
		conflg = '2'
		connection.send(conflg)
		break

# End of Rules-----------------------------------------------------------------

# Dissect target address & tupple it
fwdaddr = fwd[0:fwd.index("#")]
fwdport = fwd[fwd.index("#")+1:len(fwd)]
fwddest = (fwdaddr, int(fwdport))

# Create a forward connection to target address
print ("[*] Forwarding %s to %s ..." %(caddr1[0], fwdaddr))
fwdsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fwdsock.connect(fwddest)

# Error validation
if fwdsock.connect != -1:
	conflg = "2"
	connection.send(conflg)
	print ("[*] Connected...")
else :
	print ("[*] Fail to connect, canot connect to destined address or it is not available")
	sys.exit(0)

# Receive data from client1 and forward it to client2
data = connection.recv(1024)
fwdsock.send(data)

# Receive and forward connection from both
while True:
	msg = connection.recv(1024)
	if msg == "sys.terminate" :
		msg = "signal.exit"
		fwdsock.send(msg)
		connection.send(msg)
		psock.close()
		os.system("clear")
		sys.exit(0)
	fwdsock.send(msg)
	msg = fwdsock.recv(1024)
	connection.send(msg)


psock.close()



