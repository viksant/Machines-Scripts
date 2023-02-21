# Elasticsearch enumerator. It is incompleted. To be continued:

import requests
import argparse
from pwn import *
import subprocess

def def_handler(sig, frame):
    print("[!] Aborting...")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# Colors
class Interface:
    def __init__(self):
        self.red = '\033[91m'
        self.green = '\033[92m'
        self.white = '\033[37m'
        self.yellow = '\033[93m'
        self.blue = '\033[94m'

    def error(self, message):
        print(f"{self.red}{message}")

    def message(self, message):
        print(f"{self.blue}{message}")

    def success(self, message):
        print(f"{self.green}{message}")

    def warning(self, message):
        print(f"{self.yellow}{message}")

color = Interface()

if len(sys.argv) < 2:
    color.error("Usage: python3 main.py -u <Target's IP>")
    sys.exit(1)

# Check if jq exists in the system:
if not which("jq"):
    color.error("jq is not installed in your system.")
    choice = raw_input('Would you like to install it?(yes/no):')

    if choice.decode().strip() == 'yes':
        color.message("Installing jq...")
        os.system("sudo apt install jq")
        color.success("\n Done! Run the script again")
        sys.exit(0)
    else:
        color.warning("Consider Installing it...")


# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="Target's URL")
args = parser.parse_args()
url = args.url
target_ip = args.url


# Make a request to the target
def MainRequest():
    r = requests.get(f"http://{target_ip}:9200/")
    output = []
    for lines in r.text.splitlines():
        if "number" in lines:
            version = lines.split(":")[1].strip()
            output.append("Elasticsearch Version: " + version + "(Maybe vulnerable to CVE-2018-17246 - Kibana LFI")
        elif "cluster_name" in lines:
            cluster_name = lines.split(":")[1].strip()
            output.append(f"Cluster name: " + cluster_name)

def BasicEnumeration():

    directories = ['Role', 'User']
    for directory in directories:
        r2 = requests.get(f"http://{target_ip}:9200/_security/{directory}")
        if directory == 'Role':
            color.message("Checking for roles...")
            if "error" in r2.text:
                color.error(f"{directory} directory is not available")
            elif directory == "role" and "error" not in r2.text:
                print(r2.text)
        if directory == 'User':
            color.message("Enumerating system users...")
            if "error" in r2.text:
                color.error(f"{directory} directory is not available")
            elif directory == "user" and "error" not in r2.text:
                print(r2.text)
    color.warning("\nDisplying /_cat reachable endpoints...")
    r3 = requests.get(f"http://{target_ip}:9200/_cat")
    response = r3.text
    if "error" in response:
        color.error("No endpoints found")
    else:
        if "=^.^=" in r3.text:
            response = response.replace("=^.^=", " ")
        color.message(response)

    color.warning("\nEnumerating indices...")
    r4 = requests.get(f"http://{target_ip}:9200/_cat/indices")
    if "error" in r4.text:
        color.error("No indices found")
    else:
        color.message(r4.text)

    choice = input('yes or no:').strip().lower()
    if choice == 'yes':
        input_str = input("Enter the index name: ")
        # split the input on whitespace and take the first part as the index name
        index = input_str.split()[0]
        r5 = requests.get(f"http://{target_ip}:9200/{index}/_search?pretty=true")
        if "error" in r5.text:
            color.error("Index not found")
        else:
            store_file=input("Do you want to save it to a file?(yes/no):").strip().lower()
            if store_file == 'yes':
                filename = input("Enter the filename: ")
                with open(filename, 'w') as f:
                    f.write(r5.text)
                    color.success("File saved successfully")
            else:
                color.message(r5.text)

if __name__ == "__main__":
    #MainRequest()
    BasicEnumeration()


