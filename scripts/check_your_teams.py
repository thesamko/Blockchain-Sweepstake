from brownie import Sweepstake, accounts
import time

account = accounts.add("0xa06ea5c253925ade7e8e4d1cd613812396e8f47f2727ca15c6aa4291b758dc9b")

def decode_hex_strings(hex_string):
    new_hex = hex_string[2:]
    bytes_object = new_hex.fromhex(new_hex)
    ascii_string = bytes_object.decode("ASCII")
    return ascii_string

def check_your_teams():
    sweepstake = Sweepstake[-1]
    val = sweepstake.getParticipantTeams()
    return val
    
def main():
    check_your_teams()
