from brownie import Sweepstake, exceptions, accounts
from scripts.utils import *
import pytest

entry_fee = 10000000

def test_sweepstake_status_when_deployed():
    account_owner = accounts[0]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    actual_state = sweepstake.sweepstake_status()
    expected_state = 0
    assert actual_state == expected_state

def test_owner_cannot_participate():
    account = accounts[0]
    sweepstake = Sweepstake.deploy({"from":account})
    with pytest.raises(exceptions.VirtualMachineError):
        sweepstake.enter(20, {"from":account, "value": entry_fee})
def test_cannot_enter_entry_fee_smaller():
   account = accounts[0]
   sweepstake = Sweepstake.deploy({"from":account})
   with pytest.raises(exceptions.VirtualMachineError):
       sweepstake.enter(20, {"from":accounts[1], "value": 100000})

def test_entering_success_logging():
    account_owner = accounts[0]
    account_enter = accounts[1]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    assert sweepstake.participants_entries(0) == account_enter

def test_participant_logged_with_team():
    account_owner = accounts[0]
    account_enter = accounts[1]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    expected_team = sweepstake.teams(0)
    tx = sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    actual_team = tx.events["PlayerTeam"]["teamRandom"]
    participant_address = sweepstake.participants(0)[0]
    assert expected_team == actual_team
    assert participant_address == account_enter

def test_teams_shuffled_after_entered():
    account_owner = accounts[0]
    account_enter = accounts[1]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    expected_team = sweepstake.getTeam(19)
    sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    actual_team = sweepstake.getTeam(0)
    assert expected_team == actual_team

def test_entering_sweepstake_returns_team():
    account_owner = accounts[0]
    account_enter = accounts[1]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    tx = sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    picked_team = tx.events["PlayerTeam"]["teamRandom"]
    actual_value = decode_hex_strings(picked_team).replace("\x00","")
    expected_value = "Arsenal"
    assert actual_value == expected_value


def test_cannot_enter_when_soldout():
    account_owner = accounts[0]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    for i in range(1,4):
        sweepstake.enter(20, {"from":accounts[i], "value": entry_fee})
    with pytest.raises(exceptions.VirtualMachineError):
        sweepstake.enter(20, {"from":accounts[4], "value": entry_fee})

def test_sweepstake_status_when_soldout():
    account_owner = accounts[0]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    for i in range(1,4):
        sweepstake.enter(20, {"from":accounts[i], "value": entry_fee})
    actual_state = sweepstake.sweepstake_status()
    expected_state = 1
    assert actual_state == expected_state

def test_getting_your_teams_when_open():
    account_owner = accounts[0]
    account_enter = accounts[1]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    with pytest.raises(exceptions.VirtualMachineError):
        sweepstake.getParticipantTeams(account_enter, {"from":account_enter})

def test_getting_your_teams_when_soldout():
    account_owner = accounts[0]
    account_enter = accounts[1]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    for i in range(1,4):
        sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    tx = sweepstake.getParticipantTeams(account_enter, {"from":account_enter})
    actual_value =[decode_hex_strings(i).replace("\x00","") for i in tx.events["AllPlayersTeams"]["teamsP"]]
    expected_value = ['Arsenal', 'Manchester United', 'Liverpool']
    assert actual_value == expected_value

def test_pay_winner_bad_actor():
    account_owner = accounts[0]
    account_enter = accounts[1]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    with pytest.raises(exceptions.VirtualMachineError):
        sweepstake.payWinner(0x4c69766572706f6f6c0000000000000000000000000000000000000000000000,
                            {"from":account_enter})

def test_pay_winner():
    account_owner = accounts[0]
    account_enter = accounts[1]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    tx = sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    winner_team = tx.events["PlayerTeam"]["teamRandom"]
    account_two = accounts[2]
    sweepstake.enter(20, {"from":account_two, "value": entry_fee})
    sweepstake.enter(20, {"from":account_two, "value": entry_fee})
    sweepstake_balance = sweepstake.balance()
    starting_balance =  account_enter.balance()
    sweepstake.payWinner(winner_team, {"from":account_owner})
    assert sweepstake.balance() == 0
    assert account_enter.balance() == sweepstake_balance + starting_balance

def test_pay_winner_status_changed():
    account_owner = accounts[0]
    account_enter = accounts[1]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    tx = sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    winner_team = tx.events["PlayerTeam"]["teamRandom"]
    sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    sweepstake.payWinner(winner_team, {"from":account_owner})
    assert sweepstake.sweepstake_status() == 2

def test_redeploy_open_sweepstake():
    account_owner = accounts[0]
    account_enter = accounts[1]
    sweepstake = Sweepstake.deploy({"from":account_owner})
    tx = sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    winner_team = tx.events["PlayerTeam"]["teamRandom"]
    sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    sweepstake.enter(20, {"from":account_enter, "value": entry_fee})
    sweepstake.payWinner(winner_team, {"from":account_owner})
    sweepstake.openSweepstake(
        "0x417273656e616c00000000000000000000000000000000000000000000000000",
        "0x4d616e6368657374657220556e69746564000000000000000000000000000000",
        "0x4c69766572706f6f6c0000000000000000000000000000000000000000000000",
        "0x4e6f7474696e6768616d00000000000000000000000000000000000000000000",
        "0x4d616e6368657374657220436974790000000000000000000000000000000000",
        "0x4d616e6368657374657220436974790000000000000000000000000000000000", {"from":account_owner})
    actual_team = sweepstake.getTeam(0)
    expected_team = "0x4e6f7474696e6768616d00000000000000000000000000000000000000000000"
    actual_status = sweepstake.sweepstake_status()
    assert actual_team == expected_team
    assert actual_status == 0
    







