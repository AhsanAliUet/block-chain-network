#!/bin/bash

while getopts n:d:c: flag
do
    case "${flag}" in
        n) node_number=${OPTARG};;
        d) directory=${OPTARG};;
        c) chain_id=${OPTARG};;
    esac
done

rpc_port_num=$((22000 + $node_number))
port_num=$((30300 + $node_number))

PRIVATE_CONFIG=ignore geth --datadir data --nodiscover --istanbul.blockperiod 5 --syncmode full --mine --miner.threads 1 --verbosity 5 --networkid 10 --http --http.addr 127.0.0.1 --http.port $rpc_port_num --http.api admin,db,eth,debug,miner,net,shh,txpool,personal,web3,quorum,istanbul --emitcheckpoints --allow-insecure-unlock --port $port_num 2>>node.log &
