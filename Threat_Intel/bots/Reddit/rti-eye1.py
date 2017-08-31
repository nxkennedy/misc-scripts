#!/usr/bin/env python3

#http://progur.com/2016/09/how-to-create-reddit-bot-using-praw4.html
# Author: nxkennedy

import praw # The Reddit bot library
import time # For time formatting
import os # Check file paths
import json # For reading the config file



def main():

    if not os.path.isfile("config/bot-config.json"):
        print("You must create a config file with your username and password.")
        exit(1)

    with open('config/bot-config.json') as json_config_file:
        config = json.load(json_config_file)


    print("Logging in. . .")
    bot = praw.Reddit(user_agent='REPLACE', client_id='REPLACE', client_secret='REPLACE', username=config["login"]["username"], password=config["login"]["password"])


    #bot.login()
    print("[Success]\n")
    #bot.login()
    # monitor r/pwned
    pwned_subreddit = bot.subreddit('pwned')

    # list of comment stream
    pwned_submissions = pwned_subreddit.stream.submissions()

    suspicious_list = ["account", "accounts", "breach","creds", "credentials", "leaked", "leak", "pwd", "password", "passwords", "username", "usernames", "dump", "dumps", "dumped", "citrix", "gotomypc", "gotomeeting", "gototraining", "gotowebinar", "lastpass", "logmein", "getgo", "leakedsource", "haveibeenpwned", "hacked-db"]

    for submission in pwned_submissions:
        title = submission.title # fetch title
        text = submission.selftext # fetch body
        author = submission.author # fetch author
        date = submission.created_utc # fetch time in epoch UTC
        url = submission.url # fetch URL where link is
        for suspicious_word in suspicious_list:
            if suspicious_word in title.lower():
                print("[+] TITLE: " + title)
                print("[+] AUTHOR: " + str(author))
                print("[+] DATE: " + time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(date)) + " UTC")
                print("[+] TEXT: " + text)
                print("[+] URL: " + url)
                print("-----------------------------\n")



if __name__ == "__main__":
    main()
