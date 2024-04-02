
def get_data_from_istanbul(file_name):
    with open(file_name, 'r') as file:
        content = file.read()

    sections = [section.strip() for section in content.split('\n\n') if section.strip()]

    target_file_names = {
        "validators": "validators.log",
        "static-nodes.json": "dummy-static-nodes.json",
        "genesis.json": "dummy-genesis.json"
    }

    for section in sections:
        name, data = section.split('\n', 1)

        with open(target_file_names[name], 'w') as file:
            file.write(data)

import json

def update_port_numbers(file_path):
    # Read content from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Define the updated lines
    updated_data = []

    # Iterate through each line
    port_ = 30300
    for line in data:
        # Extract the current IP address and port number from the line
        parts = line.split('@')
        if len(parts) < 2:
            print(f"Skipping line: {line.strip()} - Invalid format")
            continue
        
        ip_and_port = parts[1].split('?')[0]
        ip, port = ip_and_port.split(':')

        # Construct the updated line
        updated_line = f"{parts[0]}@127.0.0.1:{str(port_)}?{parts[1].split('?')[1]}"
        updated_data.append(updated_line)
        port_ = port_ + 1

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write('[')
        file.write('\n')
        for i in range(len(updated_data)):
            if (i == len(updated_data)-1):
                file.write('\t\"' + updated_data[i] + '\"\n')
            else:
                file.write('\t\"' + updated_data[i] + '\",\n')
        file.write(']')

def create_account(passwd, datadir, node_num):
    import pexpect

    # Define your command and password
    command = f'nohup geth account new --datadir {datadir} account new'
    password = passwd

    # Start the command
    child = pexpect.spawn(command)

    # Wait for the password prompt
    child.expect('Password:')
    child.sendline(password)  # Send the password

    # Wait for the password confirmation prompt
    child.expect('Repeat password:')
    child.sendline(password)  # Send the password again

    # Wait for the process to complete and print its output
    child.expect(pexpect.EOF)
    # print(child.before.decode())

