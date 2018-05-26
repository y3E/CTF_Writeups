import socket
import os
import sys

# Argument Variable
prxaddr = sys.argv[1]
prxport = int(sys.argv[2])
tgtaddr = sys.argv[3]
tgtport = int(sys.argv[4])

if len(sys.argv) < 4 :
	print ("[*] Invalid Argument")
	print ("Usage : python %s <ProxyIP> <ProxyPortNumber> <TargetIP> <TargetPort>" %(sys.argv[0]))
	sys.exit()

# Create Socket	
c1sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Proccess proxy address
pipddr = socket.gethostbyname(prxaddr)
prxdst = (pipddr, prxport)

# Connect to Proxy
c1sock.connect(prxdst)
print ("[*] Connecting to proxy %s ..." %pipddr)

# Receive connection flag from proxy
conflg = c1sock.recv(1)
if conflg is not None :
	print("[*] Successfully connected to proxy !")
else :
	print("[*] Failed to connect, exiting...")
	sys.exit(0)

# Send target address to proxy
c1sock.send(tgtaddr + "#" + str(tgtport))

# Receive Error flag from proxy
respns = c1sock.recv(50)
conflg = respns[0]
if conflg == '3' :
	msgerr = respns[respns.index("#")+1:len(respns)]
	print ("[*] %s, exiting ..." %msgerr)
	c1sock.close()
	sys.exit(0)

# Receive success and failed connection flag from proxy
conflg = c1sock.recv(10)	
if conflg == "2" :
	print ("[*] Successfully connected to %s" %tgtaddr)
else :
	print ("[*] Error, cannot connect to destined address or it is not available")
	c1sock.close()
	sys.exit(0)

# Main Code
print("Wellcome to tugaskoirvan.exe v1.0.0")
uname = raw_input("What is your name : ")
c1sock.send(uname)
print("------------------------------------------------------")
print("Hi %s, you are paired with %s, let's start chatting !!" %(uname,tgtaddr))

while True :	
	msg = raw_input("%s : "%uname)
	c1sock.send(msg)
	msg = c1sock.recv(1024)
	if msg == "signal.exit" :
		c1sock.close()
		os.system("clear")
		sys.exit(0)
	print("%s : %s" %(tgtaddr,msg))
	
	
c1sock.close()

