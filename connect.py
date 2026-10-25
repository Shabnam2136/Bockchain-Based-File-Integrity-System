import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SEPOLIA_RPC_URL")

if not url:
    raise ValueError("SEPOLIA_RPC_URL is missing from .env")

w3 = Web3(Web3.HTTPProvider(url))

print("Connected:", w3.is_connected())
