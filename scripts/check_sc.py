from brownie import accounts, Sweepstake
from scripts.deploy import sweepstake

account = accounts.add("0xa06ea5c253925ade7e8e4d1cd613812396e8f47f2727ca15c6aa4291b758dc9b")

def check_sc():
    sweepstake = Sweepstake[-1]
    val = sweepstake.getRandomTeam(1)
    return val

def main():
    print(check_sc())