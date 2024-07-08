from web3 import Web3
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import serial
import time
import threading
import socketio

# Initialize web3
web3 = Web3(Web3.HTTPProvider('http://localhost:22000'))

# Node.js web application framework equivalent in Python
app = Flask(__name__)
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

# Setup Serial Connection with Arduino Nano to control relay
arduino_serial_port = serial.Serial('/dev/cu.usbmodem1421', baudrate=9600, timeout=1)
arduino_serial_port.flush()

# Serial Port Setup for Energy Meter Reading
meter_serial_port = serial.Serial('/dev/cu.usbserial', baudrate=115200, timeout=1)

meter_reading_string = ""
value_meter = None
producer_address = None
consumer_address = None
ether_per_token = 0
accepted_bid = None
accept_deal_flag = 0
block_deal_flag = 1
energy_tokens = 0
pending_tx_list = []
energy_KWH = 0
prev_energy_KWH = 0
difference = 0
producer = None
consumer = None

# Smart Contract for generation of Virtual Energy Tokens and Automate transactions
abi = [{"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "balances", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_account", "type": "address"}], "name": "eth_balance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address payable", "name": "_account", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "send_eth", "outputs": [], "stateMutability": "payable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_account", "type": "address"}], "name": "token_balance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_account", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "update_tokens", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]
contract_address = "0x83AE811Db5F0D6C0B8Cad3e1392904e94480f5F4"

# Contract Object Creation at Contract Address
contract = web3.eth.contract(address=contract_address, abi=abi)
web3.eth.default_account = web3.eth.accounts[0]

def read_meter():
    global meter_reading_string, energy_KWH, prev_energy_KWH, value_meter
    while True:
        meter_serial_port.write(b'SHOW=\r\n')
        time.sleep(1)
        meter_reading_string = meter_serial_port.read_all().decode('utf-8')
        KWH_index = meter_reading_string.find("KWH")
        if KWH_index != -1:
            value_meter = meter_reading_string[KWH_index + 8: KWH_index + 9]
            energy_KWH = 1 + int(value_meter)
        meter_reading_string = ""
        time.sleep(5)

def handle_arduino():
    global accept_deal_flag, block_deal_flag, producer_address, consumer_address, accepted_bid, ether_per_token, producer, consumer, energy_tokens, pending_tx_list, energy_KWH, prev_energy_KWH, difference
    while True:
        # Handle Arduino serial port data
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

@socketio_server.on('check_passphrase')
def check_passphrase(data):
    unlock_result = web3.geth.personal.unlock_account(web3.eth.accounts[0], data, 100000)
    emit('unlock_ethereum_account_result', unlock_result)

@app.route('/enter_wallet')
def enter_wallet():
    return send_from_directory('public', 'wallet.html')

@socketio_server.on('startmine')
def start_mine():
    web3.geth.miner.start()

@socketio_server.on('stopmine')
def stop_mine():
    web3.geth.miner.stop()

@socketio_server.on('basic_tx')
def basic_tx(data):
    web3.eth.send_transaction({'from': web3.eth.accounts[0], 'to': data['add'], 'value': data['val']})

def update_energy_tokens():
    global energy_tokens, energy_KWH, prev_energy_KWH, difference, pending_tx_list
    while True:
        difference = energy_KWH - prev_energy_KWH
        balance = web3.eth.get_balance(web3.eth.accounts[4])
        socketio_server.emit('pending_tx_list', {'tx_1': pending_tx_list[0], 'tx_2': pending_tx_list[1], 'tx_3': pending_tx_list[2]})
        socketio_server.emit('energy_token_balance', {'energy': energy_KWH, 'tok': energy_tokens, 'bal': balance})
        if difference != 0:
            contract.functions.update_tokens(web3.eth.accounts[4], difference).transact()
            prev_energy_KWH = energy_KWH
        pending_tx_list = web3.eth.get_block('pending').transactions
        energy_tokens = contract.functions.token_balance(web3.eth.accounts[4]).call()
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=read_meter).start()
    threading.Thread(target=handle_arduino).start()
    threading.Thread(target=manage_deals).start()
    threading.Thread(target=update_energy_tokens).start()
    socketio_server.run(app, host='0.0.0.0', port=3000)
