from web3 import Web3
import hashlib
import os
import time
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# ---------------- CONFIG ----------------

RPC_URL = "https://eth-sepolia.g.alchemy.com/v2/ANE3rmvTrsensSqv4vIN8"
PRIVATE_KEY = "0x860ed389dc6f086b64623ad531e204c0ede89b8b7109eec197d4025ebeeadffc"
WALLET = "0x118d3Fe7AA1007fa036f93CcC97491104fE16901"
CONTRACT = "0x3c9dc4E9a4BCD6B030D15C921C8A6F73ceabd9F5"

# ---------------- ABI ----------------

ABI = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_fileName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_fileHash",
				"type": "string"
			}
		],
		"name": "addFile",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "authorizeUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "revokeUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "authorizedUsers",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "files",
		"outputs": [
			{
				"internalType": "string",
				"name": "fileName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "fileHash",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "uploadedBy",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "version",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getFile",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTotalFiles",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "latestVersion",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

    

# ---------------- CONNECT ----------------

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print("❌ Failed to connect to Sepolia")
    exit()

print("✅ Connected to Sepolia")

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT),
    abi=ABI
)

# ---------------- GET ALL RECORDS ----------------

def get_all_records():
    records = []
    total = contract.functions.getTotalFiles().call()
    
    for i in range(total):
        data = contract.functions.getFile(i).call()
        records.append({
        "name": data[0],
        "hash": data[1],
        "timestamp": data[2],
        "owner": data[3],
        "version": data[4]
})

    return records

# ---------------- STORE FILES ----------------

print("\n📂 Scanning local folder for .txt files...\n")

blockchain_records = get_all_records()
existing_hashes = [r["hash"] for r in blockchain_records]

nonce = w3.eth.get_transaction_count(WALLET, "pending")

        
for filename in os.listdir("."):
    if filename.endswith(".txt"):

        with open(filename, "rb") as f:
            file_data = f.read()

        file_hash = hashlib.sha256(file_data).hexdigest()

        if file_hash in existing_hashes:
            print(f"⚠ Duplicate skipped: {filename}")
            continue

        print(f"📁 Storing: {filename}")
        print(f"🔐 Hash: {file_hash}")

        tx = contract.functions.addFile(filename, file_hash).build_transaction({
            "chainId": 11155111,
            "gas": 300000,
            "maxFeePerGas": w3.to_wei("30", "gwei"),
            "maxPriorityFeePerGas": w3.to_wei("2", "gwei"),
            "nonce": nonce,
            "from": WALLET
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print("🚀 TX:", tx_hash.hex())

        try:
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
            print("✅ Confirmed in block:", receipt.blockNumber)
        except Exception:
            print("⚠ Transaction not confirmed yet")
            print("https://sepolia.etherscan.io/tx/" + tx_hash.hex())

        nonce += 1
        existing_hashes.append(file_hash)
        time.sleep(2)

# ---------------- VERIFICATION MODE ----------------

print("\n🔍 Verification Mode\n")

blockchain_records = get_all_records()

for filename in os.listdir("."):
    if filename.endswith(".txt"):

        with open(filename, "rb") as f:
            file_data = f.read()

        current_hash = hashlib.sha256(file_data).hexdigest()

        matched = False

        for record in blockchain_records:
            if record["name"] == filename:
                matched = True

                if record["hash"] == current_hash:
                    print(f"✅ {filename} is SAFE")
                else:
                    print(f"🚨 {filename} has been TAMPERED!")

                break

        if not matched:
            print(f"❌ {filename} not found on blockchain")
# ---------------- DISPLAY RECORDS ----------------

print("\n📊 Blockchain Records\n")

for i, record in enumerate(blockchain_records):
    readable_time = datetime.fromtimestamp(record["timestamp"])
    print("=" * 60)
    print(f"Index      : {i}")
    
    print(f"Version    : {record['version']}")
    print(f"File Name  : {record['name']}")
    print(f"Owner      : {record['owner']}")
    print(f"Timestamp  : {readable_time}")
    print(f"Hash       : {record['hash']}")
    print("=" * 60)
    
    

# ---------------- GENERATE PDF REPORT ----------------

print("\n📄 Generating PDF Report...")

doc = SimpleDocTemplate("Blockchain_Report.pdf")
elements = []
styles = getSampleStyleSheet()

elements.append(Paragraph("Blockchain File Integrity Report", styles["Title"]))
elements.append(Spacer(1, 0.5 * inch))

for i, record in enumerate(blockchain_records):
    readable_time = datetime.fromtimestamp(record["timestamp"])
    text = f"""
    Index: {i}<br/>
    File: {record['name']}<br/>
    Version: {record['version']}<br/>
    Owner: {record['owner']}<br/>
    Timestamp: {readable_time}<br/>
    Hash: {record['hash']}<br/><br/>
    """
    elements.append(Paragraph(text, styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

doc.build(elements)

print("✅ PDF Generated: Blockchain_Report.pdf")
print("\n🎉 SYSTEM COMPLETE")

print(contract.functions.authorizedUsers(WALLET).call())