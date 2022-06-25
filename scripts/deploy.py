from brownie import accounts, Sweepstake
import random

random_number = random.randint(1,3)

account = accounts.add("0xa06ea5c253925ade7e8e4d1cd613812396e8f47f2727ca15c6aa4291b758dc9b")

def sweepstake():
    sweepstake = Sweepstake.deploy({"from":account})
    #tx = sweepstake.enter(random_number,{"from": account, "value": 10000000000})
    

def main():
    sweepstake()



