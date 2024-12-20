/*  @file       server.js
*   @authors    Saurabh Gupta     [saurabh.gupta1002@gmail.com]
*               Awadhut Thube     [awadhutthube@gmail.com]
*               Jheel Nagaria     [nagariajheel@gmail.com]
*               Ashish Kamble     [ashishkamble14@gmail.com]
*/

// Instances //
var app = require('express')();
const path = require('path');
var http = require('http').Server(app);
var io = require('socket.io')(http);
var express = require('express');

//Variables
var consumer_address_list = ["", "", "", "", "", ""];
var producer_address_list = ["", "", "", "", "", ""];
var energy_token = ["", "", "", "", "", ""];
var asking_bid = [0, 0, 0, 0, 0, 0];
var seller_available_0 = 0, seller_available_1 = 0, seller_available_2 = 0;
var seller_available_3 = 0, seller_available_4 = 0, seller_available_5 = 0;
var buyer_available_0 = 0, buyer_available_1 = 0, buyer_available_2 = 0;
var buyer_available_3 = 0, buyer_available_4 = 0, buyer_available_5 = 0;
var Card_0; var Card_1; var Card_2; var Card_3; var Card_4; var Card_5;

app.use(express.static('public'));

//Energy Marketplace Functions
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'energy_marketplace.html'));
  io.once('connection', function (socket)
  {
    // Send request to producer server to get number of energy tokens in entered account address
    // Adds corresponding producer address and asking_bid value to the list
    // Sets the corresponding 'Seller Available' Flag to 1
    socket.on('add_prosumer', function (data)
    {
      io.emit('add_prosumer', data)
    });

    socket.on('add_consumer', function (data)
    {
      io.emit('add_consumer', data)
    });

    socket.on('start_auction', function (data)
    {
      io.emit('start_auction', 2)
    });

    socket.on('close_connection', function (data)
    {
      io.emit('close', 2);
    });

    // Bidding Function for each seller
    // Gets account data of each buyer
    // Increments bid by 1 Ether on every call
    // Sets the corresponding 'Buyer Available' Flag to 1
    socket.on('bid_for_producer_0', function(data)
    { 
      if(!(producer_address_list[0] == "" || data == null))
      {
        clearTimeout(Card_0);
        asking_bid[0] = Number(asking_bid[0]) + 1;
        consumer_address_list[0] = data;
        buyer_available_0 = 1;
      }
    });

    socket.on('bid_for_producer_1', function(data)
    {
      if(!(producer_address_list[1] == "" || data == null))
      {
        clearTimeout(Card_1);
        asking_bid[1] = Number(asking_bid[1]) + 1;
        consumer_address_list[1] = data;
        buyer_available_1 = 1;
      }
    });

    socket.on('bid_for_producer_2', function(data)
    {
      if(!(producer_address_list[2] == "" || data == null))
      {
        clearTimeout(Card_2);
        asking_bid[2] = Number(asking_bid[2]) + 1;
        consumer_address_list[2] = data;
        buyer_available_2 = 1;
      }
    });

    socket.on('bid_for_producer_3', function(data)
    {
      if(!(producer_address_list[3] == "" || data == null))
      {
        clearTimeout(Card_3);
        asking_bid[3] = Number(asking_bid[3]) + 1;
        consumer_address_list[3] = data;
        buyer_available_3 = 1;
      }
    });

    socket.on('bid_for_producer_4', function(data)
    {
      if(!(producer_address_list[4] == "" || data == null))
      {
        clearTimeout(Card_4);
        asking_bid[4] = Number(asking_bid[4]) + 1;
        consumer_address_list[4] = data;
        buyer_available_4 = 1;
      }
    });

    socket.on('bid_for_producer_5', function(data)
    {
      if(!(producer_address_list[5] == "" || data == null))
      {
        clearTimeout(Card_5);
        asking_bid[5] = Number(asking_bid[5]) + 1;
        consumer_address_list[5] = data;
        buyer_available_5 = 1;
      }
    });

    // Update Marketplace in a regular interval
    setInterval(function()
    {
      io.emit('update_marketplace',
      {
        add0:producer_address_list[0], add1:producer_address_list[1], add2:producer_address_list[2], add3:producer_address_list[3], add4:producer_address_list[4], add5:producer_address_list[5],
        bid0:asking_bid[0], bid1:asking_bid[1], bid2:asking_bid[2], bid3:asking_bid[3], bid4:asking_bid[4], bid5:asking_bid[5],
        con0:consumer_address_list[0], con1:consumer_address_list[1], con2:consumer_address_list[2], con3:consumer_address_list[3], con4:consumer_address_list[4], con5:consumer_address_list[5],
        tok0:energy_token[0], tok1:energy_token[1], tok2:energy_token[2], tok3:energy_token[3], tok4:energy_token[4], tok5:energy_token[5]
      });
    }, 1000);
  });
    
  // Accept a transaction after a timeout
  // Reset all Flags to 0 and clear corresponding data from lists
  // Emit accepted deal's transaction details through socket
  setInterval(function()
  { 
    if(buyer_available_0 == 1)
    { 
      Card_0 = setTimeout(function()
      {
        io.emit('accept_deal_0', {producer_address:producer_address_list[0], bid:asking_bid[0], consumer_address:consumer_address_list[0]});
        producer_address_list[0] = "";
        consumer_address_list[0] = "";
        asking_bid[0] = 0;
        energy_token[0] = "";
        buyer_available_0 = 0;
        seller_available_0 = 0;
      }, 5000);
    }
    if(buyer_available_1 == 1)
    {
      Card_1 = setTimeout(function()
      {
        io.emit('accept_deal_1', {producer_address:producer_address_list[1], bid:asking_bid[1], consumer_address:consumer_address_list[1]});
        producer_address_list[1] = "";
        consumer_address_list[1] = "";
        asking_bid[1] = 0;
        energy_token[1] = "";
        buyer_available_1 = 0;
        seller_available_1 = 0;
      }, 5000);
    }
    if(buyer_available_2 == 1)
    {
      Card_2 = setTimeout(function()
      {
        io.emit('accept_deal_2', {producer_address:producer_address_list[2], bid:asking_bid[2], consumer_address:consumer_address_list[2]});
        producer_address_list[2] = "";
        consumer_address_list[2] = "";
        asking_bid[2] = 0;
        energy_token[2] = "";
        buyer_available_2 = 0;
        seller_available_2 = 0;
      }, 5000);
    }
    if(buyer_available_3 == 1)
    {
      Card_3 = setTimeout(function()
      {
        io.emit('accept_deal_3', {producer_address:producer_address_list[3], bid:asking_bid[3], consumer_address:consumer_address_list[3]});
        producer_address_list[3] = "";
        consumer_address_list[3] = "";
        asking_bid[3] = 0;
        energy_token[3] = "";
        buyer_available_3 = 0;
        seller_available_3 = 0;
      }, 5000);
    }
    if(buyer_available_4 == 1)
    {
      Card_4 = setTimeout(function()
      {
        io.emit('accept_deal_4', {producer_address:producer_address_list[4], bid:asking_bid[4], consumer_address:consumer_address_list[4]});
        producer_address_list[4] = "";
        consumer_address_list[4] = "";
        asking_bid[4] = 0;
        energy_token[4] = "";
        buyer_available_4 = 0;
        seller_available_4 = 0;
      }, 5000);
    }
    if(buyer_available_5 == 1)
    {
      Card_5 = setTimeout(function()
      {
        io.emit('accept_deal_5', {producer_address:producer_address_list[5], bid:asking_bid[5], consumer_address:consumer_address_list[5]});
        producer_address_list[5] = "";
        consumer_address_list[5] = "";
        asking_bid[5] = 0;
        energy_token[5] = "";
        buyer_available_5 = 0;
        seller_available_5 = 0;
      }, 5000);
    }
  }, 10000);
});


// Display Energy Tokens as per request from Producer Server
io.on('connection', function(socket)
{
  socket.on('display_tokens_0', function(data)
  {
    energy_token[0] = data;
  });
  socket.on('display_tokens_1', function(data)
  {
    energy_token[1] = data;
  });
  socket.on('display_tokens_2', function(data)
  {
    energy_token[2] = data;
  });
  socket.on('display_tokens_3', function(data)
  {
    energy_token[3] = data;
  });
  socket.on('display_tokens_4', function(data)
  {
    energy_token[4] = data;
  });
  socket.on('display_tokens_5', function(data)
  {
    energy_token[5] = data;
  });
});

http.listen(4000, () => {
  console.log('listening on *:4000');
});