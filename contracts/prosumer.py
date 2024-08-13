from web3 import Web3
from web3.middleware import geth_poa_middleware
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import serial
import time
import threading
import socketio

try:
    import RPi.GPIO as GPIO
except:
    print("RPi.GPIO (Raspberry Pi) not found. Running in simulation mode.")
    pass

RELAY_PIN = 23

GPIO.setmode(GPIO.BCM) # GPIO.BCM or GPIO.BOARD
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)

# Initialize web3
web3 = Web3(Web3.HTTPProvider('http://192.168.0.154:22000'))
web3.middleware_onion.inject(geth_poa_middleware, layer=0) # Apply PoA middle ware
# Node.js web application framework equivalent in Python
app = Flask(__name__, static_folder='public')
socketio_server = SocketIO(app)
main_server = socketio.Client()

# Connect to the main server
main_server.connect('http://localhost:4000')

@main_server.event
def connect():
    print("Connected to the main server")

@main_server.event
def disconnect():
    print("Disconnected from the main server")

# # Setup Serial Connection with Arduino Nano to control relay
# arduino_serial_port = serial.Serial('/dev/ttyUSB1', baudrate=9600, timeout=1)
# arduino_serial_port.flush()

# # Serial Port Setup for Energy Meter Reading
# meter_serial_port = serial.Serial('/dev/cu.usbserial', baudrate=115200, timeout=1)

meter_reading_string = ""
value_meter = None
producer_address = None
consumer_address = None
ether_per_token = 0
accepted_bid = None
accept_deal_flag = 0
block_deal_flag = 1
energy_tokens = 0
tokens_used = 0
pending_tx_list = []
energy_KWH = 0
prev_energy_KWH = 0
difference = 0
producer = None
consumer = None

# Smart Contract for generation of Virtual Energy Tokens and Automate transactions
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
        "inputs": [],
        "name": "getTotalTokensGiven",
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
        "inputs": [],
        "name": "getTotalTokensUsed",
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
        "name": "getTotalTokensUsedByAccount",
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
                "name": "",
                "type": "address"
            }
        ],
        "name": "tokensUsedByAccount",
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
        "inputs": [],
        "name": "totalTokensGiven",
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
        "inputs": [],
        "name": "totalTokensUsed",
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

contract_deployed_at = "0x8D7D5b8BE5649a5Fe6455A7a4a44013D8c9B8046"
contract_address = web3.to_checksum_address(contract_deployed_at)

# Contract Object Creation at Contract Address
contract = web3.eth.contract(address=contract_address, abi=abi)
web3.eth.default_account = web3.eth.accounts[0]

def read_meter():
    from pzem import read_pzem
    voltage, current, power, energy, frequency, powerFactor, alarm = read_pzem('/dev/ttyS0')

    while True:
        time.sleep(1)
        energy_KWH = energy

def relay_ctrl():
    global accept_deal_flag, block_deal_flag, producer_address, consumer_address, accepted_bid, ether_per_token, producer, consumer, energy_tokens, tokens_used, pending_tx_list, energy_KWH, prev_energy_KWH, difference
    while True:
        pass

def manage_deals():
    global accept_deal_flag, block_deal_flag, producer_address, consumer_address, accepted_bid, ether_per_token, producer, consumer
    while True:
        if accept_deal_flag == 1 and block_deal_flag == 1:
            producer = producer_address
            consumer = consumer_address
            ether_per_token = accepted_bid
            block_deal_flag = 2
        if accept_deal_flag == 1:
            contract.functions.send_eth(producer, ether_per_token).transact({'from': consumer, 'to': contract_address, 'value': ether_per_token})
        time.sleep(8)

@app.route('/')
def index():
    return send_from_directory('public', 'login_page.html')

@app.route('/enter_wallet')
def enter_wallet():
    return send_from_directory('public', 'wallet.html')

@app.route('/node_modules/<path:path>')
def send_node_modules(path):
    return send_from_directory('public/node_modules', path)

@app.route('/consumer.py')
def send_consumer_py():
    return send_from_directory('public', 'consumer.py')

@socketio_server.on('check_passphrase')
def check_passphrase(data):
    unlock_result = web3.geth.personal.unlock_account(web3.eth.accounts[0], data, 100000)
    emit('unlock_ethereum_account_result', unlock_result)

@socketio_server.on('startmine')
def start_mine(data):
    try:
        web3.geth.miner.start()
        emit('mine status', {'status': 'Mining started'})
        print('\n\nMining started\n\n')
    except Exception as e:
        emit('mine_status', {'status': f'Error starting mining: {str(e)}'})
        print('\n\nError starting mining\n\n')

@socketio_server.on('stopmine')
def stop_mine(data):
    web3.geth.miner.stop()

@socketio_server.on('basic_tx')
def basic_tx(data):
    web3.eth.send_transaction({'from': web3.eth.accounts[0], 'to': data['add'], 'value': data['val']})

@main_server.on('req_tokens_0')
def handle_req_tokens_0(data):
    main_server.emit('display_tokens_0', energy_tokens)

@main_server.on('req_tokens_1')
def handle_req_tokens_1(data):
    main_server.emit('display_tokens_1', energy_tokens)

@main_server.on('req_tokens_2')
def handle_req_tokens_2(data):
    main_server.emit('display_tokens_2', energy_tokens)

@main_server.on('req_tokens_3')
def handle_req_tokens_3(data):
    main_server.emit('display_tokens_3', energy_tokens)

def update_energy_tokens():
    global energy_tokens, tokens_used, energy_KWH, prev_energy_KWH, difference, pending_tx_list
    while True:
        difference = energy_KWH - prev_energy_KWH
        balance = web3.eth.get_balance(web3.eth.accounts[0])

        pending_tx_dict = {}
        for i in range(min(3, len(pending_tx_list))):
            pending_tx_dict[f'tx_{i+1}'] = pending_tx_list[i]

        socketio_server.emit('pending_tx_list', pending_tx_dict)
        socketio_server.emit('energy_token_balance', {'tok': energy_tokens, 'tokens_used': tokens_used, 'energy': energy_KWH, 'bal': balance})

        if difference != 0:
            contract.functions.update_tokens(web3.eth.accounts[0], difference).transact()
            prev_energy_KWH = energy_KWH
        pending_tx_list = web3.eth.get_block('pending').transactions
        energy_tokens = contract.functions.token_balance(web3.eth.accounts[0]).call()
        tokens_used   = contract.functions.getTotalTokensUsedByAccount(web3.eth.accounts[0]).call()
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=read_meter).start()
    threading.Thread(target=relay_ctrl).start()
    threading.Thread(target=manage_deals).start()
    threading.Thread(target=update_energy_tokens).start()
    socketio_server.run(app, host='0.0.0.0', port=3000, debug=False)
