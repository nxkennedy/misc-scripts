
import subprocess
import csv
import os
from tqdm import tqdm # for progress tracking




def convert_ipv4(ip):

    return tuple(int(n) for n in ip.split('.'))



def check_ipv4_in(ip, start, end):

    return convert_ipv4(start) < convert_ipv4(ip) < convert_ipv4(end)



def name_lookup(name):

    try:
        # Executing command 'host -t a [hostname] [nameserver]'
        lookup = subprocess.check_output(['host', '-t', 'a', name, '10.1.90.19']) # QAI nameserver
        output = lookup.decode('utf-8').strip().split() # puts output in list

        if output[11] == 'alias':
            name, ip = output[9], output[18] # parse output like awk
        else:
            name, ip = output[8], output[11]

        return name, ip

    except Exception as e:
        return name, 'NOT FOUND'



def format_ipv4_ranges():

    formattedRanges = []

    # First we need to do a little formatting on the ip ranges file, send contents to a list called formattedRanges
    with open('foo.txt') as ipRanges:

        for ips in ipRanges:
            ranges = ips.split(',')

            for ipPair in ranges:
                ipPair = ipPair.strip().split(' - ')
                formattedRanges.append(ipPair) # Now ranges are in a list of lists: ['10.230.100.1', '10.230.100.254']

    ########################""" Plugged in ad-hoc, remove normally
    with open('foo.txt') as ipRanges:

        for ips in ipRanges:
            ranges = ips.split(',')

            for ipPair in ranges:
                ipPair = ipPair.strip().split(' - ')
                formattedRanges.append(ipPair) # Now ranges are in a list of lists: ['10.230.100.1', '10.230.100.254']
    #########################"""

    return formattedRanges



def counter_for_progress_bar(filename):

    total = 0

    with open(filename) as counter:

        for i in counter:
            total += 1

    return total



def percentage(part, whole):

    return round(100 * float(part)/float(whole))



def compare_resolved_hosts_to_ipv4_ranges(): # the meat and potatoes

    foundIpCount = 0
    wasntFoundIpCount = 0
    formattedRanges = format_ipv4_ranges()

    # now we iterate through the ips of resolved hosts and compare
    with open('qai-data/qai-processed-names-with-ips.csv') as hostAndIps:

        for hostAndIp in hostAndIps:
            hostAndIp = hostAndIp.strip().split(',')
            name, ip = hostAndIp

            for start, end in formattedRanges: # for each single ip, compare it to each range before
                discovered = check_ipv4_in(ip, start, end)

                if discovered:
                    foundIpCount += 1
                    csv_writer(3, (name, ip))
                    break # if ip found, doesn't continue iterating through the rest of the ranges

            else: # not attached to the 'if', attached to the 'for'
                wasntFoundIpCount += 1
                csv_writer(4, (name, ip))

    print("\n> Hosts From Foreman Covered in Scanned Ranges: {0} of {1}".format(foundIpCount, (foundIpCount + wasntFoundIpCount)))
    print("( {0} Not Covered - {1}% Visibility )".format(wasntFoundIpCount, percentage(foundIpCount, (foundIpCount + wasntFoundIpCount))))
    print("===")
    print("> For Lists of Hosts Check: '*-names-covered.csv' and '*-names-not-covered.csv'")
    print("===\n")



def csv_writer(flag, resolvedName):

    name, ip = resolvedName
    fieldnames = ['Name', 'IP']

    env = 'qai' # fix this so that env is passed as a flag to the writer

    if flag == 1:
        filename = '{0}-data/{1}-processed-names-with-ips.csv'.format(env, env)
    elif flag == 2:
        filename = '{0}-data/{1}-processed-names-not-resolved.csv'.format(env, env)
    elif flag == 3:
        filename = '{0}-data/{1}-processed-names-covered.csv'.format(env, env)
    elif flag == 4:
        filename = '{0}-data/{1}-processed-names-not-covered.csv'.format(env, env)
    else:
        pass

    with open('{0}'.format(filename), 'a') as nameAndIps:
        writer = csv.DictWriter(nameAndIps, fieldnames=fieldnames)
        file_exists = os.path.isfile(filename) # wtf is this -_-

        if not file_exists:
            writer.writeheader()

        writer.writerow({'Name': name, 'IP': ip})



def resolve_hostnames():

    NamesFoundCount = 0
    NamesNotFoundCount = 0
    # count our file for our progress bar
    fileLen = counter_for_progress_bar('foo.txt')
    # qai-all-hostnames includes all hosts from the 'Owner' tab of praveen's file
    # qai-all-hostnames-ips is those names + ips
    # qai-all-hostnames-off are the names filtered (in excel) using 'OFF', 'Decomm', or 'Shutdown' in the 'Owner' tab of praveen's file
    with open('footxt') as nameFile:

        with tqdm(total=fileLen, desc='[-] Resolving Names') as progress: # progress bar

            for name in nameFile:
                name = name.strip()
                resolvedName = name_lookup(name)
                progress.update(1)

                if 'NOT FOUND' in resolvedName:
                    NamesNotFoundCount += 1
                    csv_writer(2, resolvedName) # we send a flag of int(2) to our csv_writer function
                else:
                    NamesFoundCount += 1
                    csv_writer(1, resolvedName)

    print("___")
    print("> {0} of {1} names resolved ( {2} not found )".format(NamesFoundCount, (NamesFoundCount + NamesNotFoundCount), (NamesNotFoundCount)))



def file_check():
    pass # for now. . .
    # output files already exist? would you like to delete them? Y/n



def main():

    # TODO
    #file_check(): # STEP 1, delete output files if they already exist

    print("\n[+] Comparing All Foreman Hostnames to Nexpose Scan Ranges...")
    resolve_hostnames() # STEP 2, resolve hostnames
    compare_resolved_hosts_to_ipv4_ranges() # STEP 3, compare the data



if __name__ == '__main__':
    main()
