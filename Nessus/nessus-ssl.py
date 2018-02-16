#!/usr/bin/env python3
#
# Description: This script parses a Nessus csv report and flags hosts using vulnerable 
# TLS/SSL versions and ciphers. Currently looks for SSLv2, SSLv3, DES, 3DES, RC4. 
# Provides final tally and writes findings to csv.
#
# Use case: Meeting compliance standards. Builds an actionable report for engineers to implement fixes.
#
# Author: Nolan Kennedy (nxkennedy)
#
# Usage: nessus-ssl.py <nessus-report.csv>
#
# Don't be mad that this is a flat script! 
#
import csv
import sys




# Nessus Plugin
# 21643: SSL Cipher Suites Supported
plugin = '21643'

# final list of dicts for our csv writer
final = []

# counters
analyzed_svcs = 0
affected = 0
sslv2  = 0
sslv3  = 0
des = 0
tripdes = 0
rc4 = 0

### Our help
if '.csv' not in sys.argv[1]:
	print('USAGE: %s <nessus-report.csv>' % sys.argv[0])
	exit(0)


### Reader
print("[+] Reading from file...")
with open(sys.argv[1]) as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
			# we collect each line of findings as a dict
			findings = {'Host' : '',
			'Port' : '',
			'SSLv2' : '',
			'SSLv3' : '',
			'DES' : '',
			'3DES' : '',
			'RC4' : '',
			'Raw Output' : '',}

			# if we see an "SSL / TLS Versions Supported" plugin
			if row['Plugin ID'] == plugin:
				# we scan the nessus plugin output for key words
				for line in row['Plugin Output'].splitlines():
					
					# SSLv2 check
					if 'SSL Version : SSLv2' in line:
						findings['SSLv2'] = 'X'
						sslv2 += 1
					
					# SSLv3 check
					if 'SSL Version : SSLv3' in line:
						findings['SSLv3'] = 'X'
						sslv3 += 1
					
					# DES check
					if 'Enc=DES' in line:
						findings['DES'] = 'X'
						des += 1
					
					# 3DES check
					if 'Enc=3DES' in line:
						findings['3DES'] = 'X'
						tripdes += 1
					
					# RC4 check	
					if 'Enc=RC4' in line:
						findings['RC4'] = 'X'
						rc4 += 1
						
					findings['Host'] = row['Host']
					findings['Port'] = row['Port']
					findings['Raw Output'] = row['Plugin Output']
				
				if 'X' in findings.values():
					final.append(findings)
					affected += 1
				
				analyzed_svcs += 1


### Writer
outfile = sys.argv[1].split('.')[0] + '-parsed.csv'
print("[+] Writing to %s" % outfile)
fieldnames = ['Host', 'Port', 'SSLv2', 'SSLv3', 'DES', '3DES', 'RC4', 'Raw Output']
with open(outfile, 'w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for f in final:
		writer.writerow(f)


### Output
print("\nTotal Services Analyzed: %s" % analyzed_svcs)
print("Total Services Affected: %s" % affected)
print("Total Findings: %s" % (sslv2 + sslv3 + des + tripdes + rc4))
print("-> SSLv2: %s" % sslv2)
print("-> SSLv3: %s" % sslv3)
print("-> DES: %s" % des)
print("-> 3DES: %s" % tripdes)
print("-> RC4: %s" % rc4)
