import hashlib
import datetime

def generate_hash(data, prev_hash=""):
    record = f"{data}-{prev_hash}-{datetime.datetime.now()}"
    return hashlib.sha256(record.encode()).hexdigest()

def create_block(transaction, prev_hash):
    data = f"{transaction.from_account}->{transaction.to_account}:{transaction.amount}:{transaction.txntype}"
    return {
        "data": data,
        "prev_hash": prev_hash,
        "hash": generate_hash(data, prev_hash),
        "timestamp": str(datetime.datetime.now())
    }
