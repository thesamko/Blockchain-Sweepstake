// SPDX-License-Identifier: MIT
//import '@openzeppelin/contracts/access/Owanble.sol';
import '@chainlink/contracts/src/v0.6/VRFConsumerBase.sol';

pragma solidity ^0.6.0;


contract Sweepstake is VRFConsumerBase {
    address[] public participants_entries;
    bytes32[] public teams = [bytes32("Arsenal"), "Manchester", "Liverpool"];
    Participant[] public participants;
    enum SWEEPSTAKE_STATUS{ OPEN, SOLD_OUT, CLOSED}
    SWEEPSTAKE_STATUS public sweepstake_status;
    address public owner;
    uint public entry_fee;
    uint internal MAX_PARTICIPANTS;
    uint public balance;
    uint256 public fee;
    bytes32 public keyhash;

    constructor(address _VRFCoordinator, address _link, uint256 _fee, bytes32 _keyhash) public 
    VRFConsumerBase(_VRFCoordinator, _link) {
        owner = msg.sender;
        sweepstake_status = SWEEPSTAKE_STATUS.CLOSED;
        entry_fee = 10000000;
        MAX_PARTICIPANTS = 20;
        fee = _fee;
        keyhash = _keyhash;

    }

    struct Participant {
        address participant_address;
        bytes32 teams;
    }

    function openSweepstake() public {
        require(sweepstake_status == SWEEPSTAKE_STATUS.CLOSED);
        sweepstake_status = SWEEPSTAKE_STATUS.OPEN;
    }

    function enter() public payable {
        if(participants_entries.length == MAX_PARTICIPANTS) {
            setSweepstakeSoldOut();
        }
        require(sweepstake_status == SWEEPSTAKE_STATUS.OPEN,"Sweepstake is either Sold Out or Closed");
        require(msg.value >= entry_fee);
        participants_entries.push(msg.sender);
        balance += msg.value;
        bytes32 requestId = requestRandomness(keyhash, fee);
    }

    function setSweepstakeSoldOut() internal {
        require(sweepstake_status == SWEEPSTAKE_STATUS.OPEN);
        sweepstake_status = SWEEPSTAKE_STATUS.SOLD_OUT;
    }

    function getRandomTeam(uint8 _indexValue) public view returns(bytes32) {
        return teams[_indexValue];
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(_randomness > 0);
        uint256 indexOfTeam = _randomness % teams.length;
        bytes32 team = teams[indexOfTeam];
        addParticipant(msg.sender, team);
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




