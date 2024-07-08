// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract test {
   mapping (address => uint) public balances;
   
   // Increment Energy Tokens in given account
   function update_tokens(address _account, uint amount) public {
       balances[_account] = balances[_account] + amount;
       }
    
    // Return Energy Token Balance in given account
    function token_balance(address _account) public view returns (uint) {
        return balances[_account];
        }

    // Return Ether Balance in given account
    function eth_balance(address _account) public view returns (uint) {
        return _account.balance;
        }

    // Interface for automated payment
    // Decrements Energy Tokens in given account
    function send_eth(address payable _account, uint amount) public payable {
        require(balances[_account] >= amount, "Insufficient balance");

        balances[_account] -= amount;
        _account.transfer(amount);
    }

}
