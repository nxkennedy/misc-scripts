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
# python3 remote-ssh-yumUpdate.py scanengs.txt
#
#
#**********************#

import sys
from pexpect import pxssh, TIMEOUT, EOF, spawn
import getpass
from termcolor import colored



def main(hostFile=sys.argv[1]):

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
    print(colored("[+] Testing " + str(fcount) + " hosts. . .\n", "yellow"))
    # loop to login to each box. Reads from arg file
    with open(hostFile) as f2:
        for hostname in f2:
            s = pxssh.pxssh()
            try:
                print('[*] Logging into ' + hostname.strip())
                s.login(hostname, username, password)
                # standard yum update
                print('[*]' + colored(' SUCCESS.', 'green') + colored(' Trying sudo. . .', attrs=['blink']), end='\r')
                s.sendline('sudo yum -y update')
                s.prompt()
                s.sendline(password)
                print(colored('[*] Updating host. . .', 'yellow'),  end='\r')
                s.prompt()
                s.sendline('sudo yum --enablerepo=updates -y update --security')
                print(colored('[*] Applying security specific patches. . .', 'yellow'), end='\r')
                s.prompt()
                # Checking the installed kernel to determine if reboot needed
                s.sendline("rpm -q --last kernel | awk '{print $1}' |head -1 |sed 's/kernel-//'")
                s.prompt
                installed_kernel = s.before.decode('utf-8').strip()
                s.sendline('uname -r')
                s.prompt()
                running_kernel = s.before.decode('utf-8').strip()
                s.logout()
                s.close()

                print(colored('[*] ' + hostname.strip() + ' update complete.', 'green'))
                if installed_kernel != running_kernel:
                    print(colored('[!] REBOOT REQUIRED FOR KERNEL ' + installed_kernel + '\n' + running_kernel, 'red'))
                count += 1
                # print remaining host count to screen for progress
                if fcount - count == 1:
                    print(colored('[+] ' + str(fcount - count) + ' host remaining' + '\n', 'magenta'))
                elif fcount - count == 0:
                    print(colored('\n[+] FINISHED. ' + str(fcount) + ' hosts updated\n', 'magenta'))
                else:
                    print(colored('[+] ' + str(fcount - count) + ' hosts remaining\n', 'magenta'))



            # print exception to screen
            except pxssh.ExceptionPxssh as e:
                print(colored('[-] Pxssh failed on login', 'red'))
                print(colored(str(e), 'red'))
                pass



if __name__ == '__main__':
    main()
