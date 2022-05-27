#!/usr/bin/python3

import sys, os
from datetime import datetime
from azure.cli.core import get_default_cli
import subprocess
import argparse
import pandas as pd

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class azure_defender:
    def __init__(self):
        pass
        self.az_cli = get_default_cli()
        self.date = datetime.now().strftime("%Y%m%d-%H%M%S")

    def login(self):
        print(self.az_cli.invoke(['login']))
        try:
            print(f"{bcolors.OKGREEN}\nOK: Logged in successfully\n")
        except KeyboardInterrupt:
            print(f"{bcolors.WARNING}WARNING: Aborted.")

    def list_subs(self):
        if os.path.isdir("Subscriptions") == False:
            os.mkdir("Subscriptions")
        
        subprocess.check_output([f'az account list --output tsv > Subscriptions/subscriptions_{self.date}.csv'], shell=True)
        print(f"{bcolors.OKGREEN}\nOK: Wrote subs to file.\n")

    def list_alerts(self):
        if os.path.isdir("Alerts") == False:
            os.mkdir("Alerts")

        subprocess.check_output([f'az security alert list --output json > Alerts/alerts_{self.date}.json'], shell=True)
        print(f"{bcolors.OKGREEN}\nOK: Listed the security alerts to file.\n")

    def list_recommendations(self):
        if os.path.isdir("Recommendations") == False:
            os.mkdir("Recommendations")

        subprocess.check_output([f"az security assessment list --output json > Recommendations/recommendations_{self.date}.json"], shell=True)
        print(f"{bcolors.OKCYAN}\nOK: Listed the security recommendations on each subscription.\n")

def main():
    execute = azure_defender()
    # Arguments for usage and options
    parser = argparse.ArgumentParser(description="Azure CLI Helper", add_help=True)
    parser.add_argument("-l", "--login", help="Login into a Microsoft Azure Account",\
                                        action="store_true")
    parser.add_argument("-s", "--subs", help="List the subscriptions of the Azure Account in a json file",\
                                        action="store_true")
    parser.add_argument("-a", "--alerts", help="List all alerts in a file",\
                                        action="store_true")
    parser.add_argument("-r", "--recom", help="List security recommendations in an output file.",\
                                        action="store_true")
    args = parser.parse_args()

    if args.login:
        execute.login()

    if args.subs:
        execute.list_subs()

    if args.alerts:
        execute.list_alerts()
    
    if args.recom:
        execute.list_recommendations()

    # execute = azure_defender()
    # execute.list_subs()

if __name__ == "__main__":
    main()