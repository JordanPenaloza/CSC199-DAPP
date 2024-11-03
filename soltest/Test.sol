// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FHEStorage {
    // Storage for chunked public key, relinearization keys, and encryption parameters
    uint256[] public publicKeyChunks;
    uint256[][] public relinKeyChunks;
    uint256 public polyModulusDegree;
    uint256 public scale;

    // Mapping to store encrypted values submitted by users
    mapping(address => uint256[]) public encryptedValues;
    
    // Mapping to store encrypted addition results for each address
    mapping(address => uint256[]) public encryptedResults;

    // Events
    event KeysStored();
    event EncryptedValueStored(address indexed user, uint256[] encryptedValue);
    event EncryptedResultStored(address indexed user, uint256[] encryptedResult);

    // Function to store the FHE public key and relinearization keys in chunks
    function setFHEKeys(
        uint256[] memory _publicKeyChunks,
        uint256[][] memory _relinKeyChunks,
        uint256 _polyModulusDegree,
        uint256 _scale
    ) public {
        publicKeyChunks = _publicKeyChunks;
        relinKeyChunks = _relinKeyChunks;
        polyModulusDegree = _polyModulusDegree;
        scale = _scale;
        emit KeysStored();
    }

    // Function to retrieve the public key chunks
    function getPublicKeyChunks() public view returns (uint256[] memory) {
        return publicKeyChunks;
    }

    // Function to retrieve a specific relinearization key chunk
    function getRelinKeyChunks(uint index) public view returns (uint256[] memory) {
        require(index < relinKeyChunks.length, "Invalid index for relinearization key chunk.");
        return relinKeyChunks[index];
    }

    // Function to store an encrypted value
    function storeEncryptedValue(uint256[] memory encryptedValue) public {
        encryptedValues[msg.sender] = encryptedValue;
        emit EncryptedValueStored(msg.sender, encryptedValue);
    }

    // Function to retrieve an encrypted value
    function getEncryptedValue(address user) public view returns (uint256[] memory) {
        return encryptedValues[user];
    }

    // Function to store an encrypted result (after FHE addition in Python)
    function storeEncryptedResult(uint256[] memory encryptedResult) public {
        encryptedResults[msg.sender] = encryptedResult;
        emit EncryptedResultStored(msg.sender, encryptedResult);
    }

    // Function to retrieve an encrypted result
    function getEncryptedResult(address user) public view returns (uint256[] memory) {
        return encryptedResults[user];
    }
}
