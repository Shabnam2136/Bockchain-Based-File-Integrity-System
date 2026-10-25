from web3 import Web3

url = "https://eth-sepolia.g.alchemy.com/v2/ANE3rmvTrsensSqv4vIN8"

w3 = Web3(Web3.HTTPProvider(url))

print("Connected:", w3.is_connected())
