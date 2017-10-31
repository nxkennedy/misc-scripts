import datetime
import webbrowser
import sys

print "\n[+] Shmoocon Front of the Line Pass"
print "[+] Author: Nolan Kennedy (nxkennedy)"

if len(sys.argv) > 1:
	print "\n[+] Description:\n\tThis script will open a new browser window at a predetermined \n\ttime to hopefully get a spot in the shmoocon ticket queue."
	print "[+] Usage: Requires no args!\n\t'python shmoofotlp.py'\n"
	exit(0)

print "\n[-] Waiting to jump in line for tickets at the strike of noon..."
while True:
	if datetime.datetime(2017, 11, 1, 12) == datetime.datetime.now():
		webbrowser.open_new("http://landing.shmoocon.org/")
		print "[+] Quick! A browser window just opened! Go claim your tickets!"