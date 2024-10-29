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

    // New mapping to store encrypted votes
    mapping(uint => uint256[]) public encryptedVotes; // Maps candidate ID to encrypted votes

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
        require(!voters[msg.sender], "You have already voted."); // Ensure unique votes
        require(_candidateId > 0 && _candidateId <= candidatesCount, "Invalid candidate ID.");

        voters[msg.sender] = true; // Record that the voter has voted
        encryptedVotes[_candidateId].push(_encryptedVote); // Store the encrypted vote

        emit EncryptedVoteSubmitted(msg.sender, _candidateId, _encryptedVote);
    }

    // Function to retrieve encrypted votes for a specific candidate
    function getEncryptedVotes(uint _candidateId) public view returns (uint256[] memory) {
        require(_candidateId > 0 && _candidateId <= candidatesCount, "Invalid candidate ID.");
        return encryptedVotes[_candidateId];
    }
}
