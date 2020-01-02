# Description: Translates URL encoded SQLmap strings containing int ASCII codes to character values
# Example:
# -1208%20OR%206434%20IN%20%28SELECT%20%28CHAR%28113%29%2BCHAR%28107%29%2BCHAR%28122%29%2B 
# Translates to:
# -1208 OR 6434 IN (SELECT (q+k+z+
# Usage: python3 script.py in.csv out.csv
# Author: Nolan B. Kennedy (nxkennedy)
import urllib.parse
import re
import sys
import csv




try:
  with open(sys.argv[1]) as csvfile:
		with open(sys.argv[2], 'w', newline='') as csvfile2:
			print("[+] Working...")
			reader = csv.reader(csvfile)
			writer = csv.writer(csvfile2)
			for row in reader:
				row = row[0]
				
				# URL Decode
				url_decoded = urllib.parse.unquote(row)
				
				# find all the CHAR(foo)
				found = re.findall(r"[Cc][Hh][Aa][Rr]\(.*?\)", url_decoded)

				# convert the int CHAR(foo) to the ascii character equiv
				char_decoded = []
				for i in found:
					num = int(re.split(r'[\(\s\)]', i)[1])
					char_decoded.append(chr(num))

				# xcore magic ;)
				new = re.sub(r"[Cc][Hh][Aa][Rr]\(.*?\)", lambda match: str(char_decoded.pop(0)), url_decoded) 
				writer.writerow([new.encode('utf-8')]) # did the encode bit to play nice with windows
				#print("%s" % new.encode('utf-8'))
			
except Exception as e:
	print(e)

print("[+] Done!")
