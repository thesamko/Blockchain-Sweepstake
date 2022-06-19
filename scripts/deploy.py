from brownie import accounts, Sweepstake
account = accounts.add("0xa06ea5c253925ade7e8e4d1cd613812396e8f47f2727ca15c6aa4291b758dc9b")
def sweepstake():
    sweepstake = Sweepstake.deploy({"from":account})

def main():
    sweepstake()



