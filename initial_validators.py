
import os
from os import system as shellRun
from functions import *

# only one validator node initially
initial_validators = 1

assert(initial_validators > 0)

for i in range(initial_validators):
    shellRun(f"mkdir -p node{i}")

# setting up the directory, giving the lead to node0
os.chdir("node0")
shellRun(f"istanbul setup --num {initial_validators} --nodes --quorum --save --verbose --verbose >> istanbul.log")
get_data_from_istanbul("istanbul.log")
shellRun("mv validators.log ../")
shellRun("mv dummy-genesis.json ../")
shellRun("mv dummy-static-nodes.json ../")

# update static-node.json to include intended IP and port numbers of all initial validators
os.chdir("..")
update_port_numbers("dummy-static-nodes.json")

for i in range(initial_validators):
    shellRun(f"mkdir -p node{i}/data/geth")

exit()

# create accounts
acc_passwd = "12345"
for i in range(initial_validators):
    create_account(acc_passwd, f"node{i}/data", i)

# update genesis.json file with Public account adresses generated in the above steps
public_addr_dict = extract_acc_public_keys("geth.log")
balance = "0x446c3b15f9926687d2c40534fdb564000000000000"
print(public_addr_dict)
for i in range(initial_validators):
    insert_in_json(f"node{i}/genesis.json", "alloc", public_addr_dict[i], balance)

# distribute files among all initial validators
for i in range(initial_validators):
    shellRun(f"cp -Rn node0/genesis.json node{i}")
    shellRun(f"cp -Rn dummy-static-nodes.json node{i}/data/static-nodes.json") # dummy because it is the updated one
    shellRun(f"cp -Rn node0/{i}/nodekey node{i}/data/geth")
    shellRun(f"rm node{i}/static-nodes.json")

# initialize the nodes
for i in range(initial_validators):
    os.chdir(f"node{i}")
    shellRun("geth --datadir data init genesis.json")
    os.chdir("..")

for i in range(initial_validators):
    shellRun(f"PRIVATE_CONFIG=ignore nohup geth --datadir data --nodiscover --istanbul.blockperiod 5 --syncmode full --mine --miner.threads 1 --verbosity 5 --networkid 10 --rpc --rpcaddr 127.0.0.1 --rpcport 2200{i} --rpcapi admin,db,eth,debug,miner,net,shh,txpool,personal,web3,quorum,istanbul --emitcheckpoints --port 3030{i} 2>>node{i}.log &")


