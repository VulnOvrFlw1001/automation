import hashlib 
import itertools
import string
from concurrent.futures import ThreadPoolExecutor

hash_name = [
    'md5',
    'sha1',
    'sha224',
    'sha384',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'sha512'
]

def generate_passwords(min_length, max_length, characters):
    for length in range(min_length, max_length + 1):
        for pwd in itertools.product(characters, repeat=length):
            yield ''.join(pwd)

def crack_hash(hash, wordlist=None, hash_type='md5', min_length=0, characters=string.ascii_letters + string.digits, max_workers=4):
    hash_fn = getattr(hashlib, hash_type, None)
    if hash_fn is None or hash_type not in hash_name:
        raise ValueError(f'[!] Invalid hash type: {hash_type} supported are {hash_name}')
    
    if wordlist:
        with open(wordlist, 'r') as f:
            lines = f.read()
            total_lines = len(lines)
            print(f"[*] Cracking hash {hash} using {hash_type} with a list of {total_lines} passwords.")
    
