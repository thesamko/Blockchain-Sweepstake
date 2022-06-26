from brownie import accounts, config

def decode_hex_strings(hex_string):
    ascii_string = hex_string.decode("utf-8").rstrip("0")
    if len(ascii_string) % 2 != 0:
        ascii_string = ascii_string + '0'
    return ascii_string

def get_account():
    return accounts.add(config["wallets"]["from_key"])
