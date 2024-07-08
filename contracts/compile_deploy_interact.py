from eth_utils import address
from web3 import Web3
import os
from solcx import compile_standard, compile_solc
from dotenv import load_dotenv
from decrypt import decrypt_aes128
import json

smart_contract_file_path = "./"
smart_contract_file = "test"

with open(smart_contract_file_path + smart_contract_file + ".sol", "r") as file:
    simple_storage_file = file.read()

compile_solc("0.8.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {f"{smart_contract_file}.sol": {"content": simple_storage_file}},
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
bytecode = compiled_sol["contracts"][f"{smart_contract_file}.sol"][f"{smart_contract_file}"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"][f"{smart_contract_file}.sol"][f"{smart_contract_file}"]["metadata"]
)["output"]["abi"]

# ===================== Establishing the connection with the network =====================
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:22000"))
chain_id = 10

# absolute path to UTC file of the node
utc_file = "/home/ahsan/block-chain-network/node0/data/keystore/UTC--2024-07-08T17-20-31.789847381Z--45b93cf8c2af1c8f43ff17ae436371bc45df538e"
sender_account = '0x' + utc_file.split("--")[2]
my_address = Web3.to_checksum_address(sender_account)

encryption_file = utc_file
acc_passwd = "12345"
private_key = decrypt_aes128(encryption_file, acc_passwd)

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

# # ===================== Interact with the deployed contract ===================== 
# simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# print(f"\nInitial value stored is: {simple_storage.functions.get().call()}")

# # nonce is increamented by 1 for every attemp made (https://www.investopedia.com/terms/n/nonce.asp#:~:text=A%20nonce%20is%20a%20numerical%20value%20used%20in,values%20in%20the%20block%20consumes%20significant%20computational%20power.)
# nonce = nonce + 1

# new_transaction = simple_storage.functions.set(12344321).build_transaction(
#     {
#         "chainId": chain_id,
#         "gasPrice": w3.eth.gas_price,
#         "from": my_address,
#         "nonce": nonce,
#     }
# )

# signed_new_txn = w3.eth.account.sign_transaction(
#     new_transaction, private_key=private_key
# )
# tx_new_hash = w3.eth.send_raw_transaction(signed_new_txn.rawTransaction)
# print("\nSending new transaction...\n")
# tx_new_receipt = w3.eth.wait_for_transaction_receipt(tx_new_hash)

# print(f"We have updated the value. New value is: {simple_storage.functions.get().call()}")