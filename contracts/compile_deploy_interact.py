from eth_utils import address
from web3 import Web3
import os
from solcx import compile_standard, install_solc
from dotenv import load_dotenv
import json

smart_contract_file_path = "./"
smart_contract_file = "SimpleStorage"

with open(smart_contract_file_path + smart_contract_file + ".sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.8.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open(smart_contract_file_path + smart_contract_file + ".json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# set up connection
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:22000"))
chain_id = 10
sender_account = "0x30af42e072068e7bff8ddce6d5ee59d4fd2c6694"
my_address = Web3.to_checksum_address(sender_account)
# private_key = os.getenv("PRIVATE_KEY")
private_key = "0xd9cdee3121681abd782c342938683f51bdf76909d77b67cb8be846230f05be62"
# initialize contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.get_transaction_count(my_address)
# set up transaction from constructor which executes when firstly
tx = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Contract deployed to {tx_receipt.contractAddress}")

# Working with deployed Contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"Initial stored value at Retrieve {simple_storage.functions.get().call()}")
new_transaction = simple_storage.functions.set(89128921).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_new_txn = w3.eth.account.sign_transaction(
    new_transaction, private_key=private_key
)
tx_new_hash = w3.eth.send_raw_transaction(signed_new_txn.rawTransaction)
print("Sending new transaction...")
tx_new_receipt = w3.eth.wait_for_transaction_receipt(tx_new_hash)

print(f"New stored value at Retrieve {simple_storage.functions.get().call()}")