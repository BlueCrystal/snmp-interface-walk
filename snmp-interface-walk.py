#!/usr/bin/env python2.7
import os
import argparse
import sys
import subprocess

#Version 0.2a
def parse_args(arguments):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('ip', help='destination IP')
    client_method = parser.add_mutually_exclusive_group()
    client_method.add_argument('-c', help='Cisco tag', action='store_true')
    client_method.add_argument('-H', help='HP tag', action='store_true')
    parser.add_argument('-s', help='Obtain Serial Number', action='store_true')
    args = parser.parse_args(arguments)
    return args

def run_checks(ip):
    print("\033[1m" + "Running Test Checks for Validation" + "\033[0m")
    print("\033[1m" + "Ping Test" + "\033[0m")
    ping = os.system("ping -c 1 {}".format(ip))
    if ping == 0:
        print("\033[1m" + "Site is up, add Ping Check" + "\033[0m")
    else:
        sys.exit("\033[1m" + "Site down, ignore" + "\033[0m")
    print ("\033[1m" + "Testing SNMP Community" + "\033[0m")
    testsnmp = subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.1.1.0".format(ip).split())
    if testsnmp == 0:
        print("\033[1m" + "SNMP Community Injected, Add Checks" + "\033[0m")
    else:
        sys.exit("\033[1m" + "SNMP Community Not Injected, Leave Ping Only" + "\033[0m")
    print("\033[1m" + "Interface Status Sample Test" + "\033[0m")
    ifstatus = subprocess.call("/usr/lib/nagios/plugins/check_ifstatus -v2 -H {} -C SNMPCOMMUNITYHERE\n\n".format(ip).split())
    print("\033[1m" + "CPU Status Sample Test" + "\033[0m")
    cpustatus = subprocess.call("/usr/lib/nagios/plugins/check_snmp_load.pl -H {} -T cisco -C SNMPCOMMUNITYHERE -w 101,101,90 -c 102,102,95\n\n".format(ip).split())
    print("\033[1m" + "Environment Status Sample Test" + "\033[0m")
    envstatus = subprocess.call("/usr/lib/nagios/plugins/check_snmp_env.pl -H {} -T cisco -C SNMPCOMMUNITYHERE\n\n".format(ip).split())
    print("\033[1m" + "Interface Error Sample Test" + "\033[0m")
    iferror = subprocess.call("/usr/lib/nagios/plugins/check_iferrors -H {} -C SNMPCOMMUNITYHERE -w 300\n\n".format(ip).split())
    print("\033[1m" + "Printing Full List of Interfaces" + "\033[0m")
    intlistfull = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.2".format(ip).split())
    print("\033[1m" + "Printing Full List of Physical Interfaces" + "\033[0m")
    intlistphys = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.2 | grep 'FastEthernet\|GigabitEthernet\|Serial\|Port-channel\|Ethernet\|Multilink\|Cellular'".format(ip), shell=True)
    print("\033[1m" + "Printing Full List of Enabled Interfaces" + "\033[0m")
    intlisten = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.8 | grep 'INTEGER: 1' > intlist".format(ip), shell=True)
    subprocess.call("cat intlist", shell=True)
    print("\033[1m" + "Printing Full List of Interface Descriptions" + "\033[0m")
    intlistdesc = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.31.1.1.1.18 > intlistdesc".format(ip), shell=True)
    subprocess.call("cat intlistdesc", shell=True)
    print("\033[1m" + "Printing Status of Interfaces" + "\033[0m")
    intliststatus = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.8 > intliststatus".format(ip), shell=True)
    subprocess.call("cat intliststatus", shell=True)

    print("\033[1m" + "Printing comma separated integers for all Enabled Devices" + "\033[0m")
    commalist = subprocess.call("grep -oP '(?<=\d\.)\d+(?= = INTEGER)' intlist | paste -s -d , >> csv", shell=True)
    with open('csv', 'r') as in_file:
        text = in_file.read()
        print("\033[31;1m" + text + "\033[0;0m")
    if testsnmp == 0:
        print("\033[1m" + "SNMP Community Injected, Add Checks" + "\033[0m")
    else:
        sys.exit("\033[1m" + "SNMP Community Not Injected, Leave Ping Only" + "\033[0m")
    if ifstatus == 2:
        print("\033[1m" + "Interface Status Works, Add Check" + "\033[0m")
    else:
        print("\033[1m" + "Interface Status Failed, Do Not Add" + "\033[0m")
    if cpustatus == 0:
        print("\033[1m" + "CPU Status Works, Add Check" + "\033[0m")
    else:
        print("\033[1m" + "CPU Status Failed, Do Not Add" + "\033[0m")
    if envstatus == 0:
        print("\033[1m" + "Environment Status Works, Add Check" + "\033[0m")
    else:
        print("\033[1m" + "Environment Status Failed, Do Not Add" + "\033[0m")
    if iferror == 0:
        print("\033[1m" + "Interface Errors Works, Add Check" + "\033[0m")
    else:
        print("\033[1m" + "Interface Errors Failed, Do Not Add" + "\033[0m")
#    subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} iso.3.6.1.2.1.47.1.1.1.1.11.1".format(ip).split())
#    subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} iso.3.6.1.2.1.47.1.1.1.1.11.1001".format(ip).split())
    print("\033[1m" + "Cleaning Up" + "\033[0m")
    cleanup = subprocess.call("rm -f intlist && rm csv", shell=True)

def ciscoserial(ip):
    print("\033[1m" + "Device:" + "\033[0m")
    subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} iso.3.6.1.2.1.1.1.0 | grep 'Cisco IOS'".format(ip), shell=True)
    subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} iso.3.6.1.2.1.47.1.1.1.1.11.1".format(ip).split())
    subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} iso.3.6.1.2.1.47.1.1.1.1.11.1001".format(ip).split())

def hpserial(ip):
    subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.4.1.11.2.36.1.1.2.2.0".format(ip).split())
    print("Environment Status for ProCurve Does Not Work")
    print("Interface Status Check for ProCurve Does Not Work")
    print("Interface Errors Check for ProCurve Does Not Work")

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    if not args.c and not args.H:
        args.c = True
    if (args.c or args.H) and not args.s:
        #runs with -c, -H
        print("running checks")
        run_checks(args.ip)
    if args.H:
        # runs with -H, -Hs
        # runs with -H, -Hs
        print("running HP")
        hpserial(args.ip)
    elif args.c:
        # runs with -c, -s, and -cs
        print("running Cisco")
        ciscoserial(args.ip)
    print("IP Address: {}".format(args.ip))

