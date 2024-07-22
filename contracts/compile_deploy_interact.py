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
bytecode = "6080604052348015600e575f80fd5b5061063f8061001c5f395ff3fe608060405260043610610049575f3560e01c8063105ae03a1461004d57806327e235e3146100895780634e61e2ed146100c55780639ba7548e14610101578063cef29f371461011d575b5f80fd5b348015610058575f80fd5b50610073600480360381019061006e91906103c1565b610145565b6040516100809190610404565b60405180910390f35b348015610094575f80fd5b506100af60048036038101906100aa91906103c1565b61018a565b6040516100bc9190610404565b60405180910390f35b3480156100d0575f80fd5b506100eb60048036038101906100e691906103c1565b61019e565b6040516100f89190610404565b60405180910390f35b61011b60048036038101906101169190610482565b6101be565b005b348015610128575f80fd5b50610143600480360381019061013e91906104c0565b6102d7565b005b5f805f8373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f20549050919050565b5f602052805f5260405f205f915090505481565b5f8173ffffffffffffffffffffffffffffffffffffffff16319050919050565b805f808473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f2054101561023d576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161023490610558565b60405180910390fd5b805f808473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f82825461028891906105a3565b925050819055508173ffffffffffffffffffffffffffffffffffffffff166108fc8290811502906040515f60405180830381858888f193505050501580156102d2573d5f803e3d5ffd5b505050565b805f808473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205461031f91906105d6565b5f808473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f20819055505050565b5f80fd5b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f61039082610367565b9050919050565b6103a081610386565b81146103aa575f80fd5b50565b5f813590506103bb81610397565b92915050565b5f602082840312156103d6576103d5610363565b5b5f6103e3848285016103ad565b91505092915050565b5f819050919050565b6103fe816103ec565b82525050565b5f6020820190506104175f8301846103f5565b92915050565b5f61042782610367565b9050919050565b6104378161041d565b8114610441575f80fd5b50565b5f813590506104528161042e565b92915050565b610461816103ec565b811461046b575f80fd5b50565b5f8135905061047c81610458565b92915050565b5f806040838503121561049857610497610363565b5b5f6104a585828601610444565b92505060206104b68582860161046e565b9150509250929050565b5f80604083850312156104d6576104d5610363565b5b5f6104e3858286016103ad565b92505060206104f48582860161046e565b9150509250929050565b5f82825260208201905092915050565b7f496e73756666696369656e742062616c616e63650000000000000000000000005f82015250565b5f6105426014836104fe565b915061054d8261050e565b602082019050919050565b5f6020820190508181035f83015261056f81610536565b9050919050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52601160045260245ffd5b5f6105ad826103ec565b91506105b8836103ec565b92508282039050818111156105d0576105cf610576565b5b92915050565b5f6105e0826103ec565b91506105eb836103ec565b925082820190508082111561060357610602610576565b5b9291505056fea26469706673582212203fe19f9d769accf6e4b98ba3a549a125bfed32ac7bb22f89700dd1c9447c790b64736f6c634300081a0033"

# get abi
abi = json.loads(
    compiled_sol["contracts"][f"{smart_contract_file}.sol"][f"{smart_contract_file}"]["metadata"]
)["output"]["abi"]
abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "balances",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_account",
				"type": "address"
			}
		],
		"name": "eth_balance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address payable",
				"name": "_account",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "send_eth",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_account",
				"type": "address"
			}
		],
		"name": "token_balance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_account",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "update_tokens",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

# ===================== Establishing the connection with the network =====================
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:22000"))
chain_id = 10

# absolute path to UTC file of the node
utc_file = "/home/ahsan/block-chain-network/node0/data/keystore/UTC--2024-07-09T10-45-24.263880062Z--8f5ee93f7ac20bc9c69c205fe33363e92788dab4"
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