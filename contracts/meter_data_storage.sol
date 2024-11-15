// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract meter_data_storage {

    struct meter_reading {
        string  timestamp;
        int active_power;
        int import_energy;
        int export_energy;
    }

    mapping(address => meter_reading[]) public readings;

    modifier authorize(address meter_address) {
        require(msg.sender == meter_address, "Unauthorized access");
        _;
    }

    function store_meter_reading(address meter_address, string memory timestamp, int active_power, int import_energy, int export_energy) public authorize(meter_address)
    {
        if (readings.length == 10) {
            for (uint i = 0; i < 9; i++) {
                readings[i] = readings[i+1]; // shift elements
            }
            readings.pop()
        }

        readings[meter_address].push(meter_reading(timestamp, active_power, import_energy, export_energy));
    }

    function get_meter_reading(address meter_address) public view returns (meter_reading[] memory)
    {
        return readings[meter_address];
    }

}