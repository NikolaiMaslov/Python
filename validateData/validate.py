import re
import os

# ping -c = for Linux
# ping -n = for Windows

def ping(host):
    hostname = host
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        return True
    else:
        return False
    
def validate_ip(ip):
    try:
        check_ip = ip.split(".")
        for octet in check_ip:
            if int(octet):
                continue
            else:
                return False
    except ValueError:
        return False

    reg_ip = re.match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$', ip)
    if reg_ip:
        return True
    else:
        return False

def check_command(response):
    if "Invalid input" in response:
        return False
    else: 
        return True