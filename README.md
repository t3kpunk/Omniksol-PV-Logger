# Data Logger for Omniksol PV inverter
=====
This script logs the data received from the Omniksol photovoltaic inverter.
It's intercepting data send to a www site and store's it locally. Only csv
format is supported and saved to a local file. .
Wifi kits with a s/n starting with 402 are supported.
It's using a module from https://github.com/Woutrrr/Omnik-Data-Logger


This script is listening on port 10004 and receives every 5 minutes data from
the wifi module. The wifi module contacts a public IP. Iptables reroutes this
public IP to the python server on the wifi network.
It can be used running on a Raspberry Pi with Debian Wheezy. The init script
omniklog can be used to start the script when booting. It will also configure
the iptables rules. Init script omniklog and python server can both log to
syslog which could be useful for remote monitoring.



## Setup

* edit the init bash script omniklog and omniksol4kd.py to change the settings
* cp omniklog /etc/init.d/omniklog
* by default the server is running as a privileged user pi
* Start the server with /etc/init.d/omniklog start
* via the web interface on the onmiksol wifi module, configure a fixed IP address
  and point the WiFi Gateway address towards the python server IP.
* init script requires lsof. Install lsof: apt-get install lsof



### Example syslog

syslog example that can be used on the Raspberry Pi to monitor it.
edit /etc/rsyslog.conf

$WorkDirectory /var/spool/rsyslog  # where to place spool files
$ActionQueueFileName fwdRule1      # unique name prefix for spool files
$ActionQueueMaxDiskSpace 1g        # 1gb space limit (use as much as possible)
$ActionQueueSaveOnShutdown on      # save messages to disk on shutdown
$ActionQueueType LinkedList        # run asynchronously
$ActionResumeRetryCount -1         # infinite retries if host is down

remote host is: name/ip:port, e.g. 192.168.0.7:514, port optional

Provides UDP forwarding. The IP is the server's IP address
*.* @192.168.0.7:514

Provides TCP forwarding. But the current server runs on UDP
*.* @@192.168.0.2:514



### Example Iptables

In this example the Raspberry Pi IP on the wifi network = 192.168.0.100

iptables -t nat -A PREROUTING -p tcp -d 176.58.117.69 --dport 10004 -j DNAT --to-destination 192.168.0.100:10004

iptables -t nat -A OUTPUT -p tcp -d 176.58.117.69 -j DNAT --to-destination 192.168.0.100

## TODO
Adding support for storing the data in a database and uploading to
Pvoutput.org.


