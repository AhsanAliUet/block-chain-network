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

# retrieve bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# ===================== Establishing the connection with the network =====================
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:22000"))
chain_id = 10
sender_account = "0xa6d3ac044d58c6f4a838c1127034d03fe0720194"
my_address = Web3.to_checksum_address(sender_account)
# private_key = os.getenv("PRIVATE_KEY")
private_key = "0x1f773492dc6c001a5f73cb4adccc5393f84e88f65cdf3055fda23a7d55d4a06f"

# ===================== Instantiate the contract ===================== 
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.get_transaction_count(my_address)

# ===================== Set up transaction from constructor ===================== 
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
print(f"Contract deployed to address {tx_receipt.contractAddress}")

# ===================== Interact with the deployed contract ===================== 
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"\nInitial value stored is: {simple_storage.functions.get().call()}")

new_transaction = simple_storage.functions.set(12344321).build_transaction(
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
print("\nSending new transaction...\n")
tx_new_receipt = w3.eth.wait_for_transaction_receipt(tx_new_hash)

print(f"We have updated the value. New value is: {simple_storage.functions.get().call()}")