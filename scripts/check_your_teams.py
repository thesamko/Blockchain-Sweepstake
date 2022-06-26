from brownie import Sweepstake
from scripts.utils import *

account = get_account()

def check_your_teams():
    sweepstake = Sweepstake[-1]
    return sweepstake.getParticipantTeams("0x8FD52e7f0a51DdE47FFdEe0bB73AbEF1B1C5Ed41",{"from":account}) #anyAccountNumber
    
def main():
    tx = check_your_teams()
    list_teams = [decode_hex_strings(i) for i in tx.events[0][0].popitem()[-1]]
    print(", ".join(list_teams))