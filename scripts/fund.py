from brownie import Sweepstake, accounts



def fund():
    account = accounts.add("0xa06ea5c253925ade7e8e4d1cd613812396e8f47f2727ca15c6aa4291b758dc9b")
    sweepstake = Sweepstake[-1]
    sweepstake.openSweepstake({"from": account})
    sweepstake.enter({"from": account, "value": 10000000000})

def main():
    fund()