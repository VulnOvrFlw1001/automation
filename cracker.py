import itertools
import pikepdf

def generate_passwords(chars, min_length, max_length):
    for length in range(min_length, max_length + 1):
        for password in  itertools.product(chars, repeat=length):
            yield ''.join(password)
