import sys
import socket
import time
from datetime import datetime
from threading import Thread

origtime = datetime.now()
threads = []
openports = {}

def superTrouper(start, end, ip):
	global checks
	global strings
	for port in range(start, end):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			conn = s.connect_ex((ip, port))
			if conn is 0:
				try:
					openports[port] = "Port " + str(port) + " open, service: " + str(socket.getservbyport(port, 'tcp'))
				except:
					openports[port] = "Port " + str(port) + " open, service: Unknown" 
		except socket.error:
			print "Socket error."
			s.close()
			continue
		s.close()
		
def main():
	if len(sys.argv) <= 1:
		print "Exiting."
	url = str(sys.argv[1])
	ip = socket.gethostbyname(url)
	print "Please wait for a few (usually 3-4) minutes..."
	tno = 1000
	for x in range(tno):
		if((x+1)*(65536/tno)<=65536):
			th = Thread(target = superTrouper, args = (x*(65536/tno), (x+1)*(65536/tno), ip))
		else:
			th = Thread(target = superTrouper, args = (x*(65536/tno), 65536, ip))			
		th.start()
		threads.append(th)
	for x in threads:
		x.join()
	dictkeys = openports.keys()
	dictkeys.sort()
	for each in dictkeys:
		print openports[each]
	print "Time taken:", datetime.now()-origtime, "\nNumber of open ports:", len(openports), "\nScan rate:", 65536/((datetime.now()-origtime).total_seconds()), "ports per second."
		
main()