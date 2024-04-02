
import os
from os import system as shellRun
from functions import *

# only one validator node initially
initial_validators = 2

assert(initial_validators > 0)

for i in range(initial_validators):
    shellRun(f"mkdir node{i}")

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

# create accounts
acc_passwd = "12345"
for i in range(initial_validators):
    create_account(acc_passwd, f"node{i}/data", i)

exit()
# copy genesis in node<n> and static-nodes.json in node<n>/data
# copy node<n>/0/nodekey in all the generate nodes

os.chdir(f"cd node0")
shellRun(f"geth --datadir data init genesis.json")

# repeat the above step of all the nodes

shellRun("PRIVATE_CONFIG=ignore nohup geth --datadir data --nodiscover --istanbul.blockperiod 5 --syncmode full --mine --miner.threads 1 --verbosity 5 --networkid 10 --rpc --rpcaddr 0.0.0.0 --rpcport 22000 --rpcapi admin,db,eth,debug,miner,net,shh,txpool,personal,web3,quorum,istanbul --emitcheckpoints --port 30300 2>>node.log &")

# repeat the above step of all the nodes with changed rpc port etc

