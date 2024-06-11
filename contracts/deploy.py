
from os import system as shellRun
import json
import time
from web3 import Web3
import re  # regular expressions

bin_file = open("SimpleStorage.bin", "r")
bin_file_content = bin_file.readlines()[0]

sender_account = "0x36db16d950d889dfc38af9d81e90294a3c101d67"
gas = "0x24A22"
gasPrice = "0x0"
print("============== Deploying the contract... ==============\n")

command = f"curl -X POST --data \'{{\"jsonrpc\":\"2.0\",\"method\":\"eth_sendTransaction\",\"params\":[{{\"from\":\"{sender_account}\", \"to\":null, \"gas\":\"{gas}\",\"gasPrice\":\"{gasPrice}\", \"data\":\"0x{bin_file_content}\"}}], \"id\":1}}\' -H \'Content-Type: application/json\' http://localhost:22000 > deploy.log"
try:
    shellRun(command)
    print("\n============== Contract Deployed! ==============\n")
except:
    raise Exception("Contract Deployment failed! Check .bin file, sender account is incorrect or locked.")

# ========================= Getting Transaction Receipt ======================

deployed_file = 'deploy.log'

# Read the JSON data from the file
with open(deployed_file, 'r') as file:
    json_data = file.read().strip()

parsed_data = json.loads(json_data)
result_field = parsed_data.get('result')

print("Getting Transaction Receipt of the Deployed contract...\n")

# transaction receipt command

node_url = "http://localhost:22000"

web3 = Web3(Web3.HTTPProvider(node_url))
time.sleep(10)  # let web3 connect to url

transactionReceipt_file = open("transaction_receipt.log", "w")

try:
    transactionReceipt = web3.eth.get_transaction_receipt(result_field)
    transactionReceipt = str(transactionReceipt)
    transactionReceipt_file.write(transactionReceipt)
except:
    raise Exception("Cannot get transaction receipt, check the account whether it is unlocked!")

transactionReceipt_file.close()

# ============= Get contract Address ==================
match = re.search(r"'contractAddress': '([^']+)'", transactionReceipt)
contractAddr = match.group(1)
print(contractAddr)