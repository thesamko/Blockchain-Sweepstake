from brownie import Sweepstake
from scripts.utils import *
import random

random_number = random.randint(1,9999)

def enter(_random_number):
    account = get_account()
    sweepstake = Sweepstake[-1]
    tx = sweepstake.enter(_random_number,{"from": account, "value": 10000000000})
    tx.wait(1)
    return tx

def main():
    tx = enter(random_number)
    picked_team = [i for i in tx.events[0][0].popitem()]
    print(decode_hex_strings(picked_team[-1]))
    