#!/usr/bin/env python2.7
import os
import argparse
import sys
import subprocess

#Version 0.4d
def parse_args(arguments):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('ip', help='destination IP')
    client_method = parser.add_mutually_exclusive_group()
    client_method.add_argument('-c', help='Cisco tag', action='store_true')
    client_method.add_argument('-H', help='HP tag', action='store_true')
    parser.add_argument('-s', help='Obtain Serial Number', action='store_true')
    args = parser.parse_args(arguments)
    return args
#Testing for Validation Begins
def run_checks(ip):
        print("\033[1m" + "Running Test Checks for Validation" + "\033[0m")
        print("\033[1m" + "Ping Test" + "\033[0m")
#Ping Test. If there's no response, the script quits.
        ping = os.system("ping -c 1 {}".format(ip))
        if ping == 0:
                print("\033[1m" + "Site is up, add Ping Check" + "\033[0m")
        else:
                sys.exit("\033[1m" + "Site down, ignore" + "\033[0m")
#SNMP Testing. Stuff that actually might matter.
#Testing begins here. First SNMP Test. Displays essentially a sh ver. Not fully documented in the Cisco OID Database.
#If there is no response due to no SNMP, the test will fail out here and the device is either not managable,
#or the SNMP Community has not been injected.

#Runs basic SNMP Test to see if the SNMP Community has been injected in to the device.
        print ("\033[1m" + "Testing SNMP Community" + "\033[0m")
        testsnmp = subprocess.call("snmpget -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.1.1.0".format(ip).split())
        if testsnmp == 0:
                print("\033[1m" + "SNMP Community Injected, Add Checks" + "\033[0m")
        else:
                sys.exit("\033[1m" + "SNMP Community Not Injected, Leave Ping Only" + "\033[0m")

#Runs SNMP Check for Interface Status OIDs. Uses the check_ifstatus nagios script.
        print("\033[1m" + "Interface Status Sample Test" + "\033[0m")
        ifstatus = subprocess.call("/usr/lib/nagios/plugins/check_ifstatus -v2 -H {} -C SNMPCOMMUNITYHERE".format(ip).split())

#Runs SNMP Check for CPU Status. Uses the SNMP Load nagios script.
        print("\033[1m" + "CPU Status Sample Test" + "\033[0m")
        cpustatus = subprocess.call("/usr/lib/nagios/plugins/check_snmp_load.pl -H {} -T cisco -C SNMPCOMMUNITYHERE -w 101,101,90 -c 102,102,95\n\n".format(ip).split())

#Runs SNMP Check for Environment Status. Uses the SNMP Environment nagios script.
        print("\033[1m" + "Environment Status Sample Test" + "\033[0m")
        envstatus = subprocess.call("/usr/lib/nagios/plugins/check_snmp_env.pl -H {} -T cisco -C SNMPCOMMUNITYHERE\n\n".format(ip).split())

#Runs Interface Error Test. Uses the Interface Errors nagios script.
        print("\033[1m" + "Interface Error Sample Test" + "\033[0m")
        iferror = subprocess.call("/usr/lib/nagios/plugins/check_iferrors -H {} -C SNMPCOMMUNITYHERE -w 300\n\n".format(ip).split())

#Prints the Full List of Interfaces with their Type (Serial, Fa, Gi, etc)
        print("\033[1m" + "Printing Full List of Interfaces" + "\033[0m")
        intlistfull = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.2".format(ip).split())

#Prints the Full List of Physical Interfaces Regardless of whether it's down or not
        print("\033[1m" + "Printing Full List of Physical Interfaces" + "\033[0m")
        intlistphys = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.2 | grep 'FastEthernet\|GigabitEthernet\|Serial\|Ethernet\|Cellular\|Stack\|TenGigabitEthernet\|ATM'".format(ip), shell=True)

#Prints the Full List of Virtual Interfaces regardless of whether it's down or not
        print("\033[1m" + "Printing Full List of Virtual Interfaces" + "\033[0m")
        intlistvirt = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.2 | grep 'Multilink\|Port-channel\|Vlan\|Embedded-Service-Engine\|Loopback'".format(ip), shell=True)

#Prints the Full List of Physical and Virtual Interfaces
        print("\033[1m" + "Printing Full List of Enabled Interfaces" + "\033[0m")
        intlisten = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.8 | grep 'INTEGER: 1' > intlist".format(ip), shell=True)
        outintlist = subprocess.call("cat intlist", shell=True)

#Prints the Full List of Interface Descriptions
        print("\033[1m" + "Printing Full List of Interface Descriptions" + "\033[0m")
        intlistdesc = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.31.1.1.1.18 > intlistdesc".format(ip), shell=True)
        outintlistdesc = subprocess.call("cat intlistdesc", shell=True)

#Prints the current Status of All Interfaces
        print("\033[1m" + "Printing Status of All Interfaces" + "\033[0m")
        intlistallstatus = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.8 > intlistallstatus && sed -i 's/INTEGER: 1/Up/g' intlistallstatus && sed -i 's/INTEGER: 2/Down/g' intlistallstatus && sed -i 's/INTEGER: 3/Testing/g' intlistallstatus && sed -i 's/INTEGER: 4/Unknown/g' intlistallstatus && sed -i 's/INTEGER: 5/NotPresent/g' intlistallstatus && sed -i 's/INTEGER: 7/LowerLayerDown/g' intlistallstatus".format(ip), shell=True)
        outintlistallstatus = subprocess.call("cat intlistallstatus", shell=True)
   
#Prints the full list of Up/Up Interfaces
        print("\033[1m" + "Printing Status of All Up Interfaces" + "\033[0m")
        intlistupstatus = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.2.1.2.2.1.8 > intlistupstatus".format(ip), shell=True)
        outintlistupstatus = subprocess.call("cat intlistupstatus", shell=True)

#Prints a Comma Separated List of Integers for all Enabled Interfaces
        print("\033[1m" + "Printing comma separated integers for all Enabled Interfaces" + "\033[0m")
        commaintlist = subprocess.call("grep -oP '(?<=\d\.)\d+(?= = INTEGER)' intlistupstatus | paste -s -d , >> csv")
        with open('csv', 'r') as in_file:
                text = in_file.read()
                print("\033[31;1m" + text + "\033[0;0m")
       
#Prints a Full List of Stack Ports
        print("\033[1m" + "Printing Status of all Stack Ports" + "\033[0m")
        stacklist = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.4.1.9.9.500.1.2.2.1.1 > intliststackstatus".format(ip), shell=True)
        outintliststackstatus = subprocess.call("cat intliststackstatus", shell=True)
   
#Prints a Comma Separated List of Stack Ports that are up
        print("\033[1m" + "Printing comma separated integers for all Up Stack Ports" + "\033[0m")
        commastackuplist = subprocess.call("grep -oP '(?<=\d\.)\d+(?= = INTEGER: 1)' intliststackstatus | paste -s -d , >> stackcsv")
        with open('csv', 'r') as in_file:
                text = in_file.read()
                print("\033[31;1m" + text + "\033[0;0m")
   

#Prints a Comma Separated List of All Stack Ports
#       print("\033[1m" + "Printing comma separated integers for all Stack Ports" + "\033[0m")
#       commalist = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.4.1.9.9.500.1.2.2.1.1 > stacklist | grep "INTEGER: 1" stacklist | grep -oP #'(?<=\d\.)\d+(?= = INTEGER)' stacklist | paste -s -d , >> stackcsv", shell=True)
#       with open('csv', 'r') as in_file:
#               text = in_file.read()
#               print("\033[31;1m" + text + "\033[0;0m")

#Prints a Full List of Trunk Ports
        print("\033[1m" + "Printing List of All Trunk Ports" + "\033[0m")
        trunklist = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.4.1.9.9.46.1.6.1.1.14 > intlisttrunkstatus".format(ip))
        outintlisttrunkstatus = subprocess.call("cat intlisttrunkstatus", shell=True)
                   
#Prints a Comma Separated List of Trunk Ports
        print("\033[1m" + "Printing a Comma Separated List of All Up Trunk Ports" + "\033[0m")
        commatrunklist = subprocess.call("grep -oP '(?<=\d\.)\d+(?= = INTEGER: 1)' intlisttrunkstatus | paste -s -d , trunkcsv")
        with open ('csv', 'r') as in_file:
                text = in_file.read()
                print("\033[31;1m" + text + "\033[0;0m")

#Prints a Comma Separated List of All Trunk Ports
#       print("\033[1m" + "Printing comma separated integers for all Trunk Ports" + "\033[0m")
#       trunklist = subprocess.call("snmpbulkwalk -v2c -c SNMPCOMMUNITYHERE {} 1.3.6.1.4.1.9.9.46.1.6.1.1.14 > trunklist | grep "INTEGER: 1" trunklist | grep -oP '(?<=\d\.)\d+(?= = INTEGER)' stacklist | paste -s -d , >> trunkcsv", shell=True)
#       with open('csv', 'r') as in_file:
#               text = in_file.read()
#               print("\033[31;1m" + text + "\033[0;0m")

#Prints a Comma Separated List of All Trunk and Switch Ports
#       print("\033[1m" + "Printing comma separated integers for all Trunk and Switch Ports" + "\033[0m")  
#       trunkswitch = subprocess.call("echo ',' >> stackcsv && cat stackcsv >> trunkcsv", shell=True)
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

#Remove all of the files created by this script
        print("\033[1m" + "Cleaning Up" + "\033[0m")
        cleanup = subprocess.call("rm -f intlist && rm -f intlist* && rm -f *list && rm *csv && rm -f *csv", shell=True)

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

        #Default the script to a Cisco device.
    if not args.c and not args.H:
        args.c = True
    if (args.c or args.H) and not args.s:
        #runs with -c, -H
        print("Running Checks")
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
