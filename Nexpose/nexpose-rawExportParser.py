#! /usr/bin/env python3
from __future__ import print_function
from __future__ import unicode_literals

"""

[+] Description: csv parsing script for "raw export" report from Nexpose. Script splits critical, severe, & moderate vulns by severity score into separate files with only necessary columns for remediation teams.
[+] ***meant to be a cleaner version of the other "working" parser
[+] Author: nxkennedy

[+] Usage: python3 nexpose-rawExportParser.py

"""

import os
import csv
import datetime
from tabulate import tabulate
from termcolor import colored




def terminal_output(outputDataCollection): # final output formatting

    scum ="""
            Vulnerable scum!
            /
    /\\︿╱\\
    \\0_ 0 /╱\\╱
    \\▁︹_/
    """
    fmtHeadingReport = colored("Report", "magenta")
    fmtHeadingCritical = colored("Critical", "red")
    fmtHeadingSevere = colored("Severe", "yellow")
    fmtHeadingModerate = colored("Moderate", "cyan")
    print("\n" + scum)
    print(tabulate(outputDataCollection, headers=[fmtHeadingReport, fmtHeadingCritical, fmtHeadingSevere, fmtHeadingModerate], tablefmt='fancy_grid') + "\n")



def csv_writing_formatter(csvReportName, readCsvRow, severity):

    now = datetime.date.today()
    fieldnames = [
        "Site Name",
        "Asset IP Address",
        "Asset Name",
        "Service Port",
        "Service Name",
        "Vulnerability CVE IDs",
        "Vulnerability Title",
        "Vulnerability Description",
        "Vulnerability Proof",
        "Vulnerability Solution",
    ]

    with open('reports/{0}/{1}-{2}-{3}.csv'.format(now, now, csvReportName.strip('.csv'), severity), 'a+') as someSeverityFile:
        writer = csv.DictWriter(someSeverityFile, fieldnames=fieldnames)

        if someServerityFile[0] == '':
            writer.writeheader()

        writer.writerow({
            'Site Name': readCsvRow[1],
            'Asset IP Address' : readCsvRow[2],
            'Asset Name' : readCsvRow[3],
            'Service Port' : readCsvRow[5],
            'Service Name': readCsvRow[6],
            'Vulnerability CVE IDs' : readCsvRow[9],
            'Vulnerability Title' : readCsvRow[10],
            'Vulnerability Description' : readCsvRow[11],
            'Vulnerability Proof' : readCsvRow[12],
            'Vulnerability Solution' : readCsvRow[13],
        })



def csv_writer(csvReportName, csvdata, severity):

    if severity == 'critical':
        csv_writing_formatter(csvReportName, csvdata, severity)
    elif severity == 'severe':
        csv_writing_formatter(csvReportName, csvdata, severity)
    elif severity == 'moderate':
        csv_writing_formatter(csvReportName, csvdata, severity)
    else:
        print("UNKNOWN SEVERITY")
        exit(1)


def file_count():
    csvCount = 0

    for report in os.listdir('.'):
        if not report.endswith('.csv'):
            continue
        csvCount +=1
    return csvCount


def csv_reader(csvReport):

    criticalScores = ["8", "9", "10"]
    severeScores = ["4", "5", "6", "7"]
    moderateScores = ["1", "2", "3"]
    # Initialize counters
    criticalCount = 0
    severeCount = 0
    moderateCount = 0
    outputDataCollection = []
    csvProgress = 1 # start at 1 because we're already on a file
    csvCount = file_count()


    with open(csvReport) as csvfile:
        readCSV = list(csv.reader(csvfile))
        lineCount = 0
        for lines in readCSV:
            lineCount += 1
        reportLength = lineCount
        print(colored('Processing File [{0}/{1}]: '.format(csvProgress, csvCount), "green") + csvReport + "...", end = "\r")
        csvProgress += 1

        for row in range(1, reportLength):

            severity = readCSV[row][0]

            if severity in criticalScores:
                csv_writer(csvReport, readCSV[row],'critical')
                criticalCount += 1
            elif severity in severeScores:
                csv_writer(csvReport, readCSV[row], 'severe')
                severeCount += 1
            elif severity in moderateScores:
                csv_writer(csvReport, readCSV[row], 'moderate')
                moderateCount += 1
            else:
                print("UNKNOWN VULNERABILITY SCORE: '{0}' for host {1}".format(readCSV[row][0], readCSV[row][1]))
                continue

    # store the info in a list, then put that list in another list
    outputData = [csvReport, criticalCount, severeCount, moderateCount]
    outputDataCollection.append(outputData)
    terminal_output(outputDataCollection)


if __name__ == "__main__":

    now = datetime.date.today()

    try:
        os.mkdir('reports/{0}'.format(now))
    except Exception as e:
        print(e)

    for report in os.listdir('.'):

        if not report.endswith('.csv'):
            continue

        csv_reader(report)
