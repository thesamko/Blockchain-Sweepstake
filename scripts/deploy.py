from brownie import Sweepstake, config
from scripts.utils import *

account = get_account()

def sweepstake_deploy():
    sweepstake = Sweepstake.deploy({"from": account})
    
def main():
    sweepstake_deploy()