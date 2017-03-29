import socket
import re
import sys
import urlparse
from subprocess import Popen, PIPE
from threading import Thread



def getMachineIP():
#	print([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1])
    l = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
    return l


def getConnectedMachines(ip):
    nn = ip.split('.')
    print nn
    #for n in range(256):


#print getMachineIP()



class Pinger(object):
    def __init__(self, hosts):
        for host in hosts:
            #hostname = urlparse.urlparse(host).hostname
            hostname = host
            if hostname:
                pa = PingAgent(hostname)
                pa.start()
            else:
                continue

class PingAgent(Thread):
    def __init__(self, host):
        Thread.__init__(self)        
        self.host = host

    def run(self):
        p = Popen('ping -n 1 ' + self.host, stdout=PIPE)
        s = p.stdout.read()
        print s
        m = re.search('Average = (.*)ms', p.stdout.read())
        n = re.search('Medio =  (.*)ms', p.stdout.read())
        if m: print '%s - Round Trip Time: %s ms\n' % self.host, m.group(1)
        elif n: print '%s - Round Trip Time: %s ms\n' % self.host, n.group(1)
        else: print '%s - Error: Invalid Response\n' % self.host


if __name__ == '__main__':
#    content = []
#    for i in range(1):
#        s = '192.168.0.%d' % i
#        content.append(s)
#    #print content
#    p = Pinger(content)
	import nmap                         # import nmap.py module
	nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
	nm.scan('127.0.0.1', '22-443')      # scan host 127.0.0.1, ports from 22 to 443
	nm.command_line()                   # get command line used for the scan : nmap -oX - -p 22-443 127.0.0.1
	nm.scaninfo()                       # get nmap scan informations {'tcp': {'services': '22-443', 'method': 'connect'}}
	nm.all_hosts()                      # get all hosts that were scanned
	print nm['127.0.0.1'].hostname()          # get hostname for host 127.0.0.1
	print nm['127.0.0.1'].state()             # get state of host 127.0.0.1 (up|down|unknown|skipped)
	print nm['127.0.0.1'].all_protocols()     # get all scanned protocols ['tcp', 'udp'] in (ip|tcp|udp|sctp)
	print nm['127.0.0.1']['tcp'].keys()       # get all ports for tcp protocol
	print nm['127.0.0.1'].all_tcp()           # get all ports for tcp protocol (sorted version)
	print nm['127.0.0.1'].all_udp()           # get all ports for udp protocol (sorted version)
	print nm['127.0.0.1'].all_ip()            # get all ports for ip protocol (sorted version)
	print nm['127.0.0.1'].all_sctp()          # get all ports for sctp protocol (sorted version)
	print nm['127.0.0.1'].has_tcp(22)         # is there any information for port 22/tcp on host 127.0.0.1
	print nm['127.0.0.1']['tcp'][22]          # get infos about port 22 in tcp on host 127.0.0.1
	print nm['127.0.0.1'].tcp(22)             # get infos about port 22 in tcp on host 127.0.0.1
	print nm['127.0.0.1']['tcp'][22]['state'] # get state of port 22/tcp on host 127.0.0.1 (open
	# for host in nm.all_hosts():
	#     print '----------------------------------------------------'
	#     print 'Host : %s (%s)' % (host, nm[host].hostname())
	#     print 'State : %s' % nm[host].state()

	#     for proto in nm[host].all_protocols():
	#         print '----------'
	#         print 'Protocol : %s' % proto

	#         lport = nm[host][proto].keys()
	#         lport.sort()
	#         for port in lport:
	#             print 'port : %s\tstate : %s' % (port, nm[host][proto][port]['state'])
