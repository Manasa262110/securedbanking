# block.py

"""
Backup of blockchain integration logic used in transaction views.
This module is currently not linked to any views or models.
"""

import hashlib
import time
import json

blockchain = []

def create_genesis_block():
    return {
        'index': 0,
        'timestamp': time.time(),
        'data': 'Genesis Block',
        'prev_hash': '0',
        'hash': '',
    }

def calculate_hash(block):
    block_data = f"{block['index']}{block['timestamp']}{block['data']}{block['prev_hash']}"
    return hashlib.sha256(block_data.encode()).hexdigest()

def create_block(data, prev_block):
    block = {
        'index': prev_block['index'] + 1,
        'timestamp': time.time(),
        'data': data,
        'prev_hash': prev_block['hash'],
        'hash': '',
    }
    block['hash'] = calculate_hash(block)
    return block

def send_to_chain(data):
    """
    Appends a transaction to the blockchain.
    `data` should be a string like: "TXN:from_user->to_user:amount"
    """
    if not blockchain:
        genesis_block = create_genesis_block()
        genesis_block['hash'] = calculate_hash(genesis_block)
        blockchain.append(genesis_block)

    prev_block = blockchain[-1]
    new_block = create_block(data, prev_block)
    blockchain.append(new_block)

    print(f"Block added: {json.dumps(new_block, indent=4)}")

# Example usage (won't run unless this file is run directly)
if __name__ == '__main__':
    send_to_chain("TXN:alice->bob:100")
    send_to_chain("TXN:bob->charlie:50")
