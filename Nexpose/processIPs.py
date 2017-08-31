#! /usr/bin/env python3
from __future__ import print_function
from __future__ import unicode_literals

# BLUF: MAC Address Counter for Rapid7 Nexpose discovery reports
# USE CASE: Often Nexpose discovery scans of vips, VMs, and hypervisors
# return results of duplicate MACs or no MAC at all. This tool provides
# insight into those numbers.
# AUTHOR: nxkennedy





import csv



def convert_ipv4(ip):

    return tuple(int(n) for n in ip.split('.'))



def check_ipv4_in(addr, start, end):

    return convert_ipv4(start) < convert_ipv4(addr) < convert_ipv4(end)



def csv_writer(sortedips):

    with open('qai-data/qai-processed-not-covered-ips.csv', 'w') as csvOutput:
        fieldnames = ['IP']
        writer = csv.DictWriter(csvOutput, fieldnames=fieldnames)
        # writer.writeheader() # we don't really need a header for this list
        for i in sortedips:
            writer.writerow({'IP': i})



def percentage(part, whole):
    return round(100 * float(part)/float(whole))



def final_output(foundCount, wasntFoundCount, wasntFoundips):

    sortedips = sorted(wasntFoundips)
    csv_writer(sortedips)

    print("___")
    print("\n> New IPs Covered by Old Ranges: {0} of {1}".format(foundCount, (foundCount + wasntFoundCount)))
    print("( {0} Not Covered - {1}% Visibility )".format(wasntFoundCount, percentage(foundCount, wasntFoundCount)))
    print("===")
    print("> For List of IPs Not Covered Check file: 'qai-data/qai-processed-not-covered-ips.csv'")
    print("===")
    print()



def read_ipv4():

    oldRanges = []
    foundCount = 0
    wasntFoundCount = 0
    wasntFoundips = []

    with open('foo.txt') as ipranges, open('foo.txt') as newips:

        print("\n[+] Comparing Newly Found IPs to Nexpose Scan Ranges...")

        for ips in ipranges:

            ranges = ips.split(',')

            for ipPair in ranges:
                oldRanges.append(ipPair.strip().split(' - ')) # Now ranges are in a list of lists: ['10.230.100.1', '10.230.100.254']

        for newip in newips:
            addr = newip.strip()

            for start, end in oldRanges:
                check = check_ipv4_in(addr, start, end)

            if check is False:
                wasntFoundips.append(addr)
                wasntFoundCount += 1
            else:
                foundCount += 1

    final_output(foundCount, wasntFoundCount, wasntFoundips)



def main():
    read_ipv4()



if __name__ == '__main__':
    main()
