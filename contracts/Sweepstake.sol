// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract Sweepstake is Ownable{
    address[] public participants_entries;
    bytes32[] public teams = [bytes32("Arsenal"), "Manchester United", "Liverpool", "Leicester", "Brentford", "Crystal Palace",
                                "Southampton", "Newcastle", "Fulham", "Aston Villa", "Manchester City", "Everton", "Tottenham", 
                                "Chelsea", "West Ham", "Leeds", "Wolverhampton", "Brighton", "Nottingham", "Bournemouth"];
    Participant[] public participants;
    enum SWEEPSTAKE_STATUS{ OPEN, SOLD_OUT, CLOSED}
    SWEEPSTAKE_STATUS public sweepstake_status;
    uint public entry_fee;
    uint internal MAX_PARTICIPANTS;
 
    constructor() public  {
        sweepstake_status = SWEEPSTAKE_STATUS.OPEN;
        entry_fee = 10000000;
        MAX_PARTICIPANTS = 3;
    }

    struct Participant {
        address payable participant_address;
        bytes32 teams;
    }

    function openSweepstake() public onlyOwner {
        require(sweepstake_status == SWEEPSTAKE_STATUS.CLOSED);
        sweepstake_status = SWEEPSTAKE_STATUS.OPEN;
    }

    event PlayerTeam(bytes32);
    function enter(uint256 _number) public payable{
        checkFreeSlots();
        require(sweepstake_status == SWEEPSTAKE_STATUS.OPEN,"Sweepstake is either Sold Out or Closed.");
        require(msg.value >= entry_fee);
        uint256 indexValue = _number % getTeamsCount();
        participants_entries.push(msg.sender);
        bytes32 teamRandom = GetRandomTeam(indexValue);
        addParticipant(msg.sender, teamRandom);
        removeTeamsItem(indexValue);
        emit PlayerTeam(teamRandom);
    }

    function getParticipantTeams() public payable returns(bytes32[] memory) {
        require(sweepstake_status == SWEEPSTAKE_STATUS.SOLD_OUT, "You can checked picked teams when Sweepstake is sold out.");
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

    function payWinner(bytes32 _champion) public onlyOwner{
        address payable winner;
        for(uint256 i = 0; i < MAX_PARTICIPANTS; i++) {
            if(participants[i].teams == _champion) {
                winner = participants[i].participant_address;
                break;
            }
        }
        winner.transfer(address(this).balance);
        sweepstake_status = SWEEPSTAKE_STATUS.CLOSED;
    }

    function setSweepstakeSoldOut() internal {
        require(sweepstake_status == SWEEPSTAKE_STATUS.OPEN);
        sweepstake_status = SWEEPSTAKE_STATUS.SOLD_OUT;
    }

    function GetRandomTeam(uint256 _indexValue) internal view returns(bytes32) {
        bytes32 team_to_return = teams[_indexValue];
        return team_to_return;
    }
    
    function addParticipant(address payable _address, bytes32 _team) internal {
        participants.push(Participant(_address, _team));
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

    function checkFreeSlots() internal {
        if(participants_entries.length == MAX_PARTICIPANTS) {
            setSweepstakeSoldOut();
        }
    }

    function removeTeamsItem(uint256 _indexValue) internal {
        teams[_indexValue] = teams[(getTeamsCount()-1)];
        teams.pop();
    }

    function getTeamsCount() internal view returns(uint256) {
        return teams.length;
    }
}