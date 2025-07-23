# txn/crypto_utils.py

from Crypto.Cipher import AES
import base64
import hashlib

BLOCK_SIZE = 16  # AES block size

def pad(text):
    text = str(text)
    pad_len = BLOCK_SIZE - len(text) % BLOCK_SIZE
    return text + chr(pad_len) * pad_len

def unpad(text):
    return text[:-ord(text[-1])]

def get_private_key(key):
    """
    Derives a 256-bit key from the given string key using SHA-256.
    """
    return hashlib.sha256(key.encode('utf-8')).digest()

def encrypt_data(raw, key):
    """
    Encrypts the given data with AES ECB mode using the derived key.
    """
    raw = pad(raw)
    private_key = get_private_key(key)
    cipher = AES.new(private_key, AES.MODE_ECB)
    encrypted = cipher.encrypt(raw.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_data(enc, key):
    """
    Decrypts the AES encrypted data using the same key.
    """
    enc = base64.b64decode(enc)
    private_key = get_private_key(key)
    cipher = AES.new(private_key, AES.MODE_ECB)
    decrypted = cipher.decrypt(enc).decode('utf-8')
    return unpad(decrypted)

# Optional: Run this file directly to test the functions
if __name__ == "__main__":
    test_key = "my_secret_key"
    test_data = "Hello, MPS user!"

    encrypted = encrypt_data(test_data, test_key)
    print("Encrypted:", encrypted)

    decrypted = decrypt_data(encrypted, test_key)
    print("Decrypted:", decrypted)
