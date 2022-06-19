from brownie import accounts, Sweepstake, config, network
account = accounts.add("0xa06ea5c253925ade7e8e4d1cd613812396e8f47f2727ca15c6aa4291b758dc9b")
def sweepstake():
    sweepstake = Sweepstake.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link_token"],
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],        
        {"from":account})
    return sweepstake

def main():
    sweepstake()



