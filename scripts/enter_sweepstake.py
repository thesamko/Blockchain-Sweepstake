from brownie import Sweepstake, accounts
import random

random_number = random.randint(1,9999)

def decode_hex_strings(hex_string):
    new_hex = hex_string
    ascii_string = new_hex.decode("utf-8")
    return ascii_string

def enter(_random_number):
    account = accounts.add("0xa06ea5c253925ade7e8e4d1cd613812396e8f47f2727ca15c6aa4291b758dc9b")
    sweepstake = Sweepstake[-1]
    tx = sweepstake.enter(_random_number,{"from": account, "value": 10000500000})
    tx.wait(1)
    return tx

def main():
    tx = enter(random_number)
    orderdic = [i for i in tx.events[0][0].popitem()]
    print(decode_hex_strings(orderdic[-1]))
    