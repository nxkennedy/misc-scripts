#! /usr/bin/env python3
from __future__ import print_function
from __future__ import unicode_literals

# BLUF: MAC Address Counter for Rapid7 Nexpose discovery reports
# USE CASE: Often Nexpose discovery scans of vips, VMs, and hypervisors
# return results of duplicate MACs or no MAC at all. This tool provides
# insight into those numbers.
# AUTHOR: ~ teh spearow ~

# !!! IMPORTANT !!! THIS SCRIPT WAS BUILT TO PROCESS A CSV REPORT GENERATED WITH THE FOLLOWING NEXPOSE SQL QUERY:
"""

SELECT mac_address AS "MAC", da.ip_address AS "IP", host_name AS "Host Name", dos.description AS "OS", dht.description AS "Host Type"
FROM fact_asset_discovery
  JOIN dim_asset da USING (asset_id)
  JOIN dim_operating_system dos USING (operating_system_id)
  JOIN dim_host_type dht USING (host_type_id)


"""



from collections import Counter
import csv
from sys import argv
from subprocess import call


script, infile1, infile2 = argv

def percentage(part, whole):
    return round(100 * float(part)/float(whole))

def csv_reader(infile1, infile2):

    try:
        # infile1 should be the old scan, infile2 should be recent scan
        with open(infile1) as csvfile1, open(infile2) as csvfile2:

            csvReader1 = csv.DictReader(csvfile1)
            csvReader2 = csv.DictReader(csvfile2)

            newIPs = []
            notFoundInNewList = []
            infile1Contents = []
            infile2Contents = []
            sameIP = 0
            newIP = 0
            infile1Count = 0
            infile2Count = 0
            notFoundInNew = 0

            print("\n[+] Comparing IPs in {0} to {1}...".format(infile1, infile2))

            for row in csvReader1:
                infile1Count += 1
                infile1Contents.append(row['IP'])

            for row2 in csvReader2:
                infile2Count += 1
                infile2Contents.append(row2['IP'])

            for ip in infile1Contents:

                if ip not in infile2Contents:
                    notFoundInNew += 1
                    notFoundInNewList.append(ip)
                else:
                    sameIP += 1

            for ip2 in infile2Contents:

                if ip2 not in infile1Contents:
                    newIP += 1
                    newIPs.append(ip2)
        print("___")
        print("> Total IPs in {0}: {1} <- Scan With Old Ranges".format(infile1, infile1Count))
        print("> Total IPs in {0}: {1} <- Newer Scan with Additional Ranges".format(infile2, infile2Count))
        print("> Old IPs Decom'd From {0}: {1} <- IPs No Longer Active".format(infile1, notFoundInNew))
        print("\n> New IPs Found: {0} of {1}".format(newIP, (newIP + sameIP)))
        print("( {0}% of Recently Scanned IPs are New IPs )".format(percentage(newIP, (newIP + sameIP))))
        print("===")
        print("> For List of New IPs Check 'qai-data/qai-processed-new-ips.txt'")
        print("===\n")
        #print("List of new IPs:\n", newIPs)


    except Exception as e:
        print(e)


    with open('qai-data/qai-processed-new-ips.txt', 'w') as writer:

        for x in newIPs:
            writer.write(x + '\n')

if __name__ == '__main__':

    csv_reader(infile1, infile2)
    call(["python3", "processIps.py"])
    call(["python3", "processHostnames.py"])
    call(["python3", "processOffHostnames.py"])
