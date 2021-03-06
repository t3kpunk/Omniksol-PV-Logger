#!/usr/bin/env python

# omniksol wifi photovoltaic test server simulator
# Simulates the omniksol wifi module
import socket
import time
import sys


# destination
dhost = '176.58.117.69'
dport = 10004

# source
shost = '192.168.0.100'                             #<<<< change this to your listing IP address >>>>>
sport = 10000

wifi_serial = 'BEDN4020XXXXXXXX'             #<<<< change this to your serial >>>>>


omnikdata = list()


omnikdata = [ \
'hUA\xb0\xf4\x85\xd5#\xf4\x85\xd5#\x81\x02\x01' + wifi_serial + '\x01X\n\xb4\n\xc2\xff\xff\x00/\x00%\xff\xff\x00V\xff\xff\xff\xff\t<\xff\xff\xff\xff\x13\x8f\x08\x17\xff\xff\xff\xff\xff\xff\xff\xff\x01s\x00\x00(\x1f\x00\x00\t\x1e\x00\x01\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x89\x16h\x0fA\xf0\xf4\x85\xd5#\xf4\x85\xd5#DATA SEND IS OK\xfc\x16', \
'hUA\xb0\xf4\x85\xd5#\xf4\x85\xd5#\x81\x02\x01' + wifi_serial + '\x01^\n\x9c\n\xcd\xff\xff\x00.\x00!\xff\xff\x00Q\xff\xff\xff\xff\t4\xff\xff\xff\xff\x13\x8d\x07\x8b\xff\xff\xff\xff\xff\xff\xff\xff\x01\x83\x00\x00( \x00\x00\t\x1e\x00\x01\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf2\x16h\x0fA\xf0\xf4\x85\xd5#\xf4\x85\xd5#DATA SEND IS OK\xfc\x16', \
'hUA\xb0\xf4\x85\xd5#\xf4\x85\xd5#\x81\x02\x01' + wifi_serial + '\x01X\t\xd6\ny\xff\xff\x00\x0b\x00\x0b\xff\xff\x00\x15\xff\xff\xff\xff\t\x0c\xff\xff\xff\xff\x13\x8c\x01\xf9\xff\xff\xff\xff\xff\xff\xff\xff\x01\x8e\x00\x00(!\x00\x00\t\x1e\x00\x01\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa7\x16h\x0fA\xf0\xf4\x85\xd5#\xf4\x85\xd5#DATA SEND IS OK\xfc\x16', \
'hUA\xb0\xf4\x85\xd5#\xf4\x85\xd5#\x81\x02\x01' + wifi_serial + '\x01T\nb\x0b\xb1\xff\xff\x00+\x00\x1a\xff\xff\x00G\xff\xff\xff\xff\t4\xff\xff\xff\xff\x13\x8d\x06\x8a\xff\xff\xff\xff\xff\xff\xff\xff\x01\x96\x00\x00("\x00\x00\t\x1e\x00\x01\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x92\x16h\x0fA\xf0\xf4\x85\xd5#\xf4\x85\xd5#DATA SEND IS OK\xfc\x16', \
'hUA\xb0\xf4\x85\xd5#\xf4\x85\xd5#\x81\x02\x01' + wifi_serial + '\x01I\nH\nu\xff\xff\x00\t\x00\t\xff\xff\x00\x11\xff\xff\xff\xff\t\x1c\xff\xff\xff\xff\x13\x8a\x01\xa5\xff\xff\xff\xff\xff\xff\xff\xff\x01\x9a\x00\x00(#\x00\x00\t\x1e\x00\x01\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc7\x16h\x0fA\xf0\xf4\x85\xd5#\xf4\x85\xd5#DATA SEND IS OK\xfc\x16', \
'hUA\xb0\xf4\x85\xd5#\xf4\x85\xd5#\x81\x02\x01' + wifi_serial + '\x01F\n\xac\n\xd0\xff\xff\x00$\x00\x16\xff\xff\x00;\xff\xff\xff\xff\t,\xff\xff\xff\xff\x13\x8d\x05G\xff\xff\xff\xff\xff\xff\xff\xff\x01\x9e\x00\x00(#\x00\x00\t\x1e\x00\x01\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x92\x16h\x0fA\xf0\xf4\x85\xd5#\xf4\x85\xd5#DATA SEND IS OK\xfc\x16', \
'hUA\xb0\xf4\x85\xd5#\xf4\x85\xd5#\x81\x02\x01' + wifi_serial + '\x01M\x0bY\x0b\x8e\xff\xff\x00.\x00\x1d\xff\xff\x00R\xff\xff\xff\xff\t,\xff\xff\xff\xff\x13\x8a\x07\x93\xff\xff\xff\xff\xff\xff\xff\xff\x01\xa7\x00\x00($\x00\x00\t\x1f\x00\x01\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x16h\x0fA\xf0\xf4\x85\xd5#\xf4\x85\xd5#DATA SEND IS OK\xfc\x16', \
'hUA\xb0\xf4\x85\xd5#\xf4\x85\xd5#\x81\x02\x01' + wifi_serial + '\x01H\n\xd7\n\xef\xff\xff\x00\x08\x00\x08\xff\xff\x00\x11\xff\xff\xff\xff\t\x1c\xff\xff\xff\xff\x13\x8a\x01\xa1\xff\xff\xff\xff\xff\xff\xff\xff\x01\xaf\x00\x00(%\x00\x00\t\x1f\x00\x01\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe1\x16h\x0fA\xf0\xf4\x85\xd5#\xf4\x85\xd5#DATA SEND IS OK\xfc\x16'
]



for d in omnikdata:
    #s.settimeout(0.2)
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((shost, sport))
            print >>sys.stdout, 'Starting up on %s port %s' % (shost, sport)
        except socket.error , msg:
            #print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message: ' + msg[1]
            pass

        try:
            s.connect((dhost, dport))
            print >>sys.stdout, 'Connecting to %s port %s' % (dhost, dport)
        except socket.error , msg:
            print 'Connection failed. Error Code : ' + str(msg[0]) + ' Message: ' + msg[1]
        except KeyboardInterrupt:
            print "You pressed Ctrl+C"
            s.close()
            sys.exit()
        else:
            s.sendall(d)
            s.close()
            break
        finally:
            time.sleep(5)







