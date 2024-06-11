const { Web3 } = require('web3');

// Initialize Web3
const web3 = new Web3("http://localhost:22000");

// Your contract ABI
const abi = [
  {
    "inputs": [],
    "name": "get",
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
        "internalType": "uint256",
        "name": "x",
        "type": "uint256"
      }
    ],
    "name": "set",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
];

// Contract address from the deployment transaction receipt
const contractAddress = '0xB7C5dB2e2bbCe34b9256e964A4fE9b74fED26f70';

// Create contract instance
const contract = new web3.eth.Contract(abi, contractAddress);

// Example function to call a method
async function callContractMethod() {
  try {
    console.log("ABI: ", JSON.stringify(abi, null, 2));
    console.log("Contract Address: ", contractAddress);

    // Get accounts
    const accounts = await web3.eth.getAccounts();
    console.log("Accounts: ", accounts);

    // Print available methods
    console.log('Available Methods:', contract.methods);

    // Ensure there is at least one account available
    if (accounts.length === 0) {
      throw new Error("No accounts available");
    }

    // Check contract's bytecode at the address
    const code = await web3.eth.getCode(contractAddress);
    console.log("Contract Bytecode at Address: ", code);

    if (code === '0x') {
      throw new Error("No contract found at the given address");
    }

    // Set some data first to ensure the contract state is initialized
    const setTx = await contract.methods.set(42).send({
      from: accounts[0],
      gas: 2000000, // Set a gas limit
      gasPrice: '0' // Use gas price of 0 for private network
    });

    console.log("Set Transaction receipt:", setTx);

    // Call the get method
    const result = await contract.methods.get().call({ from: accounts[0] });
    console.log('Get Result:', result);
  } catch (error) {
    console.error('Error calling contract method:', error);
  }
}

// Call the example function
callContractMethod();
