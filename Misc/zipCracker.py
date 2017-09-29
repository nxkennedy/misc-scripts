# Runs a dictionary attack against a zip file. You will be prompted for the zip file name at runtime.
# ** This is an expansion of the script authored by TJ. O'Connor in Violent Python **
# Usage: python zipCracker.py
# Author: nxkennedy

from __future__ import print_function
from threading import Thread
import zipfile
import sys
from time import time



FLAG = False

def extractFile(zFile, password):
	global FLAG # sue me
	try:
		zFile.extractall(pwd=password)
		sys.stdout.write('\033[1;32m') # change output to green
		print('\n\n[*] Found password: {0}\n'.format(password))
		sys.stdout.write('\033[0;0m') # resets to default text color
		FLAG = True
	except:
		pass

def main():
	zFile = zipfile.ZipFile(raw_input('Enter zipfile to crack: '))
	passFile = open('/usr/share/wordlists/rockyou.txt') # standard wordlist on Kali
	count = 0
	print('\n[+] Attempting to crack...')
	for line in passFile.readlines():
		if FLAG:
			break
		password = line.strip('\n')
		t = Thread(target=extractFile, args=(zFile, password))
		t.start()
		count += 1
		print('[+] Passwords tested: {0}'.format(str(count)), end='\r')

if __name__ == '__main__':
	start = time()
	main()
	finish = time()
	print('Completed in {0} sec {1}'.format(round(finish-start, 2), ' ' * 15)) # round our time and add spaces
