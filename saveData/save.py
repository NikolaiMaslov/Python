import os

# Create and save file in directory
def saveTo(data, format, command):
    file_name = parseName(command)
    new_schema = open(f"Schema/{format}/{file_name}.schema.{format}", "x")
    new_schema.write(data)
    new_schema.close()
    return f"Saved to: Schema/{format}/{file_name}.schema.{format}" 

# Parse name of command. Example "show arp" --> "ModelOfShowArp"
def parseName(command):
    command = command.title().split(" ")
    command = "".join(command)
    command = "ModelOf" + command
    return command


