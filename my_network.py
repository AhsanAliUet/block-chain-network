import os
import sys
from os import system as shellRun
import subprocess
import time

ROOT_DIR = os.getcwd()
os.chdir(ROOT_DIR)

num_of_nodes = int(sys.argv[1])

passwd = '12345'

def run_geth(passwd, datadir, node_num):
    import pexpect

    # Define your command and password
    command = f'geth account new --datadir {datadir}'
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

def json_to_dict_to_value(file_name, to_find):
    """Input:  Takes file name as a string in argument file_name
       Input:  String; what key to find in the json file with name file_name
       Output: Value of the key provided in to_find argument"""
       
    import json
    with open(file_name, 'r') as file:
        data_dict = json.load(file)

    return data_dict[to_find]

def insert_in_json(file_name, existing_key, new_key, new_value):
    """Appends a new key-value pair to an existing key (existing_key)
       in json file with name file_name"""

    import json

    with open(file_name, 'r') as file:
        data_dict = json.load(file)

    # Make a new key value pair inside the existing key
    data_dict[existing_key][new_key] = {'balance': new_value}

    # Write modified dict to the json file
    with open(file_name, 'w') as file:
        json.dump(data_dict, file, indent=2)

def get_ip_and_port(file_name):
    """file_name is a file containing log of the command <ip a>"""

    import re

    file = open(file_name, 'r')
    lines = file.readlines()
    input_text = ''.join(lines)

    # Define regular expressions for matching lines with relevant information
    interface_pattern = re.compile(r'^\d+: (\w+): (.+)$')
    inet_pattern = re.compile(r'^\s+inet (\S+) .+')

    interfaces = []
    inet_addresses = []

    lines = input_text.split('\n')

    current_interface = None
    for line in lines:
        # Match lines containing interface information
        interface_match = interface_pattern.match(line)
        if interface_match:
            current_interface = interface_match.group(1)
            flags = interface_match.group(2)
            # Check if the flags contain "BROADCAST" and "MULTICAST"
            if 'BROADCAST' in flags and 'MULTICAST' in flags:
                interfaces.append(current_interface)
        
        # Match lines containing "inet" information for the selected interface
        inet_match = inet_pattern.match(line)
        if inet_match and current_interface in interfaces:
            inet_addresses.append(inet_match.group(1))

    # get data of interest
    ip , port = inet_addresses[0].split('/')[0], inet_addresses[0].split('/')[1]
    return ip, port

def distribute_static_json_line(from_str):
    """Breaks a line from static.json file in different components"""

    left_part, discport    = from_str.split('?', 1)[0], from_str.split('?', 1)[1]
    left_part, ip_and_port = left_part.split('@', 1)[0], left_part.split('@', 1)[1]
    ip, port               = ip_and_port.split(':', 1)[0], ip_and_port.split(':', 1)[1]
    left_part, identity    = left_part.split('//', 1)[0], left_part.split('//', 1)[1]

    return identity, ip, port, discport

def write_to_json(file_name, new_entry):
    """Write our devices's (node) ip and port number to static.json, 
       because to be part of the network, we should add to static.json
       file_name of string represents path to the json file, new_entry 
       is a list (if more than one entries, shoudl be comma separated) to be added to the file file_name"""
    
    import json

    with open(file_name, 'r') as file:
        data = json.load(file)

    # Extend the existing data with new entries
    data.extend(new_entry)

    # Write the modified data back to the file
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

def get_validators_info(file_name):
    import re

    with open(file_name, 'r') as file:
        file_contents = file.read()

    # Use regular expression to find "validators" followed by content within curly braces
    match = re.search(r'validators\s*{([^}]+)}', file_contents, re.DOTALL)

    if match:
        validators_str = match.group(1).strip()
    else:
        print("No validators block found in the file.")

    # Use regular expressions to extract information
    address_match = re.search(r'"Address":\s*"([^"]+)"', validators_str)
    nodekey_match = re.search(r'"Nodekey":\s*"([^"]+)"', validators_str)
    nodeinfo_match = re.search(r'"NodeInfo":\s*"([^"]+)"', validators_str)

    # Check if matches were found
    if address_match and nodekey_match and nodeinfo_match:
        address = address_match.group(1)
        nodekey = nodekey_match.group(1)
        nodeinfo = nodeinfo_match.group(1)

    else:
        print("Information not found in the string.")

    return address, nodekey, nodeinfo

balance = 100  # some arbitrary balance

for i in range(num_of_nodes):
    shellRun(f'mkdir -p node-{i}/data')
    os.chdir(f'node-{i}')
    
    # process for node-0 (the very first node) is slightly different
    if (i == 0):
        shellRun(f'istanbul setup --num 1 --nodes --quorum --save --verbose > istanbul.log')
    else:
        shellRun(f'istanbul setup --num 1 --quorum --save > istanbul.log')

    os.system('mkdir -p accounts')
    run_geth(passwd, f"{ROOT_DIR}/node-{i}/accounts", i)

    keystore_folder = os.listdir(f"{ROOT_DIR}/node-{i}/accounts/keystore")
    keystore_file_name = keystore_folder[0]
    address = json_to_dict_to_value(f"{ROOT_DIR}/node-{i}/accounts/keystore/{keystore_file_name}", "address")

    insert_in_json(f"{ROOT_DIR}/node-{i}/genesis.json", "alloc", address, hex(balance))

    address, nodekey, nodeinfo = get_validators_info(f"{ROOT_DIR}/node-{i}/istanbul.log")

    identity, ip_old, port_old, discport_old = distribute_static_json_line(nodeinfo)

    shellRun('ip a > ip_and_port_info.log')

    ip_new, port_new = get_ip_and_port(f"{ROOT_DIR}/node-{i}/ip_and_port_info.log")

    entry = [f"enode://{identity}@{ip_new}:{port_new}?{discport_old}"]
    write_to_json(f"{ROOT_DIR}/node-{i}/static-nodes.json", entry)
    # writin to static-nodes.json

    shellRun('cp static-nodes.json data/')
    shellRun('cp 0/nodekey data/')
    shellRun('geth --datadir data init ./genesis.json')
    shellRun('cp accounts/keystore/* data/keystore')
    
    # launch blockchain
    shellRun(f'PRIVATE_CONFIG=ignore geth --datadir data --nodiscover --istanbul.blockperiod 5\
              --syncmode full --mine --miner.threads 1 --verbosity 5 --networkid 10\
              --rpc --rpcaddr {ip_new} --rpcport {eval(str(30303+int(port_new)))} --rpcapi\
              admin,db,eth,debug,miner,net,shh,txpool,personal,web3,quorum,istanbul\
              --emitcheckpoints --allow-insecure-unlock --port {port_new}')

    os.chdir(ROOT_DIR)
