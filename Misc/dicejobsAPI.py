
# Search the Dice Jobs API
# lame docs: http://www.dice.com/common/content/util/apidoc/jobsearch.html
# author: nxkennedy


'''
Example response:

{"detailUrl":"http://www.dice.com/job/result/10347349a/749028?src\u003d19","jobTitle":"Front-End Web Developer","company":"The Doyle Group","location":"Denver, CO","date":"2017-01-18"}

'''


import requests
import csv
from os.path import exists
from sys import argv




def format_search(terms):

    print(terms)
    words = [x for x in terms.split(' ') if x]
    print(words)
    query = 'text=' + '+'.join(words) + '&age=30' + '&sort=1'
    print(query)
    # age - (optional) specify a posting age (a.k.a. days back)
    # sort - (optional) sort=1 sorts by posted age, sort=2 sorts by job title, sort=3 sorts by company, sort=4 sorts by location
    baseURL= 'http://service.dice.com/api/rest/jobsearch/v1/simple.json?'
    url = baseURL + query
    print("\nRequested URL:", url + '\n')
    return url



def write_to_file(jobListings):

    with open('jobs.csv', 'w') as csvFile:
        fieldnames = ['Job Title', 'Company', 'Location', 'Posted', 'URL']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()
        for job in jobListings:
            writer.writerow({'Job Title': job['jobTitle'], 'Company': job['company'], 'Location': job['location'], 'Posted': job['date'], 'URL': job['detailUrl']})
    print("Finished writing file.")



def search(terms):

    response = requests.get(format_search(terms)).json()
    rawData = response
    print(rawData['count'], 'total results')
    print(rawData['lastDocument'], 'results per page')
    jobListings = rawData['resultItemList']
    write_to_file(jobListings)



if __name__ == '__main__':
    s = input('Key word(s) to search?\n> ')
    search(s)
