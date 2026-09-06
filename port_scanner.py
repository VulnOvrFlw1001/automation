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
    with concurrent.futures.ThreadPoolExecutor(max_workers=400) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in range(start_port, end_port + 1)}
        total_ports = end_port - start_port + 1
        for i, future in enumerate(concurrent.futures.as_completed(futures), start=1)
            port, service, banner, status = future.result()
            results.append((port, service, banner, status))
            sys.stdout.write(f"\rProgress: {i}/total_ports ports scanned")
            sys.stdout.flush()