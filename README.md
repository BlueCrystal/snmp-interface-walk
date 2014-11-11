<h2>SNMP Script used for pulling info from Networking Equipment</h2>

This module is built for Python 2.7.

This script assumes the scripts used in the script are located at /usr/lib/nagios/plugins/. You may need to adjust based on your installation.

<h3>Script Dependencies:</h3>
<pre>
  check_ifstatus - https://nagios-plugins.org/doc/man/check_ifstatus.html
  check_snmp_load - http://nagios.manubulon.com/snmp_load.html
  check_snmp_env - http://nagios.manubulon.com/snmp_env.html
  check_iferrors - https://git.netways.org/plugins/collection/blobs/438dd1e53cb629e3e7d0f6c94c85cb9b9738313a/plugins/check_iferrors/trunk/check_iferrors.pl
  snmpbulkwalk
  snmpwalk
  snmpget
  ping
  Python 2.7
  Perl >=5.14.2</pre>
  
<h2>Usage:</h2>
Using no flags assumes that you are wanting to use standard Cisco OIDs for obtaining information and a serial number.

<h2>Help:</h2>
<pre>
./snmp.py -h
usage: snmp.py [-h] [-c | -H] [-s] ip

positional arguments:
  ip          destination IP

optional arguments:
  -h, --help  show this help message and exit
  -c          Cisco tag
  -H          HP tag
  -s          Obtain Serial Number
</pre>


By default, the following will be ran:
<li>  * Count of 5 Ping Test
  * Tests if the SNMP Community is Injected by Running an SNMP Check that displays the   * Equipment Model, the IOS type, and the IOS version.
  * Runs SNMP Check for Interface Status
  * Runs SNMP Check for CPU Status
  * Runs SNMP Check for Environment Status
  * Runs SNMP Check for Interface Errors
  * Runs SNMP Cisco Memory Test for SNMP verification.
  * Prints a List of all Stack Ports
  * Prints a Comma Separated List of Stack Ports that are Up/Up.
  * Prints a Full List of Trunk Ports.
  * Prints a Comma Separated List of Trunk Ports that are Up/Up.
  * Prints a Full List of Interfaces with their Interface Type (Serial, FastEthernet, GigabitEthernet, etc.)
  * Prints a Full List of Physical Interfaces Regardless of Whether the Interface is Down or Up (includes FastEthernet, GigabitEthernet, Serial, Ethernet, Cellular, Stack, TenGigabitEthernet, and ATM.)
  * Prints a Full List of Physical and Virtual Interfaces that are Up/Up
  * Prints a Full List of Interface Descriptions if Descriptions have been placed on the Interface.
  * Prints the current Status of All Interfaces.
  * Prints the full list of Up/Up Interfaces.
  * Prints a Comma Separated List of Integers for all Enabled Interfaces.
  * Prints a Full List of Stack Ports.
  * Cleans up files that were created during checks.
  * Checks for the device serial number assuming a Cisco device is used by default.
  * Can check for the device serial number assuming an HP device flag is used.</li>

<h2>Example Usage:</h2>
<pre>
$./snmp 10.165.182.58
running checks
Running Test Checks for Validation
Ping Test
PING 10.165.182.58 (10.165.182.58) 56(84) bytes of data.
[  1/1     0%] 64 bytes from 10.165.182.58: seq=1 ttl=243 time=220 ms

--- 10.165.182.58 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 220.011/220.011/220.011/0.000 ms
Site is up, add Ping Check
Testing SNMP Community
iso.3.6.1.2.1.1.1.0 = STRING: "Cisco IOS Software, C2960 Software (C2960-LANLITEK9-M), Version 12.2(55)SE5, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2012 by Cisco Systems, Inc.
Compiled Thu 09-Feb-12 19:11 by prod_rel_team"
SNMP Community Injected, Add Checks
Interface Status Sample Test
CRITICAL: host '10.165.182.58', interfaces up: 4, down: 7, dormant: 0, excluded: 0, unused: 0<BR>FastEthernet0/8: down <BR>FastEthernet0/3: down <BR>FastEthernet0/7: down <BR>
 |up=4,down=7,dormant=0,excluded=0,unused=0
CPU Status Sample Test
Argument "v6.0.1" isn't numeric in numeric lt (<) at /usr/lib/nagios/plugins/check_snmp_load.pl line 414.
CPU : 5 5 5 : OK
Environment Status Sample Test
1 ps OK : OK
Interface Error Sample Test
UNKNOWN: History file not found. Waiting until History is built
Printing Full List of Interfaces
iso.3.6.1.2.1.2.2.1.2.1 = STRING: "Vlan1"
iso.3.6.1.2.1.2.2.1.2.10001 = STRING: "FastEthernet0/1"
iso.3.6.1.2.1.2.2.1.2.10002 = STRING: "FastEthernet0/2"
iso.3.6.1.2.1.2.2.1.2.10003 = STRING: "FastEthernet0/3"   
iso.3.6.1.2.1.2.2.1.2.10004 = STRING: "FastEthernet0/4"
iso.3.6.1.2.1.2.2.1.2.10005 = STRING: "FastEthernet0/5"
iso.3.6.1.2.1.2.2.1.2.10006 = STRING: "FastEthernet0/6"
iso.3.6.1.2.1.2.2.1.2.10007 = STRING: "FastEthernet0/7"
iso.3.6.1.2.1.2.2.1.2.10008 = STRING: "FastEthernet0/8"
iso.3.6.1.2.1.2.2.1.2.10101 = STRING: "GigabitEthernet0/1"
iso.3.6.1.2.1.2.2.1.2.10501 = STRING: "Null0"
Printing Full List of Physical Interfaces
iso.3.6.1.2.1.2.2.1.2.10001 = STRING: "FastEthernet0/1"
iso.3.6.1.2.1.2.2.1.2.10002 = STRING: "FastEthernet0/2"
iso.3.6.1.2.1.2.2.1.2.10003 = STRING: "FastEthernet0/3"
iso.3.6.1.2.1.2.2.1.2.10004 = STRING: "FastEthernet0/4"
iso.3.6.1.2.1.2.2.1.2.10005 = STRING: "FastEthernet0/5"
iso.3.6.1.2.1.2.2.1.2.10006 = STRING: "FastEthernet0/6"
iso.3.6.1.2.1.2.2.1.2.10007 = STRING: "FastEthernet0/7"
iso.3.6.1.2.1.2.2.1.2.10008 = STRING: "FastEthernet0/8"
iso.3.6.1.2.1.2.2.1.2.10101 = STRING: "GigabitEthernet0/1"
Printing Full List of Enabled Interfaces
iso.3.6.1.2.1.2.2.1.8.1 = INTEGER: 1
iso.3.6.1.2.1.2.2.1.8.10002 = INTEGER: 1
iso.3.6.1.2.1.2.2.1.8.10101 = INTEGER: 1
iso.3.6.1.2.1.2.2.1.8.10501 = INTEGER: 1
Printing comma separated integers for all Enabled Devices
1,10002,10101,10501

SNMP Community Injected, Add Checks
Interface Status Works, Add Check
CPU Status Works, Add Check
Environment Status Works, Add Check  
Interface Errors Failed, Do Not Add
Cleaning Up
running Cisco
Device:
iso.3.6.1.2.1.1.1.0 = STRING: "Cisco IOS Software, C2960 Software (C2960-LANLITEK9-M), Version 12.2(55)SE5, RELEASE SOFTWARE (fc1)
iso.3.6.1.2.1.47.1.1.1.1.11.1 = No Such Instance currently exists at this OID
iso.3.6.1.2.1.47.1.1.1.1.11.1001 = STRING: "ABC1234D5EF"
IP Address: 10.165.182.58
</pre></li>


<u>This script was more or less written by @liliff and @Fugiman after bugging them night after night. I just threw in other commands I needed.</u>
