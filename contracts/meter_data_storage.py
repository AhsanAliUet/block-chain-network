from eth_utils import address
from web3 import Web3
import os
from solcx import compile_standard, compile_solc
from dotenv import load_dotenv
from decrypt import decrypt_aes128
import json
import subprocess
from datetime import datetime
import sys
from get_contract_addr import get_contract_addr

sys.path.append('../')
from w3080 import w3080

bytecode = "608060405234801561001057600080fd5b506116a6806100206000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c80630f0429f21461004657806321de9d311461006257806365059e3514610092575b600080fd5b610060600480360381019061005b9190610f70565b6100c7565b005b61007c60048036038101906100779190610f47565b6105b3565b60405161008991906112c1565b60405180910390f35b6100ac60048036038101906100a7919061109e565b6109bc565b6040516100be969594939291906112e3565b60405180910390f35b868073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610136576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161012d9061136e565b60405180910390fd5b600a6000808a73ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208054905014156104655760005b6009811015610376576000808a73ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206001826101d79190611455565b8154811061020e577f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b90600052602060002090600602016000808b73ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208281548110610292577f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b906000526020600020906006020160008201816000019080546102b490611529565b6102bf929190610d45565b5060018201816001019080546102d490611529565b6102df929190610d45565b5060028201816002019080546102f490611529565b6102ff929190610d45565b50600382018160030190805461031490611529565b61031f929190610d45565b50600482018160040190805461033490611529565b61033f929190610d45565b50600582018160050190805461035490611529565b61035f929190610d45565b50905050808061036e9061155b565b915050610183565b506000808973ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208054806103eb577f4e487b7100000000000000000000000000000000000000000000000000000000600052603160045260246000fd5b6001900381819060005260206000209060060201600080820160006104109190610dd2565b6001820160006104209190610dd2565b6002820160006104309190610dd2565b6003820160006104409190610dd2565b6004820160006104509190610dd2565b6005820160006104609190610dd2565b505090555b6000808973ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206040518060c001604052808981526020018881526020018781526020018681526020018581526020018481525090806001815401808255809150506001900390600052602060002090600602016000909190919091506000820151816000019080519060200190610515929190610e12565b506020820151816001019080519060200190610532929190610e12565b50604082015181600201908051906020019061054f929190610e12565b50606082015181600301908051906020019061056c929190610e12565b506080820151816004019080519060200190610589929190610e12565b5060a08201518160050190805190602001906105a6929190610e12565b5050505050505050505050565b60606000808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020805480602002602001604051908101604052809291908181526020016000905b828210156109b157838290600052602060002090600602016040518060c001604052908160008201805461064690611529565b80601f016020809104026020016040519081016040528092919081815260200182805461067290611529565b80156106bf5780601f10610694576101008083540402835291602001916106bf565b820191906000526020600020905b8154815290600101906020018083116106a257829003601f168201915b505050505081526020016001820180546106d890611529565b80601f016020809104026020016040519081016040528092919081815260200182805461070490611529565b80156107515780601f1061072657610100808354040283529160200191610751565b820191906000526020600020905b81548152906001019060200180831161073457829003601f168201915b5050505050815260200160028201805461076a90611529565b80601f016020809104026020016040519081016040528092919081815260200182805461079690611529565b80156107e35780601f106107b8576101008083540402835291602001916107e3565b820191906000526020600020905b8154815290600101906020018083116107c657829003601f168201915b505050505081526020016003820180546107fc90611529565b80601f016020809104026020016040519081016040528092919081815260200182805461082890611529565b80156108755780601f1061084a57610100808354040283529160200191610875565b820191906000526020600020905b81548152906001019060200180831161085857829003601f168201915b5050505050815260200160048201805461088e90611529565b80601f01602080910402602001604051908101604052809291908181526020018280546108ba90611529565b80156109075780601f106108dc57610100808354040283529160200191610907565b820191906000526020600020905b8154815290600101906020018083116108ea57829003601f168201915b5050505050815260200160058201805461092090611529565b80601f016020809104026020016040519081016040528092919081815260200182805461094c90611529565b80156109995780601f1061096e57610100808354040283529160200191610999565b820191906000526020600020905b81548152906001019060200180831161097c57829003601f168201915b50505050508152505081526020019060010190610613565b505050509050919050565b600060205281600052604060002081815481106109d857600080fd5b9060005260206000209060060201600091509150508060000180546109fc90611529565b80601f0160208091040260200160405190810160405280929190818152602001828054610a2890611529565b8015610a755780601f10610a4a57610100808354040283529160200191610a75565b820191906000526020600020905b815481529060010190602001808311610a5857829003601f168201915b505050505090806001018054610a8a90611529565b80601f0160208091040260200160405190810160405280929190818152602001828054610ab690611529565b8015610b035780601f10610ad857610100808354040283529160200191610b03565b820191906000526020600020905b815481529060010190602001808311610ae657829003601f168201915b505050505090806002018054610b1890611529565b80601f0160208091040260200160405190810160405280929190818152602001828054610b4490611529565b8015610b915780601f10610b6657610100808354040283529160200191610b91565b820191906000526020600020905b815481529060010190602001808311610b7457829003601f168201915b505050505090806003018054610ba690611529565b80601f0160208091040260200160405190810160405280929190818152602001828054610bd290611529565b8015610c1f5780601f10610bf457610100808354040283529160200191610c1f565b820191906000526020600020905b815481529060010190602001808311610c0257829003601f168201915b505050505090806004018054610c3490611529565b80601f0160208091040260200160405190810160405280929190818152602001828054610c6090611529565b8015610cad5780601f10610c8257610100808354040283529160200191610cad565b820191906000526020600020905b815481529060010190602001808311610c9057829003601f168201915b505050505090806005018054610cc290611529565b80601f0160208091040260200160405190810160405280929190818152602001828054610cee90611529565b8015610d3b5780601f10610d1057610100808354040283529160200191610d3b565b820191906000526020600020905b815481529060010190602001808311610d1e57829003601f168201915b5050505050905086565b828054610d5190611529565b90600052602060002090601f016020900481019282610d735760008555610dc1565b82601f10610d845780548555610dc1565b82800160010185558215610dc157600052602060002091601f016020900482015b82811115610dc0578254825591600101919060010190610da5565b5b509050610dce9190610e98565b5090565b508054610dde90611529565b6000825580601f10610df05750610e0f565b601f016020900490600052602060002090810190610e0e9190610e98565b5b50565b828054610e1e90611529565b90600052602060002090601f016020900481019282610e405760008555610e87565b82601f10610e5957805160ff1916838001178555610e87565b82800160010185558215610e87579182015b82811115610e86578251825591602001919060010190610e6b565b5b509050610e949190610e98565b5090565b5b80821115610eb1576000816000905550600101610e99565b5090565b6000610ec8610ec3846113bf565b61138e565b905082815260208101848484011115610ee057600080fd5b610eeb8482856114e7565b509392505050565b600081359050610f0281611642565b92915050565b600082601f830112610f1957600080fd5b8135610f29848260208601610eb5565b91505092915050565b600081359050610f4181611659565b92915050565b600060208284031215610f5957600080fd5b6000610f6784828501610ef3565b91505092915050565b600080600080600080600060e0888a031215610f8b57600080fd5b6000610f998a828b01610ef3565b975050602088013567ffffffffffffffff811115610fb657600080fd5b610fc28a828b01610f08565b965050604088013567ffffffffffffffff811115610fdf57600080fd5b610feb8a828b01610f08565b955050606088013567ffffffffffffffff81111561100857600080fd5b6110148a828b01610f08565b945050608088013567ffffffffffffffff81111561103157600080fd5b61103d8a828b01610f08565b93505060a088013567ffffffffffffffff81111561105a57600080fd5b6110668a828b01610f08565b92505060c088013567ffffffffffffffff81111561108357600080fd5b61108f8a828b01610f08565b91505092959891949750929550565b600080604083850312156110b157600080fd5b60006110bf85828601610ef3565b92505060206110d085828601610f32565b9150509250929050565b60006110e68383611215565b905092915050565b60006110f9826113ff565b6111038185611422565b935083602082028501611115856113ef565b8060005b85811015611151578484038952815161113285826110da565b945061113d83611415565b925060208a01995050600181019050611119565b50829750879550505050505092915050565b600061116e8261140a565b6111788185611433565b93506111888185602086016114f6565b61119181611631565b840191505092915050565b60006111a78261140a565b6111b18185611444565b93506111c18185602086016114f6565b6111ca81611631565b840191505092915050565b60006111e2601383611444565b91507f556e617574686f72697a656420616363657373000000000000000000000000006000830152602082019050919050565b600060c08301600083015184820360008601526112328282611163565b9150506020830151848203602086015261124c8282611163565b915050604083015184820360408601526112668282611163565b915050606083015184820360608601526112808282611163565b9150506080830151848203608086015261129a8282611163565b91505060a083015184820360a08601526112b48282611163565b9150508091505092915050565b600060208201905081810360008301526112db81846110ee565b905092915050565b600060c08201905081810360008301526112fd818961119c565b90508181036020830152611311818861119c565b90508181036040830152611325818761119c565b90508181036060830152611339818661119c565b9050818103608083015261134d818561119c565b905081810360a0830152611361818461119c565b9050979650505050505050565b60006020820190508181036000830152611387816111d5565b9050919050565b6000604051905081810181811067ffffffffffffffff821117156113b5576113b4611602565b5b8060405250919050565b600067ffffffffffffffff8211156113da576113d9611602565b5b601f19601f8301169050602081019050919050565b6000819050602082019050919050565b600081519050919050565b600081519050919050565b6000602082019050919050565b600082825260208201905092915050565b600082825260208201905092915050565b600082825260208201905092915050565b6000611460826114dd565b915061146b836114dd565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff038211156114a05761149f6115a4565b5b828201905092915050565b60006114b6826114bd565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b82818337600083830152505050565b60005b838110156115145780820151818401526020810190506114f9565b83811115611523576000848401525b50505050565b6000600282049050600182168061154157607f821691505b60208210811415611555576115546115d3565b5b50919050565b6000611566826114dd565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff821415611599576115986115a4565b5b600182019050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6000601f19601f8301169050919050565b61164b816114ab565b811461165657600080fd5b50565b611662816114dd565b811461166d57600080fd5b5056fea2646970667358221220f07b5160bd6adcc465c1051e6e3cd5bb1b72ede2201bf4cd85c2644626c2fe6364736f6c63430008000033"

abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "meter_address",
				"type": "address"
			}
		],
		"name": "get_meter_reading",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "timestamp",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "from",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "to",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "active_power",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "import_energy",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "export_energy",
						"type": "string"
					}
				],
				"internalType": "struct meter_data_storage.meter_reading[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "readings",
		"outputs": [
			{
				"internalType": "string",
				"name": "timestamp",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "from",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "to",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "active_power",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "import_energy",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "export_energy",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "meter_address",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "timestamp",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "from",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "to",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "active_power",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "import_energy",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "export_energy",
				"type": "string"
			}
		],
		"name": "store_meter_reading",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

node_url = "http://192.168.0.152:22000"
chain_id = 10

account_addr, private_key, nonce, tx_receipt = get_contract_addr(bytecode, abi, node_url=node_url, chain_id=chain_id)

# print(tx_receipt.contractAddress)

# # ===================== Interact with the deployed contract =====================

w3 = Web3(Web3.HTTPProvider(node_url))
deployed_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
addr = w3.to_checksum_address(account_addr)
print(f"\nInitial value stored is: {deployed_contract.functions.get_meter_reading(addr).call()}")

def setting_transaction(nonce, chain_id, gas_price, private_key, data_dict, node_url="http://192.168.0.152:22000"):
    """
    This function is used to call the solidity functions which perform some calculations
    (unlike the functions which only have return statement in them)
    like setter function, adding function etc

    nonce: nonce of previous transaction, this function will update it automatically
    chain_id: chain id on which node is running
    gas_price: gas price
    private_key: private_key returned by decrypt_aes128 function

    returns nonce and transaction receipt if successful transaction happened.
    """

    timestamp     = data_dict["timestamp"]
    _from         = data_dict["from"]
    _to           = data_dict["to"]
    active_power  = data_dict["active_power"]
    import_energy = data_dict["import_energy"]
    export_energy = data_dict["export_energy"]

    # nonce is increamented by 1 for every attemp made (https://www.investopedia.com/terms/n/nonce.asp#:~:text=A%20nonce%20is%20a%20numerical%20value%20used%20in,values%20in%20the%20block%20consumes%20significant%20computational%20power.)
    nonce = nonce + 1


    new_transaction = deployed_contract.functions.store_meter_reading(addr, timestamp, _from, _to, active_power, import_energy, export_energy).build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": gas_price,
            "from": addr,
            "nonce": nonce,
        }
    )

    try:
        signed_new_txn = w3.eth.account.sign_transaction(
            new_transaction, private_key=private_key
        )
        tx_new_hash = w3.eth.send_raw_transaction(signed_new_txn.rawTransaction)
        print("\nSending new transaction...\n")
        tx_new_receipt = w3.eth.wait_for_transaction_receipt(tx_new_hash)

        return nonce, tx_new_receipt
    except Exception as e:
        print(f"{e}")
        exit(1)

energy_meter_url = "http://192.168.0.107/monitorjson"

import time

while True:
    w3080_data = w3080(energy_meter_url)['Data']
    data_dict = {
        "timestamp"    : str(datetime.now()),
        "from"         : str({"name": "ahsan", "acc_addr": 0x1234}),
        "to"           : str({"name": "ahsan", "acc_addr": 0x1234}),
        "active_power" : str(w3080_data[2]),   # W
        "import_energy": str(w3080_data[3]),   # kWh
        "export_energy": str(w3080_data[4])    # kWh
    }

    w3 = Web3(Web3.HTTPProvider(node_url))
    nonce, tx_receipt = setting_transaction(nonce, chain_id, w3.eth.gas_price, private_key, data_dict)
    print(f"\nWe have updated the value. New value is: {deployed_contract.functions.get_meter_reading(addr).call()}")
    time.sleep(1)