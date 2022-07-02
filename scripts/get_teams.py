from brownie import Sweepstake, accounts
from scripts.utils import *
import random

random_number = random.randint(1,9999)
account_enter = accounts.add("0x5fb54a807b66f08d9f9e2f607a9b58abaf7e16e00ef4e5aadce078f9c456c94c")

def sweepstake_deploy():
    sweepstake = Sweepstake.deploy({"from": get_account()})

def enter(_random_number):
    sweepstake = Sweepstake[-1]
    tx = sweepstake.enter(_random_number,{"from": account_enter, "value": 10000000000})
    tx.wait(1)

def get_teams():
    sweepstake = Sweepstake[-1]
    ex = sweepstake.getParticipantTeams(account_enter, {"from":account_enter})
    return ex.events["AllPlayersTeams"]["teamsP"]

def main():
    sw = get_teams()
    for i in sw:
        print(decode_hex_strings(i))
