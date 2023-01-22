
from prettytable import PrettyTable
from authData import auth
from validateData import validate
from getData import connection

def main():
    # Get input params
    host = input("Enter device IP: ")
    command = input("Enter the command: ")
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
    print(cdata, "\n")

    # Trying to connect
    try:
        response = connection.create_connection(host, login, password, command, 22)
    except Exception as error:
        print("Can not connect to device: \n", error)   

    if not validate.check_command(response):
        print("Invalid command entered \n")
        return False

    print(response)


if __name__ == "__main__":
    main()