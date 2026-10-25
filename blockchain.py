from web3 import Web3
import json
import hashlib

def hash_file(filename):
    sha = hashlib.sha256()
    with open(filename, "rb") as f:
        while chunk := f.read(4096):
            sha.update(chunk)
    return sha.hexdigest()


# connect to Sepolia
alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/ANE3rmvTrsensSqv4vIN8"
w3 = Web3(Web3.HTTPProvider(alchemy_url))
print("Connected:", w3.is_connected())


# load ABI
with open("abi.json") as f:
    abi = json.load(f)

contract_address = "0x9D7f74d0C41E726EC95884E0e97Fa6129e3b5E99"
contract = w3.eth.contract(address=contract_address, abi=abi)

# wallet
account = "0x118d3Fe7AA1007fa036f93CcC97491104fE16901"
private_key = "0x860ed389dc6f086b64623ad531e204c0ede89b8b7109eec197d4025ebeeadffc"

file_path = "record.txt"
hash_val = hash_file(file_path)

print("File hash:", hash_val)


tx = contract.functions.addFile(hash_val, "record.txt").build_transaction({
    'from': account,
    'nonce': w3.eth.get_transaction_count(account),
    'gas': 200000,
    'gasPrice': w3.to_wei('10', 'gwei'),
    'chainId': 11155111
})


signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)


print("Stored hash:", hash_val)
print("TX:", tx_hash.hex())

total = contract.functions.totalFiles().call()
print("Total files:", total)

if total > 0:
    stored = contract.functions.getFile(total - 1).call()
    print("Stored from blockchain:", stored)
else:
    print("No files found")

