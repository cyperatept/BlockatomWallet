from pywallet import *
from pywallet.utils import *

def generic_address(index):
    seed = 'usage good bronze peasant find trouble rate stock guitar monkey awake alpha'
    master_key = wallet.HDPrivateKey.master_key_from_mnemonic(seed)
    root_keys = wallet.HDKey.from_path(master_key, "m/44'/0'/0'/0")[-1].public_key.to_b58check()
    xpublic_key = (root_keys)
    address = Wallet.deserialize(xpublic_key, network='BTC').get_child(index, is_prime=False).to_address()
    rootkeys_wif = wallet.HDKey.from_path(master_key, f"m/44'/0'/0'/0/{index}")[-1]
    xprivatekey = (rootkeys_wif.to_b58check())
    wif = Wallet.deserialize(xprivatekey, network='BTC').export_to_wif()
    return address, wif