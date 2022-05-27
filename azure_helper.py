#!/usr/bin/python3
"""
Tool created by Furo Adrian-Gheorghe
                Tamasila Yasmina
"""

import sys, os
from datetime import datetime
from azure.cli.core import get_default_cli
import subprocess
import argparse
import pandas as pd
# import parser

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

class main_parser:
    def __init__(self):
        
        # Arguments for usage and options
        self.parser = argparse.ArgumentParser(description="Azure CLI Helper", add_help=True)
        self.parser.add_argument("-l", "--login", help="Login into a Microsoft Azure Account",\
                                            action="store_true")
        self.parser.add_argument("-s", "--subs", help="List the subscriptions of the Azure Account as a tsv file",\
                                            action="store_true")
        self.parser.add_argument("-a", "--alerts", help="List all alerts in a file",\
                                            action="store_true")
        self.parser.add_argument("-r", "--recom", help="List security recommendations in an output file.",\
                                            action="store_true")
        self.parser.add_argument("output", nargs="?", type=str, default="json", help="Specify the output file type")
        self.args = self.parser.parse_args()

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

        if main_parser().args.output == "table":
            subprocess.check_output([f'az account list --output {main_parser().args.output} > Subscriptions/subscriptions_{self.date}.tsv'], shell=True)
            print(f"{bcolors.OKGREEN}\nOK: Wrote subs to file.\n")
            
        elif main_parser().args.output == "json" or main_parser().args.output == "yaml" or main_parser().args.output == "tsv":
            subprocess.check_output([f'az account list --output {main_parser().args.output} > Subscriptions/subscriptions_{self.date}.{main_parser().args.output}'], shell=True)
            print(f"{bcolors.OKGREEN}\nOK: Wrote subs to file.\n")
        else:
            print(f"{bcolors.FAIL}{bcolors.BOLD}INVALID FORMAT")


    def list_alerts(self):
        if os.path.isdir("Alerts") == False:
            os.mkdir("Alerts")

        if main_parser().args.output == "table":
            subprocess.check_output([f'az security alert list --output {main_parser().args.output} > Alerts/alerts_{self.date}.tsv'], shell=True)
            print(f"{bcolors.OKGREEN}Wrote alerts to file")

        elif main_parser().args.output == "json" or main_parser().args.output == "yaml" or main_parser().args.output == "tsv":
            subprocess.check_output([f'az security alert list --output {main_parser().args.output} > Alerts/alerts_{self.date}.{main_parser().args.output}'], shell=True)
            print(f"{bcolors.OKGREEN}\nOK: Listed the security alerts to file.\n")
        else:
            print(f"{bcolors.FAIL}{bcolors.BOLD}INVALID FORMAT")

    def list_recommendations(self):
        if os.path.isdir("Recommendations") == False:
            os.mkdir("Recommendations")

        if main_parser().args.output == "table":
            subprocess.check_output([f"az security assessment list --output {main_parser().args.output} > Recommendations/recommendations_{self.date}.tsv"], shell=True)
            print(f"{bcolors.OKCYAN}\nOK: Listed the security recommendations on each subscription.\n")

        elif main_parser().args.output == "json" or main_parser().args.output == "yaml" or main_parser().args.output == "tsv":
            subprocess.check_output([f"az security assessment list --output {main_parser().args.output} > Recommendations/recommendations_{self.date}.{main_parser().args.output}"], shell=True)
            print(f"{bcolors.OKCYAN}\nOK: Listed the security recommendations on each subscription.\n")
        else:
            print(f"{bcolors.FAIL}{bcolors.BOLD}INVALID FORMAT")
 

def main():
    execute = azure_defender()
    argparser = main_parser()
    # Arguments for usage and options
    if argparser.args.login:
        execute.login()

    if argparser.args.subs:
        execute.list_subs()

    if argparser.args.alerts:
        execute.list_alerts()
    
    if argparser.args.recom:
        execute.list_recommendations()

    # execute = azure_defender()
    # execute.list_subs()

if __name__ == "__main__":
    main()