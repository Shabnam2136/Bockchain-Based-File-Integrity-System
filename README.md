# Blockchain-Based File Integrity System

A Python-based project that uses blockchain technology and SHA-256 hashing to verify file integrity and detect unauthorized modifications.

## Overview

This project demonstrates how blockchain technology can support file authentication by generating a unique SHA-256 hash for a file and recording its authentication data through a smart contract. The system helps verify whether a file matches its previously recorded state.

## Features

- **SHA-256 Hashing:** Generates a cryptographic hash for file integrity verification.
- **Blockchain Integration:** Connects to the Ethereum Sepolia test network using Web3.py.
- **Smart Contract Interaction:** Supports storing and retrieving file authentication data.
- **File Integrity Verification:** Compares file hashes to identify potential modifications.
- **Tamper Detection:** Flags files whose calculated hashes differ from their recorded hashes.

## Technologies Used

- Python
- Web3.py
- Solidity smart contracts
- Ethereum Sepolia testnet
- SHA-256
- Alchemy RPC
- JSON (contract ABI)

## Project Structure

```text
blockchain-file-authentication/
├── abi.json
├── blockchain.py
├── connect.py
├── read_contract.py
├── test.py
├── requirements.txt
├── README.md
├── .gitignore
└── Blockchain_Report.pdf
```

*The structure above lists the main files shown in the repository. Update it if your final project contains additional files or directories.*

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Shabnam2136/blockchain-file-authentication.git
cd blockchain-file-authentication
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `python-dotenv` is not included in your requirements, install it using:

```bash
pip install python-dotenv
```

### 4. Configure the RPC URL

Create a local `.env` file in the project root:

```text
SEPOLIA_RPC_URL=your_alchemy_sepolia_rpc_url
```

Replace the placeholder with your own Alchemy Sepolia RPC URL.

**Security note:** Never commit your `.env` file, API keys, wallet private keys, or seed phrases to GitHub.

### 5. Run the connection test

```bash
python connect.py
```

A successful connection should display:

```text
Connected: True
```

## How It Works

1. A file is selected for authentication.
2. The system calculates its SHA-256 hash.
3. Authentication data is stored or retrieved through blockchain smart contract interactions.
4. The file's current hash is compared with the previously recorded hash.
5. A mismatch indicates that the file may have been modified.

## Security Considerations

- File integrity verification depends on comparing hashes against trustworthy recorded values.
- Blockchain records can provide tamper-evident evidence, but do not guarantee the authenticity of a file at the time it was first registered.
- The Sepolia network is a test network and is not intended for production use.
- API credentials must be stored securely outside the source code.

## Limitations

This project is an educational prototype. Its functionality depends on the deployed smart contract, the configured RPC endpoint, and the implementation of the authentication workflow.

## Future Enhancements

- Add a user-friendly interface for file uploads and verification.
- Improve authentication history and audit logging.
- Expand automated tests for file modification scenarios.
- Improve error handling and configuration management.

## Author

**Shabnam Qureshi**
**&**
**Vistruti Mahajan**

Cybersecurity Master's Student

GitHub: [Shabnam2136](https://github.com/Shabnam2136)

---

*Developed as a cybersecurity project exploring blockchain-based file integrity and authentication.*
