from brownie import Sweepstake, accounts
import random

random_number = random.randint(1,3)


def enter(_random_number):
    account = accounts.add("0xa06ea5c253925ade7e8e4d1cd613812396e8f47f2727ca15c6aa4291b758dc9b")
    sweepstake = Sweepstake[-1]
    tx = sweepstake.enter(_random_number,{"from": account, "value": 10000000000})
    tx.wait(5)

def main():
    print(random_number)
    enter(random_number)