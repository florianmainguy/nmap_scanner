INTRODUCTION
------------

The scanner.py script is a simple nmap scanner which takes a list
or file of host/ipv4/ipv6/cidr as input. The nmap report is then
exported to a html file with informations about the discovered
hosts, open services, etc.



REQUIREMENTS
------------

The script uses python3.
The following packages need to be installed:

 * sudo pip3 install python-libnmap
 * sudo pip3 install pytest



USAGE
-----

The script needs to be run as root to allow discovery of MAC
addresses for hosts on local network. Run with one of the
following flags:

 * sudo python3 scanner.py -i [list of host/ipv4/ipv6/cidr]
 * sudo python3 scanner.py -iF [file of host/ipv4/ipv6/cidr]

In case of a list of targets, they should be separated by spaces.
Output file is named report.html.

Examples:

 * sudo python3 scanner.py -i www.synacktiv.com
 * sudo python3 scanner.py -i 91.209.35.0/24
 * sudo python3 scanner.py -i www.synacktiv.com 8.8.8.8
 * sudo python3 scanner.py -iF target.txt

 

FEATURES
--------

The Nmap scan is done through the python-libnmap package. The
following flags are applied
 * -sV: enables version detection
 * -sC: anables script scanning (NSE)
 * -p-: all ports
 * -T4: timing agressive
 
The nmap settings applied have been chosen to get a maximum of
information in a short time.

The html report contains:
 * A summary of the scan with the number of hosts up/down
 * A list of the scanned hosts ordered by their state (up first)
 * A list of all the online hosts with information on their open ports (state, service, banner, result of NSE scripts, URL to CVEs from CPE)
 * A list of all the opened services with some basic information



TEST
----

Tests use the Pytest framework. They are located in /test.
Run in current directory:

 * pytest