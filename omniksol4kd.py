#!/usr/bin/python

# This script simulates  the omniksol website. Data is send from Omniksol wifi module
# to the host = '176.58.117.69:10004'

import InverterMsg              # Import the Msg handler. Thanx to (https://github.com/Woutrrr/Omnik-Data-Logger)
import socket                   # Import socket module
import sys
import time, datetime


host = '192.168.0.100'                              #<<<< change this to your listing IP address >>>>>
port = 10004
buffer = 1024
server_sock = (host, port)

dataFile = 'omnikdata.csv'

#wifi_serial = 'BEDN4020XXXXXXXX'                  #<<<< change this to your serial >>>>>


#  Log to:
console = False
syslog = True
# To enable or disable -> (True or False)

# For debug purpose
#logf  = '/var/log/omniklog.log'
# To disable:
logf = '/dev/null'




def Logging(console, syslog):
    import logging,  os
    # set up logging to file with logging format
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s: %(levelname)-12s %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S',
                        filename=logf,
                        filemode='a'
                        )

    procname = ' * ' + os.path.basename(sys.argv[0])
    logger = logging.getLogger(procname)

    if console:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)s: [%(levelname)s] %(message)s')
        console.setFormatter(formatter)
        logger.addHandler(console)

    if syslog:
        from logging.handlers import SysLogHandler

        syslog = SysLogHandler(address='/dev/log')
        syslog.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)s: %(levelname)-12s %(message)s')
        syslog.setFormatter(formatter)
        logger.addHandler(syslog)

    return logger


log = Logging(console, syslog)




class FormatMsg():

    def __init__(self):
        self.msgHeader = "dateTime,Id,Temp,VPV1,VPV2,VPV3,IPV1,IPV2,IPV3,IAC1,IAC2,IAC3,VAC1,VAC2,VAC3,FAC1,PAC1,FAC2,PAC2,FAC3,PAC3,ETODAY,ETOTAL,HTOTAL"

    def timeStamp(self):
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')

    def decode(self,  msg):
        msgFormat = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},{23}".format(self.timeStamp(),
                msg.getID(),
                msg.getTemp(),
                msg.getVPV(1), msg.getVPV(2), msg.getVPV(3),
                msg.getIPV(1), msg.getIPV(2), msg.getIPV(3),
                msg.getIAC(1), msg.getIAC(2), msg.getIAC(3),
                msg.getVAC(1), msg.getVAC(2), msg.getVAC(3),
                msg.getFAC(1), msg.getPAC(1),
                msg.getFAC(2), msg.getPAC(2),
                msg.getFAC(3), msg.getPAC(3),
                msg.getEToday(), msg.getETotal(), msg.getHTotal())
        return msgFormat

    def consoleMsg(self,  msg):
        print "ID     : {0}      Date:  {1}".format(msg.getID(),  time.strftime("%d-%m-%Y %H:%M:%S"))

        print "E Today: {0:>5}   Total: {1:<5}".format(msg.getEToday(), msg.getETotal())
        print "H Total: {0:>5}   Temp:  {1:<5}".format(msg.getHTotal(), msg.getTemp())

        print "PV1   V: {0:>5}   I: {1:>4}".format(msg.getVPV(1), msg.getIPV(1))
        print "PV2   V: {0:>5}   I: {1:>4}".format(msg.getVPV(2), msg.getIPV(2))
        print "PV3   V: {0:>5}   I: {1:>4}".format(msg.getVPV(3), msg.getIPV(3))

        print "L1    P: {0:>5}   V: {1:>5}   I: {2:>4}   F: {3:>5}".format(msg.getPAC(1), msg.getVAC(1), msg.getIAC(1), msg.getFAC(1))
        print "L2    P: {0:>5}   V: {1:>5}   I: {2:>4}   F: {3:>5}".format(msg.getPAC(2), msg.getVAC(2), msg.getIAC(2), msg.getFAC(2))
        print "L3    P: {0:>5}   V: {1:>5}   I: {2:>4}   F: {3:>5}".format(msg.getPAC(3), msg.getVAC(3), msg.getIAC(3), msg.getFAC(3))

    def loggingMsg(self,  msg):
        log.info("ID     : {0}      Date:  {1}".format(msg.getID(),  time.strftime("%d-%m-%Y %H:%M:%S")))

        log.info("E Today: {0:>5}   Total: {1:<5}".format(msg.getEToday(), msg.getETotal()))
        log.info("H Total: {0:>5}   Temp:  {1:<5}".format(msg.getHTotal(), msg.getTemp()))

        log.info("PV1   V: {0:>5}   I: {1:>4}".format(msg.getVPV(1), msg.getIPV(1)))
        log.info("PV2   V: {0:>5}   I: {1:>4}".format(msg.getVPV(2), msg.getIPV(2)))
        log.info("PV3   V: {0:>5}   I: {1:>4}".format(msg.getVPV(3), msg.getIPV(3)))

        log.info("L1    P: {0:>5}   V: {1:>5}   I: {2:>4}   F: {3:>5}".format(msg.getPAC(1), msg.getVAC(1), msg.getIAC(1), msg.getFAC(1)))
        log.info("L2    P: {0:>5}   V: {1:>5}   I: {2:>4}   F: {3:>5}".format(msg.getPAC(2), msg.getVAC(2), msg.getIAC(2), msg.getFAC(2)))
        log.info("L3    P: {0:>5}   V: {1:>5}   I: {2:>4}   F: {3:>5}".format(msg.getPAC(3), msg.getVAC(3), msg.getIAC(3), msg.getFAC(3)))



class DataLogging(FormatMsg):

    def __init__(self):

        FormatMsg.__init__(self)
        try:
            self.fileHandle = open(dataFile, 'r')
        except IOError as e:
            errno, strerror = e.args
            log.warning('%s: %s' % (strerror,  dataFile))
            if errno == 2:
                # New log file: create csv header if file not exists
                log.info('Create csv data file %s' % (dataFile))
                try:
                     self.fileHandle = open(dataFile, 'w')
                except IOError as e:
                   errno, strerror = e.args
                   log.warning('Error writing %s: %s' % (dataFile, strerror))
                   sys.exit()
                finally:
                    log.info('Write header in database %s' % (dataFile))
                    self.msg = str(self.msgHeader) + '\n'
                    self.fileHandle.write(self.msg)
            else:
                sys.exit()
        try:
            self.fileHandle = open(dataFile, 'a')
        except IOError as e:
           errno, strerror = e.args
           log.warning('Error accessing %s: %s\n' % (dataFile, strerror))
           sys.exit()

    def writeLogLine(self, logLine):
        logLine = str(logLine)  + '\n'
        try:
            self.fileHandle.write(logLine)
        except IOError:
            pass

    def Close(self):
        self.fileHandle.close()


class tcpServer(DataLogging):

    def __init__(self):
        from optparse import OptionParser

        parser = OptionParser()
        parser.add_option("--csv",  help="Output in csv format", action="store_true", default=True )
        parser.add_option("--log", action="store_true", dest="logging", default=True)
        (self.options, self.args) = parser.parse_args()

        # Datagram (tcp) socket
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)               # Create a socket object
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error, msg:
            log.warning('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])

        # Bind socket to local host and port
        log.info('Starting listing on %s port %s' % server_sock)
        try:
            self.s.bind(server_sock)
        except socket.error , msg:
            log.warning('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit(1)
        finally:
            log.info('Socket bind complete')

        try:
            self.s.listen(1)
        except socket.error, msg:
            log.warning('Failed listen. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit(1)


    def Listing(self):
        #now keep listing and start receive data from Omniksol wifi module
        options = self.options

        while True:
            # receive data from client (data, addr)
            log.info('Waiting for a connectionon %s port %s' % server_sock)
            try:
                conn, client_addr = self.s.accept()
            except KeyboardInterrupt:
                log.warning("You pressed Ctrl+C ... Aborting!\n")
                self.s.close()
                sys.exit()
            except socket.error, msg:
                log.warning('Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
                self.s.close()
                sys.exit(1)
            else:
                log.info('Connection from: %s', client_addr)
            finally:
                data = conn.recv(buffer)
                conn.close()
                log.debug('Received data: %s', repr(data))

            if data:
                # This is where Woutrrr's magic happens ;)
                dmsg = InverterMsg.InverterMsg(data)
                # obj dLog transforms de raw data from the photovoltaic Systems converter
                dLog = DataLogging()

                if wifi_serial not in dmsg.getID():
                    log.warning("Received incorrect data!")
                    continue

                if options.csv:
                    csv = dLog.decode(dmsg)
                    dLog.writeLogLine(csv)
                    dLog.Close()

                if options.logging:
                    # print data to console
                    #dLog.consoleMsg(dmsg)
                    dLog.loggingMsg(dmsg)

            else:
                continue

        self.s.close()



def main():
    sevr = tcpServer()
    sevr.Listing()



if __name__ == "__main__":
    main()
