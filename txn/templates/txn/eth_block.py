# eth_blockchain.py

"""
Ethereum blockchain integration using Web3.py and Ganache.
This file is NOT linked to any Django views or models and is safe for backup/testing only.
"""

from web3 import Web3
import json

# Connect to local Ethereum node (Ganache)
ganache_url = "http://127.0.0.1:7545"  # Default for Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if not web3.is_connected():
    print("⚠️ Unable to connect to Ethereum network.")
    exit()

# Example accounts (replace with your Ganache account addresses)
account_1 = web3.eth.accounts[0]
account_2 = web3.eth.accounts[1]

# Example transaction
def send_eth_transaction():
    tx = {
        'from': account_1,
        'to': account_2,
        'value': web3.to_wei(0.01, 'ether'),
        'gas': 21000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account_1)
    }

    # Sign and send transaction (no private key needed with Ganache unlocked accounts)
    tx_hash = web3.eth.send_transaction(tx)
    print(f"✅ Transaction sent: {tx_hash.hex()}")

# Optional: Simple contract example (Solidity code must be compiled separately)
def deploy_dummy_contract():
    # This example requires bytecode + ABI of a compiled contract
    bytecode = "6080604052348015600f57600080fd5b50604..."  # Example
    abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"}]')

    Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Contract.constructor().transact({'from': account_1})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"✅ Contract deployed at: {tx_receipt.contractAddress}")

# Run only when this script is executed directly
if __name__ == "__main__":
    print("🔗 Ethereum test started...")
    send_eth_transaction()
    # deploy_dummy_contract()  # Uncomment if you have a real ABI + bytecode
