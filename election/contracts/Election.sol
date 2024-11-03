pragma solidity ^0.5.0;

contract Election {
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    mapping(address => bool) public voters; // Store accounts that have voted
    mapping(uint => Candidate) public candidates; // Candidates mapping
    uint public candidatesCount; // Store the count of candidates

    // Store encrypted votes for each candidate
    mapping(uint => uint256[]) public encryptedVotes;

    // Storage for split FHE keys and parameters
    uint256[] public publicKeyChunks;
    uint256[][] public relinKeyChunks; // Array of arrays for relin keys
    uint256 public polyModulusDegree;
    uint256 public scale;

    event CandidateAdded(uint candidateId, string name);
    event EncryptedVoteSubmitted(address indexed voter, uint candidateId, uint256 encryptedVote);

    constructor() public {
        addCandidate("Candidate 1");
        addCandidate("Candidate 2");
    }

    function addCandidate(string memory _name) private {
        candidatesCount++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
        emit CandidateAdded(candidatesCount, _name);
    }

    function submitEncryptedVote(uint _candidateId, uint256 _encryptedVote) public {
        require(!voters[msg.sender], "You have already voted.");
        require(_candidateId > 0 && _candidateId <= candidatesCount, "Invalid candidate ID.");

        voters[msg.sender] = true;
        encryptedVotes[_candidateId].push(_encryptedVote);

        emit EncryptedVoteSubmitted(msg.sender, _candidateId, _encryptedVote);
    }

    function getEncryptedVotes(uint _candidateId) public view returns (uint256[] memory) {
        require(_candidateId > 0 && _candidateId <= candidatesCount, "Invalid candidate ID.");
        return encryptedVotes[_candidateId];
    }

    // Store FHE keys in chunked form
    function setFHEKeys(uint256[] memory _publicKeyChunks, uint256[][] memory _relinKeyChunks, uint256 _polyModulusDegree, uint256 _scale) public {
        publicKeyChunks = _publicKeyChunks;
        relinKeyChunks = _relinKeyChunks;
        polyModulusDegree = _polyModulusDegree;
        scale = _scale;
    }

    // Retrieve FHE public key chunks
    function getPublicKeyChunks() public view returns (uint256[] memory) {
        return publicKeyChunks;
    }

    // Retrieve FHE relinearization key chunks
    function getRelinKeyChunks(uint index) public view returns (uint256[] memory) {
        require(index < relinKeyChunks.length, "Invalid relin key index.");
        return relinKeyChunks[index];
    }
}
