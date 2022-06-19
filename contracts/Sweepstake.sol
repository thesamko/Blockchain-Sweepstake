// SPDX-License-Identifier: MIT
//import '@openzeppelin/contracts/access/Owanble.sol';

pragma solidity ^0.6.0;


contract Sweepstake 
//is Ownable
{
    address[] public participants_entries;
    bytes32[] public teams = [bytes32("Arsenal"), "Manchester", "Liverpool"];
    Participant[] public participants;
    mapping(address => string[]) internal addressToTeamMatched;
    enum SWEEPSTAKE_STATUS{ OPEN, SOLD_OUT, CLOSED}
    SWEEPSTAKE_STATUS public sweepstake_status;
    address public owner;
    uint public entry_fee;

    constructor() public {
        owner = msg.sender;
        sweepstake_status = SWEEPSTAKE_STATUS.CLOSED;
        entry_fee = 10000000;
    }

    struct Participant {
        address participant_address;
        bytes32 teams;
    }

    function openSweepstake() public { //onlyOwner
        require(sweepstake_status == SWEEPSTAKE_STATUS.CLOSED);
        sweepstake_status = SWEEPSTAKE_STATUS.OPEN;
    }

    function enter() public payable {
        if(participants_entries.length == 20) {
            setSweepstakeSoldOut();
        }
        require(sweepstake_status == SWEEPSTAKE_STATUS.OPEN,"Sweepstake is either Sold Out or Closed");
        require(msg.value >= entry_fee);
        participants_entries.push(msg.sender);
        addParticipant(msg.sender, getRandomTeam(0)); //add random number
    }

    function setSweepstakeSoldOut() public {
        require(sweepstake_status == SWEEPSTAKE_STATUS.OPEN);
        sweepstake_status = SWEEPSTAKE_STATUS.SOLD_OUT;
    }

    function getRandomTeam(uint8 _indexValue) public view returns(bytes32) {
        return teams[_indexValue];
    }

    function addParticipant(address _address, bytes32 _team) internal {
        participants.push(Participant(_address, _team));
    }

    function getParticipantTeams() public view returns(bytes32[] memory) {
        address _address = msg.sender;
        bytes32[] memory teamsP = new bytes32[] (getEntriesCount(_address));
        uint8 array_index;

        for(uint8 index = 0; index < participants.length; index++) {
            if(participants[index].participant_address == _address) {
                teamsP[array_index++] = participants[index].teams;
            }
        }
        return teamsP;
    }

    function getEntriesCount(address _address) internal view returns(uint) {
        uint counter;
        for(uint8 index = 0; index < participants_entries.length; index++) {
            if(participants_entries[index] == _address) {
                counter++;
            }
        }
        return counter;
    }
}




