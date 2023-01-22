import netmiko, typing, prettytable


def create_connection(host: str, username: str, password: str, command: str, port:int = 22) -> str:
    cisco_router = {
        'device_type': 'autodetect',
        'host': host,
        'username': username,
        'password': password,
        'port': port,
    }
    ssh = netmiko.ConnectHandler(**cisco_router)
    result = ssh.send_command(command_string = command)
    ssh.disconnect()
    return result

 

