
#! /usr/bin/env python3
from __future__ import print_function
from __future__ import unicode_literals

# Author: nxkennedy

import sys
import os
import csv
import datetime
from tabulate import tabulate
from termcolor import colored



def main():
    now = datetime.date.today()
    criticalScores = ["8", "9", "10"]
    severeScores = ["4", "5", "6", "7"]
    moderateScores = ["1", "2", "3"]
    headerRow = (
        "Site Name",
        "Asset IP Address",
        "Asset Name", "Service Port",
        "Service Name",
        "Vulnerability CVE IDs",
        "Vulnerability Title",
        "Vulnerability Description",
        "Vulnerability Proof",
        "Vulnerability Solution",
    )
    csvCount = 0
    csvProgress = 1
    outputDataCollection = []
    # creates "reports" directory if it doesn't exist
    dateDir = os.makedirs("reports/{0}".format(now), exist_ok=True)
    # count up csv files in directory to be processed
    for csvReport in os.listdir('.'):
        if not csvReport.endswith('.csv'):
            continue
        csvCount += 1

    # new line for cleaner output
    print("\n")
    # iterate over each csv file in directory
    for csvReport in os.listdir('.'):

        if not csvReport.endswith('.csv'):
            continue

        # read data from each csv report
        with open(csvReport) as csvfile:
            readCSV = list(csv.reader(csvfile, delimiter=","))
            reportLength = len(readCSV)
            # keep us happy with progress printed on screen
            print(colored('Processing File [{0}/{1}]: {2}...'.format(csvProgress, csvCount, csvReport), "green"), end='\r')
            csvProgress += 1

            # function to write new csv files with desired headers
            def csv_header_formatter(report):
                newCsvWriter = csv.writer(report)
                newCsvWriter.writerow(headerRow)

            # function to write new csv files with desired column data from original raw export
            def csv_body_formatter(report):
                newCsvWriter = csv.writer(report)
                newCsvWriter.writerow((readCSV[row][1], readCSV[row][2], readCSV[row][3], readCSV[row][5], readCSV[row][6], readCSV[row][9], readCSV[row][10], readCSV[row][11], readCSV[row][12], readCSV[row][13]))

            # checks vuln scores and copies findings to appropriate files
            criticalCount = 0
            severeCount = 0
            moderateCount = 0
            linesProcessed = 0
            e = None
            for row in range(1, reportLength):

                if readCSV[row][0] in criticalScores:
                    with open('reports/{0}/{1}-{2}-critical.csv'.format(now, now, csvReport.strip('.csv')), 'a+') as critical_csvfile:

                        if criticalCount < 1:
                            csv_header_formatter(critical_csvfile)

                        csv_body_formatter(critical_csvfile)
                        criticalCount += 1
                elif readCSV[row][0] in severeScores:
                    with open('reports/{0}/{1}-{2}-severe.csv'.format(now, now, csvReport.strip('.csv')), 'a+') as severe_csvfile:

                        if severeCount < 1:
                            csv_header_formatter(severe_csvfile)

                        csv_body_formatter(severe_csvfile)
                        severeCount += 1

                elif readCSV[row][0] in moderateScores:
                    with open('reports/{0}/{1}-{2}-moderate.csv'.format(now, now, csvReport.strip('.csv')), 'a+') as moderate_csvfile:

                        if moderateCount < 1:
                            csv_header_formatter(moderate_csvfile)

                        csv_body_formatter(moderate_csvfile)
                        moderateCount += 1

                else:
                    print("ILLEGAL SCORE '{0}' for asset '{1}'".format(readCSV[row][0], readCSV[row][1]))

                linesProcessed += 1


        # store the info in a list, then put that list in another list
        outputData = [csvReport, criticalCount, severeCount, moderateCount, (criticalCount + severeCount + moderateCount)]
        outputDataCollection.append(outputData)
        print("Lines processed (excluding header) for {0}: {1}".format(csvReport, linesProcessed))

    # final output formatting
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
    fmtHeadingTotal = colored("Total", "blue")
    print("\n" + scum)
    print(tabulate(outputDataCollection, headers=[fmtHeadingReport, fmtHeadingCritical, fmtHeadingSevere, fmtHeadingModerate, fmtHeadingTotal], tablefmt='fancy_grid') + "\n")



if __name__ == "__main__":
    main()
