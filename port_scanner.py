import socket
import concurrent.futures
import sys

def get_banner(sock):
    try:
        sock.settimeout(1)
        banner = sock.recv(1024).decode().strip()
        return banner
    except:
        return " "

def scan_port(target_ip, port): 
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip.port))
        if result == 0:
            try:
                service = socket.getservbyport(port, 'tcp')
            except:
                service = 'Unknown'
            banner = get_banner(sock)
            return port, service, banner, True
        else:
            return port, "", "", False
    except:
        return port, "", "", False
    finally:
        sock.close()

def port_scan(target_host, start_port, end_port):
    target_ip = socket.gethostbyname(target_host)
    print(f"starting scan on host: {target_ip}")

    results = []
    