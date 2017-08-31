#!/usr/bin/env python3
###########################################################################
#
# [+] Description: Generic pxssh script for remote command execution
# on a list of hosts via ssh. Handles auth with getpass and prints output
# in color.
# [+] Use Case: updates, log retrieval, monitoring, service restarts, etc.
#
#                       ~ Written by nxkennedy ~
###########################################################################

#******** Usage ********#
# python remote-ssh.py hosts.txt
#
#
#**********************#

import sys
from pexpect import pxssh
import getpass
from termcolor import colored



def main(hostFile=sys.argv[1]):

    try:
        hostFile = hostFile
        # login interactively
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        # count lines in input file
        fcount = 0
        with open(hostFile) as f1:
            for lines in f1:
                fcount += 1
        #start update
        count = 0
        print(colored("[+] Attempting to update " + str(fcount) + " hosts. . .\n", "yellow"))
        # loop to login to each box. Reads from arg file
        with open(hostFile) as f2:
            for hostname in f2:
                s = pxssh.pxssh()
                print("[*] Logging in to " + hostname.strip("\n"))
                s.login(hostname, username, password)
                print(colored("[*] Sucessfully logged in! ", "green") + "Update in progress. . . ")
                # standard yum update
                s.sendline('sudo yum -y update')
                s.prompt()
                # password sent again for sudo
                s.sendline(password)
                s.prompt()
                print(s.before)
                s.sendline('sudo yum --enablerepo=updates -y update --security')
                s.prompt()
                print(s.before)
                s.logout()
                print(colored("[*] " + hostname.strip("\n") + " updated! ", "green"))
                count += 1
                # print remaining host count to screen for progress
                if fcount - count == 1:
                    print(colored("[+] " + str(fcount - count) + " host remaining" + "\n", "magenta"))
                else:
                    print(colored("[+] " + str(fcount - count) + " hosts remaining" + "\n", "magenta"))
                s.close()


    # print exception to screen
    except pxssh.ExceptionPxssh as e:
        print(colored("[-] Pxssh failed on login", "red"))
        print(colored(str(e), "red"))



if __name__ == '__main__':
    main()
