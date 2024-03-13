// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IDcreation {

    function ID_hash(string memory _device, uint256 _id)
        public
        pure
        returns (bytes32)
    {
        return keccak256(abi.encodePacked(_device, _id));
    }
   
}
