from prettytable import PrettyTable
from authData import auth
from validateData import validate
from getData import connection
from parseData import parser
from saveData import save
from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from


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
    absolute_path = path[0]
    name_of_model = path[1]
    print("Saved to: ", path)
    createServer(absolute_path, name_of_model)
    return True


def createServer(path, name_of_model):
    app = Flask(__name__)
    app.json_encoder = LazyJSONEncoder
    swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'Lime  UI'),
        'version': LazyString(lambda: '0.3'),
        'description': LazyString(lambda: 'Test API'),
        },
        host = LazyString(lambda: request.host)
    )
    swagger_config = {
        "headers": [],
        "specs": [
            {
            "endpoint": 'config',
            "route": '/config.yml',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
        }

    swagger = Swagger(app, template=swagger_template, config=swagger_config)

    @swag_from("config.yml", methods=['GET'])
    @app.route(f"/{name_of_model}")
    def send_file():
        file = open(path,'r')
        return file.read()  
    app.run()

if __name__ == "__main__":
    main()