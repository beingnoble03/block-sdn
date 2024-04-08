// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// implementation from the paper "Authentication-Chains: Blockchain-Inspired Lightweight Authentication Protocol for IoT Networks"

contract AuthenticatorV2 {
    mapping(address => bytes32) deviceId_to_blockhash;
    address immutable NOS_node_operator;

    constructor(address _nos_operator) {
        NOS_node_operator = _nos_operator;
    }

    modifier onlySuccessfulAuthentication() {
        require(msg.sender == NOS_node_operator);
        _;
    }

    function get_device_id(
        string memory device_address
    ) public pure returns (address) {
        bytes memory bytesAddress = bytes(device_address);
        bytes32 hash = keccak256(bytesAddress);
        return address(uint160(uint256(hash)));
    }

    function get_cluster_id(
        string memory cluster_address
    ) public pure returns (address) {
        bytes memory bytesAddress = bytes(cluster_address);
        bytes32 hash = keccak256(bytesAddress);
        return address(uint160(uint256(hash)));
    }

    function get_device_authentication_request(
        address device_id,
        address cluster_id,
        bytes32 key
    ) public pure returns (bytes32) {
        bytes32 signature = keccak256(
            abi.encodePacked(device_id, cluster_id, key)
        );
        bytes32 dar = keccak256(abi.encode(device_id, cluster_id, signature));
        return dar;
    }

    // send DAR on backend and store it . If the verification is successful call this function.

    function add_authentication_for_device(
        address device_id,
        bool success
    ) public onlySuccessfulAuthentication {
        require(success, "Authentication must be successful");
        deviceId_to_blockhash[device_id] = blockhash(block.number);
    }
}

// contract address -> 0x2aa639318feD7233711A1D689Bf0bD52b3C640C2