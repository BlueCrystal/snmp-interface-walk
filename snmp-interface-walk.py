#!/usr/bin/env python2.7
import os
import argparse
import sys
import subprocess

#Version 0.41b
def parse_args(arguments):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('ip', help='destination IP')
    client_method = parser.add_mutually_exclusive_group()
    client_method.add_argument('-p', metavar='--ping', help='Ping Test' action='store_true')
    client_method.add_argument('-t', metavar='--testsnmp', help='SNMP Injection Test', action='store_true')
    client_method.add_argument('--ifstatuscheck', help='Run the Interface Status Check', action='store_true')
    client_method.add_argument('--cpustatuscheck', help='Run the CPU Status Check', action='store_true')
    client_method.add_argument('--envstatuscheck', help='Run the Environment Status Check', action='store_true')
    client_method.add_argument('--iferrorcheck', help='Run the Environment Status Check', action='store_true')
    client_method.add_argument('--iflist', help='Print all Interfaces', action='store_true')
    client_method.add_argument('--iflistphys', help='Print all Physical Interfaces', action='store_true')
    client_method.add_argument('--iflistvirt', help='Print all Virtual Interfaces', action='store_true')
    client_method.add_argument('--iflistallup', help='Print all Physical and Virtual Interfaces That Are Up/Up', action='store_true')
    client_method.add_argument('--ifdesc', help='Print all Physical and Virtual Interface Descriptions', action='store_true')
    client_method.add_argument('--ifstatuses', help='Print all Physical and Virtual Interfaces Status with Type', action='store_true')
    client_method.add_argument('--ifstatusup', help='Print all Physical and Virtual Interfaces that are Up', action='store_true')
    client_method.add_argument('--ifupcs', help='Print all Physical and Virtual Interfaces that are Up and Output Them as a Comma Separated List', action='store_true')
    client_method.add_argument('--liststackports', help='Print a List of all Stack Ports', action='store_true')
    client_method.add_argument('--listupstackcs', help='Print Commma Separated List of Up Stack Ports', action='store_true')
    client_method.add_argument('--listtrunkports', help='Print Full List of Trunk Ports', action='store_true')
    client_method.add_argument('--listuptrunkcs', help='Print Comma Separated List of Up Trunk Ports', action='store_true')
    client_method.add_argument('-c', metavar='--ciscosn', help='Cisco tag', action='store_true')
    client_method.add_argument('-H', metavar='--hpsn', help='HP tag', action='store_true')
    parser.add_argument('-s', help='Obtain Serial Number', action='store_true')
    args = parser.parse_args(arguments)
    return args

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])

#Testing for Validation Begins
def runchecks(ip):
        print("\033[1m" + "Running Test Checks for Validation" + "\033[0m")

#Ping Test. If there's no response, the script quits.
def pingTest(ip):
	if args.p:
        print("\033[1m" + "Ping Test" + "\033[0m")
        ping = os.system("ping -c 5 {}".format(ip))
        if ping == 0:
                print("\033[1m" + "Site is up, add Ping Check" + "\033[0m")
        else:
                print("\033[1m" + "Site down, ignore" + "\033[0m")
    else:
#SNMP Testing. Stuff that actually might matter.
#Testing begins here. First SNMP Test. Displays essentially a sh ver. Not fully documented in the Cisco OID Database.
#If there is no response due to no SNMP, the test will fail out here and the device is either not managable,
#or the SNMP Community has not been injected.

#Runs basic SNMP Test to see if the SNMP Community has been injected in to the device.
def snmpInjection(ip):
	if args.t:
        print ("\033[1m" + "Testing SNMP Community" + "\033[0m")
        testsnmp = subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.1.1.0".format(ip).split())
        if testsnmp == 0:
                print("\033[1m" + "SNMP Community Injected, Add Checks" + "\033[0m")
        else:
                print("\033[1m" + "SNMP Community Not Injected, Leave Ping Only" + "\033[0m")
	else:

#Runs SNMP Check for Interface Status OIDs. Uses the check_ifstatus nagios script.
def ifStatus(ip):
	if args.ifstatuscheck:
        print("\033[1m" + "Interface Status Sample Test" + "\033[0m")
        ifstatus = subprocess.call("/usr/lib/nagios/plugins/check_ifstatus -v2 -H {} -C SNMPCOMMUNITYHERE".format(ip).split())
        if ifstatus == 0:
                print("\033[1m" + "Interface Status Works, Add Check" + "\033[0m")
        else:
                print("\033[1m" + "Interface Status Failed, Do Not Add" + "\033[0m")
	else:

#Runs SNMP Check for CPU Status. Uses the SNMP Load nagios script.
def cpuStatusCheck(ip)
	if args.cpustatuscheck:
        print("\033[1m" + "CPU Status Sample Test" + "\033[0m")
        cpustatus = subprocess.call("/usr/lib/nagios/plugins/check_snmp_load.pl -H {} -T cisco -C SNMPCOMMUNITYHERE -w 101,101,90 -c 102,102,95\n\n".format(ip).split())
        if cpustatus == 0:
                print("\033[1m" + "CPU Status Works, Add Check" + "\033[0m")
        else:
                print("\033[1m" + "CPU Status Failed, Do Not Add" + "\033[0m")
	else:

#Runs SNMP Check for Environment Status. Uses the SNMP Environment nagios script.
def envStatus(ip):
	if args.envstatuscheck:
        print("\033[1m" + "Environment Status Sample Test" + "\033[0m")
        envstatus = subprocess.call("/usr/lib/nagios/plugins/check_snmp_env.pl -H {} -T cisco -C SNMPCOMMUNITYHERE\n\n".format(ip).split())
        if envstatus == 0:
                print("\033[1m" + "Environment Status Works, Add Check" + "\033[0m")
        else:
                print("\033[1m" + "Environment Status Failed, Do Not Add" + "\033[0m")
	else:

#Runs Interface Error Test. Uses the Interface Errors nagios script.
def ifErrors(ip):
	if args.iferrorcheck:
        print("\033[1m" + "Interface Error Sample Test" + "\033[0m")
                iferror = subprocess.call("/usr/lib/nagios/plugins/check_iferrors -H {} -C SNMPCOMMUNITYHERE -w 300\n\n".format(ip).split())
        if iferror == 0:
                print("\033[1m" + "Interface Errors Works, Add Check" + "\033[0m")
        else:
                print("\033[1m" + "Interface Errors Failed, Do Not Add" + "\033[0m")
	else:

#Prints the Full List of Interfaces
def listInterfaces(ip):
	if args.iflist:
        print("\033[1m" + "Printing Full List of Interfaces" + "\033[0m")
        intlistfull = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.2".format(ip).split())
    else:

#Prints the Full List of Physical Interfaces 
def listAllPhysicalInterfaces(ip):
	if args.iflistphys:        
        print("\033[1m" + "Printing Full List of Physical Interfaces" + "\033[0m")
        intlistphys = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.2 | grep 'FastEthernet\|GigabitEthernet\|Serial\|Ethernet\|Cellular\|Stack\|TenGigabitEthernet\|ATM'".format(ip), shell=True)
	else:

#Prints the Full List of Virtual Interfaces regardless of whether it's down or not
def listAllVirtualInterfaces(ip):
	if args.iflistvirt:
        print("\033[1m" + "Printing Full List of Virtual Interfaces" + "\033[0m")
        intlistvirt = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.2 | grep 'Multilink\|Port-channel\|Vlan\|Embedded-Service-Engine\|Loopback'".format(ip), shell=True)
	else:

#Prints the Full List of Up Physical and Virtual Interfaces
def listPhysicalAndVirtualInterfacesUp(ip):
	if args.iflistallup:
        print("\033[1m" + "Printing Full List of Enabled Interfaces" + "\033[0m")
        intlisten = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.8 | grep 'INTEGER: 1' > intlist".format(ip), shell=True)
        outintlist = subprocess.call("cat intlist", shell=True)
	else:
		
#Prints the Full List of Interface Descriptions
def listInterfaceDescriptions(ip):
	if args.ifdesc:
        print("\033[1m" + "Printing Full List of Interface Descriptions" + "\033[0m")
        intlistdesc = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.31.1.1.1.18 > intlistdesc".format(ip), shell=True)
        outintlistdesc = subprocess.call("cat intlistdesc", shell=True)
	else:
		
#Prints the current Status Type of All Interfaces
def printAllInterfaceStatuses(ip):
	if args.ifstatuses:
        print("\033[1m" + "Printing Status of All Interfaces" + "\033[0m")
        intlistallstatus = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.8 > intlistallstatus && sed -i 's/INTEGER: 1/Up/g' intlistallstatus && sed -i 's/INTEGER: 2/Down/g' intlistallstatus && sed -i 's/INTEGER: 3/Testing/g' intlistallstatus && sed -i 's/INTEGER: 4/Unknown/g' intlistallstatus && sed -i 's/INTEGER: 5/NotPresent/g' intlistallstatus && sed -i 's/INTEGER: 7/LowerLayerDown/g' intlistallstatus".format(ip), shell=True)
        outintlistallstatus = subprocess.call("cat intlistallstatus", shell=True)
	else:
		
#Prints the full list of Up/Up Interfaces
def printOnlyUpUpInterfaces(ip):
	if args.ifstatusup:
        print("\033[1m" + "Printing Status of All Up Interfaces" + "\033[0m")
        intlistupstatus = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.8 > intlistupstatus".format(ip), shell=True)
        commaintlist = subprocess.call("grep -oP '(?<=\d\.)\d+(?= = INTEGER: 1)' intlistupstatus | paste -s -d , >> csv && cat intlistupstatus", shell=True)
	else:
		
#Prints a Comma Separated List of Integers for all Enabled Interfaces
def printCSofEnabledInterfaces(ip):
	if args.ifupcs
        print("\033[1m" + "Printing comma separated integers for all Enabled Interfaces" + "\033[0m")
        commaintlist = subprocess.call("grep -oP '(?<=\d\.)\d+(?= = INTEGER: 1)' intlistupstatus | paste -s -d , >> csv", shell=True)
#        with open('csv', 'r') as in_file:
#                text = in_file.read()
#                print("\033[31;1m" + text + "\033[0;0m")
	else:
		
#Prints a Full List of Stack Ports
def printListOfStackPorts(ip):
	if args.liststackports:
        print("\033[1m" + "Printing Status of all Stack Ports" + "\033[0m")
        stacklist = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.4.1.9.9.500.1.2.2.1.1 > intliststackstatus".format(ip), shell=True)
        outintliststackstatus = subprocess.call("cat intliststackstatus", shell=True)
    else:

#Prints a Comma Separated List of Stack Ports that are up
def printCSListOfUpStackPorts(ip):
	if args.listupstackcs:
        print("\033[1m" + "Printing comma separated integers for all Up Stack Ports" + "\033[0m")
        commastackuplist = subprocess.call("grep -oP '(?<=\d\.)\d+(?= = INTEGER: 1)' intliststackstatus | paste -s -d , >> intliststackstatus && cat intliststackstatus", shell=True)
	else:
		
#Prints a Full List of Trunk Ports
def printListOfTrunkPorts(ip):
	if args.listtrunkports:
        print("\033[1m" + "Printing List of All Trunk Ports" + "\033[0m")
        trunklist = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.4.1.9.9.46.1.6.1.1.14 > intlisttrunkstatus".format(ip), shell=True)
        outintlisttrunkstatus = subprocess.call("cat intlisttrunkstatus", shell=True)
	else:
		
#Prints a Comma Separated List of Trunk Ports
def printCSListofUpTrunkPorts(ip):
	if args.listuptrunkcs:
        print("\033[1m" + "Printing a Comma Separated List of All Up Trunk Ports" + "\033[0m")
        commatrunklist = subprocess.call("grep -oP '(?<=\d\.)\d+(?= = INTEGER: 1)' intlisttrunkstatus | paste -s -d , intlisttrunkstatus && cat intlisttrunkstatus", shell=True)
#        with open ('csv', 'r') as in_file:
#                text = in_file.read()
#                print("\033[31;1m" + text + "\033[0;0m")
	else:
		
#Prints a Comma Separated List of All Trunk Ports
#       print("\033[1m" + "Printing comma separated integers for all Trunk Ports" + "\033[0m")
#       trunklist = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.4.1.9.9.46.1.6.1.1.14 > trunklist | grep "INTEGER: 1" trunklist | grep -oP '(?<=\d\.)\d+(?= = INTEGER)' stacklist | paste -s -d , >> trunkcsv", shell=True)
#       with open('csv', 'r') as in_file:
#               text = in_file.read()
#               print("\033[31;1m" + text + "\033[0;0m")

#Prints a Comma Separated List of All Trunk and Switch Ports
#       print("\033[1m" + "Printing comma separated integers for all Trunk and Switch Ports" + "\033[0m")  
#       trunkswitch = subprocess.call("echo ',' >> stackcsv && cat stackcsv >> trunkcsv", shell=True)

#    subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} iso.3.6.1.2.1.47.1.1.1.1.11.1".format(ip).split())
#    subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} iso.3.6.1.2.1.47.1.1.1.1.11.1001".format(ip).split())

#Remove all of the files created by this script
def cleanUpFiles:
        print("\033[1m" + "Cleaning Up" + "\033[0m")
        cleanup = subprocess.call("rm -f intlist && rm -f intlist* && rm -f *list && rm *csv && rm -f *csv", shell=True)
        #Default the script to a Cisco device.


#    if not args.c and not args.H:
#        args.c = True
#    if (args.c or args.H) and not args.s:
#        #runs with -c, -H
#        print("Running Checks")
#        run_checks(args.ip)
#    if args.H:
#        # runs with -H, -Hs
3        # runs with -H, -Hs
#        print("running HP")
#        hpserial(args.ip)
#    elif args.c:
#        # runs with -c, -s, and -cs
#        print("running Cisco")
#        ciscoserial(args.ip)
#    print("IP Address: {}".format(args.ip))

#Print Cisco Serial Number and IOS Info
def ciscoserial(ip):
	if args.c:
		print("\033[1m" + "Device:" + "\033[0m")
		subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} iso.3.6.1.2.1.1.1.0 | grep 'Cisco IOS'".format(ip), shell=True)
		subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} iso.3.6.1.2.1.47.1.1.1.1.11.1".format(ip).split())
		subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} iso.3.6.1.2.1.47.1.1.1.1.11.1001".format(ip).split())
	else:

def hpserial(ip):
	if args.H:
		subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.4.1.11.2.36.1.1.2.2.0".format(ip).split())
		print("Environment Status for ProCurve Does Not Work")
		print("Interface Status Check for ProCurve Does Not Work")
		print("Interface Errors Check for ProCurve Does Not Work")
	else:



