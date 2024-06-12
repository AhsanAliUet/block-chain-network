import json
from eth_keyfile import decode_keyfile_json # pip install eth-keyfile
from getpass import getpass

with open('/home/ahsan/block-chain-network/node0/data/keystore/UTC--2024-06-12T08-41-21.482086960Z--30af42e072068e7bff8ddce6d5ee59d4fd2c6694', 'r') as f:
    keystore = json.load(f)

passphrase = getpass("Enter your passphrase: ")

# Decode the private key from the keystore file
private_key = decode_keyfile_json(keystore, passphrase.encode('utf-8'))

print(f"Private Key: 0x{private_key.hex()}") # print hex form, usual form is still not readable
