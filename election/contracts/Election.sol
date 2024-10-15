pragma solidity ^0.5.0;

contract Election {
    // Model a Candidate
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    // Store accounts that have voted
    mapping(address => bool) public voters;
    // Read/write candidates
    mapping(uint => Candidate) public candidates;
    // Store Candidates Count
    uint public candidatesCount;

    // Events
    event CandidateAdded(uint candidateId, string name);
    event Voted(address voter, uint candidateId);

    constructor() public {
        addCandidate("Candidate 1");
        addCandidate("Candidate 2");
    }

    function addCandidate(string memory _name) private {
        candidatesCount++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
        emit CandidateAdded(candidatesCount, _name);
    }

    function vote(uint _candidateId) public {
        // require that they haven't voted before
        //require(!voters[msg.sender], "You have already voted.");

        // require a valid candidate
        require(_candidateId > 0 && _candidateId <= candidatesCount, "Invalid candidate ID.");

        // record that voter has voted
        //voters[msg.sender] = true;

        // update candidate vote Count
        candidates[_candidateId].voteCount++;

        emit Voted(msg.sender, _candidateId);
    }
}