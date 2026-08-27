import itertools
import pikepdf

def generate_passwords(chars, min_length, max_length):
    for length in range(min_length, max_length + 1):
        for password in  itertools.product(chars, repeat=length):
            yield ''.join(password)

def load_wordllist(wordlist_file):
    with open(wordlist_file, 'r') as file:
        for line in file:
            yield line.strip()

def try_password(pdf_file, password):
    try:
        with pikepdf.open(pdf_file, password=password) as pdf:
            print(f'[+] Password found: {password}')
            return password
    except pikepdf._core.PasswordError:
        return None