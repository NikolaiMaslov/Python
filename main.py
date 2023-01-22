from prettytable import PrettyTable
from authData import auth
from validateData import validate
from getData import connection
from parseData import parser
from saveData import save
import pprint

def main():
    # Get input params
    host = input("Enter device IP: ")
    command = input("Enter the command: ")
    format_to_save = input("Format to save [yaml/json]: ")
    login = auth.getLogin()
    password = auth.getPassword()

    # Check IP for validation
    if not validate.validate_ip(host):
        print("Invalid Syntax")
        return False

    # Check IP for reachability
    if not validate.ping(host):
        print("Host is unreachable")
        return False

    # Vizualizing data
    cdata = PrettyTable()
    cdata.field_names = ["Key", "Value"]
    cdata.add_row(["Host IP", host])
    cdata.add_row(["Login", login])
    cdata.add_row(["Command", command])
    cdata.add_row(["Format", format_to_save])
    print(cdata, "\n")

    # Trying to connect
    try:
        response = connection.create_connection(host, login, password, command, 22)
    except Exception as error:
        print("Can not connect to device: \n", error)   

    # Validate answer from device
    if not validate.check_command(response):
        print("Invalid command entered \n")
        return False

    init_parser = parser.load_ttp(command)
    parsed_data = parser.parse_ttp(init_parser, response, format_to_save)

    path = save.saveTo(parsed_data, format_to_save, command)
    print(path)
    return True

if __name__ == "__main__":
    main()