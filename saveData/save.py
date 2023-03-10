import os

# Create and save file in directory
def saveTo(data, format, command):
    file_name = parseName(command)
    new_schema_path = f"Schema/{format}/{file_name}.schema.{format}"
    if os.path.exists(new_schema_path):
        os.remove(new_schema_path)
    new_schema = open(new_schema_path, "x")
    new_schema.write(data)
    new_schema.close()
    return [new_schema_path, file_name] 

# Parse name of command. Example "show arp" --> "ModelOfShowArp"
def parseName(command):
    command = command.title().split(" ")
    command = "".join(command)
    command = "ModelOf" + command
    return command


