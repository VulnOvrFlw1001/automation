import scapy.all as scapy
import socket

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_request
    answer = scapy.srp(packet, timeout=1, verbose=False)[0]

    clients = []
    for client in answer:
        client_info = {'IP' : client[1].psrc, 'MAC': client[1].hwsrc}
        try:
            hostname = socket.gethostbyaddr(client_info['IP'])[0]
            client_info['Hostname'] = hostname
        except socket.herror:
            client_info['Hostname'] = 'Unknown'
        clients.append(client_info)

def print_result(result):
    print('IP' + " "*20 + 'MAC' + " "*20 + 'Hostname')
    print('-'*80)
    for client in result:
        print(client['IP'] + '\t\t' + client['MAC'] + '\t\t' + client['Hostname'])
