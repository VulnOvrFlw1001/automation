import hashlib 
import itertools

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