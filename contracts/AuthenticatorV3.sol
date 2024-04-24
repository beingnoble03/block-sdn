// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuthenticatorV3 {
   
    struct Pubkeys {
        bytes32[] pubkeys;
    }

    struct PubkeyHashes {
        bytes32[] pubkeyhashes;
    }
    
    mapping(string => Pubkeys) deviceId_to_pubkey;
    mapping(string => PubkeyHashes) deviceId_to_pubkeyhash;

    address immutable NOS_node_operator;

    constructor(address _nos_operator) {
        NOS_node_operator = _nos_operator;
    }

    modifier onlySuccessfulAuthentication() {
        require(msg.sender == NOS_node_operator, "Only NOS node operator can call this function");
        _;
    }

    function add_Authentication_data(uint16 auth_type, bytes32 derived_key, string memory device_id) public onlySuccessfulAuthentication {
        if (auth_type == 0) {
            deviceId_to_pubkey[device_id].pubkeys.push(derived_key);
        } else {
            bytes32 hash = keccak256(abi.encode(derived_key, device_id));
            deviceId_to_pubkeyhash[device_id].pubkeyhashes.push(hash);
        }
    }

    function type1_auth( bytes32 derived_key, string memory device_id) public view returns(bool){
           
        bytes32[] memory device_pubs = deviceId_to_pubkey[device_id].pubkeys;
        uint array_len = device_pubs.length;

        for (uint i=0 ; i< array_len ; i++ ){
         
         if(derived_key == device_pubs[i]){
            return true;
         }
        }

        return false;
    }
    
    function type2_auth( bytes32 derived_key, string memory device_id) public view returns(bool){
           
        bytes32[] memory device_pubhashes = deviceId_to_pubkey[device_id].pubkeys;
        uint array_len = device_pubhashes.length;
        bytes32 hash = keccak256(abi.encode(derived_key, device_id));

        for (uint i=0 ; i< array_len ; i++ ){
         
         if(hash == device_pubhashes[i]){
            return true;
         }
        }

        return false;
    }
   
}
