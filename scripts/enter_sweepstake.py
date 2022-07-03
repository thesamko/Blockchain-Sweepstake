from brownie import Sweepstake, accounts
from scripts.utils import *
import random

random_number = random.randint(1,9999)

def sweepstake_deploy():
    sweepstake = Sweepstake.deploy({"from": get_account()})

def enter(_random_number):
    account = accounts.add("0x5fb54a807b66f08d9f9e2f607a9b58abaf7e16e00ef4e5aadce078f9c456c94c")
    sweepstake = Sweepstake[-1]
    tx = sweepstake.enter(_random_number,{"from": accounts[1], "value": 10000000000})
    tx.wait(1)
    picked_team = tx.events["PlayerTeam"]["teamRandom"]
    return decode_hex_strings(picked_team)

def main():
    sweepstake_deploy()
    print(enter(random_number))
    
    