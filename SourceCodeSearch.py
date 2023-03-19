############# Used to search .htb links inside source codes ################
############# Example of usage: python3 script.py -d http://horizontall.htb/


#!/usr/bin/env python3
import pdb
import requests
import argparse
from pwn import *
from bs4 import BeautifulSoup
import re
import rich

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-rhost", "--rhost", help="Remote host's IP", required=False)
parser.add_argument("-d", "--dns", help="Remote host's target DNS", required=False)

args = parser.parse_args()
rhost = args.rhost
dns = args.dns

def MakeRequest():
    # Create requests sessions & methods
    s = requests.Session()
    g = s.get(url=dns)

    # Parse HTML using beautifulsoup
    soup = BeautifulSoup(g.text, "html.parser")

    # Get all links
    links = []
    for link in soup.find_all("link"):
        href = link.get("href")
        links.append(href)

    for link in links:
        if "favicon.ico" in link:
            links.remove(link)
    # Search in every link now:

    htb_links = []
    for link in links:
        new_url = f"{dns}{link}"
        g2 = s.get(url=new_url)
        htb_files = re.findall(r'\S+\.htb\b', g2.text)
        if htb_files:
            htb_links.append(htb_files)

    for htb in htb_links:
        print(htb)

if __name__ == "__main__":
    rich.print("[yellow][!] Add machine's DNS to /etc/hosts before running this script if needed [/yellow]")
    time.sleep(2)
    MakeRequest()









