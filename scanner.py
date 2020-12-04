#!/usr/bin/env python3
import sys
import argparse
from jinja2 import Template
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
from time import sleep
from datetime import datetime

'''
Simple Nmap Scanner
Input -> list or file of host/ipv4/ipv6/cidr
Output -> html file with nmap report
'''

def nmap_scan(targets):
    # Nmap scan with service detection (-sV), script scanning (-sC) on all
    # ports (-p-) and agressive timing (-T4)
    nmap_proc = NmapProcess(targets, options='-sV -sC -p- -T4', safe_mode=False)
    nmap_proc.run_background()

    # Checks nmap progress every 30 seconds
    print('Nmap start at {0}'.format(datetime.today().ctime()))
    while nmap_proc.is_running():
        nmaptask = nmap_proc.current_task
        if nmaptask:
            print("Task {0} {1} ({2}): Progress: {3}%".format(
                len(nmap_proc.tasks)+1, nmaptask.name,
                nmaptask.status, nmaptask.progress
                )
            )
        sleep(30)
        
    print(nmap_proc.summary)
    
    try:
        report = NmapParser.parse(nmap_proc.stdout)
    except NmapParserException as e:
        print('Exception raised while parsing scan: {0}'.format(e.msg))
    
    if report.hosts_total == 0:
        print('No hosts discovered')
        sys.exit()

    return report


def export_html(report):
    with open('template.html') as f:
        template = Template(f.read())
    template.stream(nmap=report).dump('report.html')  
    print('Nmap report exported to report.html')



def main():
    parser = argparse.ArgumentParser(description='Scanner Covid Friendly')
    parser.add_argument('-i', '--input', nargs='+', help='List of host/ipv4/ipv6/cidr', metavar='TARGET')
    parser.add_argument('-iF', '--inputFile', help='File of host/ipv4/ipv6/cidr', metavar='FILE')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    
    if args.input and args.inputFile:
        print('Please provide input targets (-i) OR target file (-iF)')
        sys.exit()

    targets = []
    if args.input:
        targets = args.input
    else:
        try:
            with open(args.inputFile) as f:
                targets = f.read().splitlines()
        except:
            print('File ' + args.inputFile + ' could not be opened')
            sys.exit()
    
    print('--------------------------')
    print('      Nmap Scanner        ')
    print('--------------------------')
    nmap_report = nmap_scan(targets)
    export_html(nmap_report)


if __name__ == "__main__":
    main()